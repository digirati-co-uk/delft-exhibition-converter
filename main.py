import json
import sys
from os import listdir
from os.path import join, abspath, dirname
from shutil import copy

# settings
CONVERT_INFO_CANVAS_BODIES = True
CONVERT_INFO_CANVAS_POPUP = True
PAINTING_ANNO_THUMBS = "Annotation"
# PAINTING_ANNO_THUMBS = "Image"


def convert_folder(old_folder):
    print(f"source: {old_folder}")
    this_dir = dirname(abspath(__file__))
    # copy the source manifest here for easier comparison later
    # Don't use these as sources for conversion though, we want the latest ones.
    copied_source_folder = join(this_dir, "copied_source")
    new_folder = join(this_dir, "converted")
    print(f"dest: {new_folder}")
    manifests = []
    for exhibition in listdir(old_folder):
        source_file = join(old_folder, exhibition)
        copy(source_file, copied_source_folder)
        with open(source_file) as source:
            print(f"Converting {exhibition}")
            manifest = json.load(source)
            new_manifest = convert_manifest(manifest, exhibition)
            manifests.append({
                "id": f"converted/{exhibition}",
                "original": f"copied_source/{exhibition}",
                "label": new_manifest["label"]["en"][0],
                "homepage": new_manifest["homepage"][1]["id"]
            })
            with open(join(new_folder, exhibition), 'w', encoding='utf-8') as dest:
                json.dump(new_manifest, dest, ensure_ascii=False, indent=4)
    with open(join(this_dir, "manifests.json"), 'w', encoding='utf-8') as mini_coll:
        json.dump(manifests, mini_coll, ensure_ascii=False, indent=4)


def convert_manifest(manifest, filename):
    slug = filename.replace(".json", "")

    # Do all the things

    # Old versions had the W3C context as well, not required
    # however we may need to add a custom context for the behaviors
    set_context(manifest)

    # We'll add the live exhibition link to each manifest for convenience
    set_homepage(manifest, slug)

    # labels are already valid language maps

    for canvas in manifest["items"]:
        print(f"converting canvas {canvas['id']}")
        convert_canvas(canvas)

    return manifest


def set_context(manifest):
    manifest["@context"] = "http://iiif.io/api/presentation/3/context.json"


def set_homepage(manifest, slug):
    manifest["homepage"] = [
        {
            "id": f"https://heritage.tudelft.nl/nl/exhibitions/{slug}",
            "type": "Text",
            "format": "text/html",
            "language": ["nl"]
        },
        {
            "id": f"https://heritage.tudelft.nl/en/exhibitions/{slug}",
            "type": "Text",
            "format": "text/html",
            "language": ["en"]
        },
    ]


def convert_canvas(canvas):
    normalise_behavior(canvas)
    if "info" in canvas["behavior"]:
        convert_info_canvas(canvas)
        return

    move_describing_annos(canvas)


def move_describing_annos(canvas):
    anno_page = required_single_item(canvas)
    for_removal = []
    for anno in anno_page["items"]:
        if anno["motivation"] != "painting":
            if anno["motivation"] == "describing":
                annotations = canvas.get("annotations", None)
                if annotations is None:
                    annotations = [{
                        "type": "AnnotationPage",
                        "id": f"{canvas['id']}/annotations",
                        "items": []
                    }]
                    canvas["annotations"] = annotations
                print("moving a describing anno to canvas.annotations")
                for_removal.append(anno)
                annotations[0]["items"].append(anno)
            else:
                raise ValueError("Non-painting anno in canvas.items[0].items")
    if len(for_removal) > 0:
        print(f"{len(for_removal)} describing annos to remove")
        for moved in for_removal:
            anno_page["items"].remove(moved)


def normalise_behavior(canvas):
    # I think the canvas behaviors can be rationalised a little
    print("Converting behaviors from")
    print(canvas["behavior"])
    behaviors = set(canvas["behavior"])  # de-dupe
    canvas["behavior"] = []
    w_ = [x for x in behaviors if x.startswith("w-")][0]
    h_ = [x for x in behaviors if x.startswith("h-")][0]
    if "info" in behaviors:
        canvas["behavior"].append("info")
    else:
        if "row" in behaviors or "left" in behaviors:
            canvas["behavior"].append("left")
        elif "column" in behaviors or "bottom" in behaviors:
            canvas["behavior"].append("bottom")  # (there is no top)
        elif "right" in behaviors:
            canvas["behavior"].append("right")
    canvas["behavior"].append(w_)
    canvas["behavior"].append(h_)
    print("to")
    print(canvas["behavior"])


def convert_info_canvas(canvas):
    # An info canvas has no media on it, but shows text directly, and links to a pop-up with longer text.
    # In the old version, the canvas has label and summary that are displayed directly, and the text annotation
    # has label and summary that are displayed in the pop-up.
    if canvas["height"] != 1000 or canvas["width"] != 1000:
        raise ValueError("Info canvas has unexpected dimensions")
    if get_value(canvas["label"]) is None:
        raise ValueError("Info canvas has no label")
    if get_value(canvas["summary"]) is None:
        raise ValueError("Info canvas has no summary")
    if "requiredStatement" in canvas:
        del canvas["requiredStatement"]  # not used for info

    anno_page = required_single_item(canvas)
    textual_anno = required_single_item(anno_page)  # an info must have only one anno
    must_equal(textual_anno["body"]["type"], "TextualBody", "info anno must have a TextualBody")
    must_equal(textual_anno["motivation"], "painting", "info anno must have a painting motivation")

    # Tobacco mosaic virus in Corona Chronicles does not have a label
    # must_not_be_none(get_value(textual_anno["label"]), "info anno must have a label")
    must_not_be_none(get_value(textual_anno["summary"]), "info anno must have a summary")

    # Should just target the whole canvas
    textual_anno["target"] = textual_anno["target"].split("#")[0]

    # Transformation candidate:
    #  - The text to display on the canvas becomes the actual anno body
    #  - The pop-up text becomes an annotation under the annotations property
    # The problem is that we lose the label/summary distinction
    # We also lose the ability to pull out the first value from the language map - however that isn't used here.
    # BUT this means we have to support label and summary on annotations
    # What is easiest for the Manifest Editor?

    if CONVERT_INFO_CANVAS_BODIES:
        id_root = textual_anno["body"]["id"]
        textual_anno["body"] = []
        nl_body = get_html_from_label_and_summary(canvas, "nl")
        if nl_body is not None:
            textual_anno["body"].append(make_textual_body(nl_body, "text/html", "nl", f"{id_root}/nl"))
        en_body = get_html_from_label_and_summary(canvas, "en")
        if en_body is not None:
            textual_anno["body"].append(make_textual_body(en_body, "text/html", "en", f"{id_root}/en"))
        del canvas["label"]
        del canvas["summary"]

    if CONVERT_INFO_CANVAS_POPUP:
        canvas["annotations"] = [{
            "type": "AnnotationPage",
            "id": f"{canvas['id']}/annotations",
            "items": [{
                "id": f"{canvas['id']}/annotations/0",
                "type": "Annotation",
                "motivation": "describing",
                "target": canvas["id"],
                "body": []
            }]
        }]
        new_anno = canvas["annotations"][0]["items"][0]
        nl_body = get_html_from_label_and_summary(textual_anno, "nl")
        if nl_body is not None:
            new_anno["body"].append(make_textual_body(nl_body, "text/html", "nl", f"{new_anno['id']}/nl"))
        en_body = get_html_from_label_and_summary(textual_anno, "en")
        if en_body is not None:
            new_anno["body"].append(make_textual_body(en_body, "text/html", "en", f"{new_anno['id']}/en"))

        if "label" in textual_anno:
            del textual_anno["label"]
        del textual_anno["summary"]


def get_html_from_label_and_summary(resource, lang):
    html = ""
    label = get_value(resource.get('label', None), lang)
    if label is not None:
        html = f"<h1>{label[0]}</h1>\n\n"
    summary = get_value(resource['summary'], lang)
    if summary is not None:
        for val in summary:
            if len(val) > 0:
                if val[0] == "<":
                    html += f"{val}\n\n"
                else:
                    html += f"<p>{val}</p>\n\n"
    if len(html) == 0:
        return None

    return html


def make_textual_body(body, format, language, id):
    return {
        "type": "TextualBody",
        "value": body,
        "format": format,
        "language": language,
        "id": id
    }


def required_single_item(thing_with_items):
    items = thing_with_items.get("items", [])
    if len(items) != 1:
        raise ValueError("Object does not have exactly one member in .items")
    return items[0]


def must_equal(a, b, message):
    if a != b:
        raise ValueError(message)


def must_not_be_none(a, message):
    if a is None:
        raise ValueError(message)


def get_value(lang_map, lang=None):
    if lang_map is None:
        return None
    if lang is not None:
        return lang_map.get(lang, None)

    # default to en for our tests
    val = lang_map.get("en", None)
    if val is not None:
        return val
    return lang_map.get("nl", None)


if __name__ == '__main__':
    convert_folder(sys.argv[1])
