import json
import sys
from os import listdir
from os.path import join, abspath, dirname
from shutil import copy

# settings
CONVERT_INFO_CANVAS_BODIES = True
CONVERT_INFO_CANVAS_POPUP = True
PRESERVE_ANNO_LABELS = True
PAINTING_ANNO_THUMBS = "Annotation"
# PAINTING_ANNO_THUMBS = "Image"

ITEMS_ANNOS_COUNT = 0
ITEMS_ANNOS_WITH_LABELS_COUNT = 0
ITEMS_ANNOS_WITH_SUMMARIES_COUNT = 0
ANNOS_WITHOUT_LABELS = []
ANNOS_WITHOUT_SUMMARIES = []
REMOVED_ANNOS = []
ANNOS_WITH_NO_DESC = []

# See https://github.com/IIIF/iiif-av/issues/27
# and see https://gist.github.com/stephenwf/a1339aa170a2e80fa120f86027b89f46
# via https://digirati.slack.com/archives/D0E15T142/p1663263077484059
YOUTUBE_CONVERT = "Objectifier"  # Tells the client what <object> tag to render
# YOUTUBE_CONVERT = "Service"  # lets the client decide but client must recognise form


def convert_folder(old_folder):
    print(f"source: {old_folder}")
    this_dir = dirname(abspath(__file__))
    # copy the source manifest here for easier comparison later
    # Don't use these as sources for conversion though, we want the latest ones.
    copied_source_folder = join(this_dir, "copied_source")
    new_folder = join(this_dir, "converted")
    print(f"dest: {new_folder}")
    manifests = []
    for exhibition in sorted(listdir(old_folder)):
        source_file = join(old_folder, exhibition)
        copy(source_file, copied_source_folder)
        with open(source_file, encoding="utf-8") as source:
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

    print(f"ITEMS_ANNOS_COUNT: {ITEMS_ANNOS_COUNT}")
    print(f"ITEMS_ANNOS_WITH_LABELS_COUNT: {ITEMS_ANNOS_WITH_LABELS_COUNT}")
    print(f"ITEMS_ANNOS_WITH_SUMMARIES_COUNT: {ITEMS_ANNOS_WITH_SUMMARIES_COUNT}")
    print("ANNOS_WITHOUT_LABELS")
    print(ANNOS_WITHOUT_LABELS)
    print("ANNOS_WITHOUT_SUMMARIES")
    print(ANNOS_WITHOUT_SUMMARIES)
    print("ANNOS_WITH_NO_DESC")
    print(ANNOS_WITH_NO_DESC)


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

    convert_tour_steps_to_descriptive_annos(canvas)

    move_thumbnails_from_painting_annos_to_their_bodies(canvas)

    remodel_cropped_painting_annos(canvas)

    remodel_av_and_3d_painting_annos(canvas)


def convert_tour_steps_to_descriptive_annos(canvas):
    """
    painting annotations (check that the body is an image) under canvas.items retain their labels and summaries.

    canvases retain their labels, summaries and required statement.

    If the anno body is a TextualBody it gets removed from the painting annos altogether, it's ONLY a describing anno.
    Tours will be run from the describing annos, moving the user around the canvas.

    If a canvas.items only has one anno and it's a painting anno, leave as-is (?) - it's not a tour!
    You don't need to make a describing anno for it.

    motivation["describing"]
    """
    anno_page = required_single_item(canvas)
    for_removal = []
    expected_body_types = ["Image", "Video", "TextualBody"]
    for anno in anno_page["items"]:

        if anno["body"]["id"] == "https://dlc.services/iiif-img/7/6/acd52dad-b8b1-4afa-9ddf-77ee85397003/376,407,1042,758/full/0/default.jpg":
            print("here")

        if anno["body"]["type"] not in expected_body_types:
            raise ValueError(f"Unexpected anno body type: {anno['body']['type']}")

        update_anno_counters(anno)

        label = anno.get("label", None)
        summary = anno.get("summary", None)

        if label is None and summary is None:
            # maps are an example of this
            # https://delft-static-site-generator.netlify.com/iiif/1f05178d-9382-53b9-cd33-86ffd19f0476/canvas/f5868dbe-e170-33d5-1623-9aa2dfbb6635
            # they stay as plain painting annos but for now we'll still make them tour steps
            # raise ValueError(f"anno without label or summary: {anno}")
            pass

        if (label is not None or summary is not None) and len(anno_page["items"]) > 1:
            # For our initial migration, it's both a painting anno and a tour step
            # But later we can have tour steps that are not painting annos
            annotations = canvas.get("annotations", None)
            if annotations is None:
                # create an annotations property for the canvas
                annotations = [{
                    "type": "AnnotationPage",
                    "id": f"{canvas['id']}/annotations",
                    "items": []
                }]
                canvas["annotations"] = annotations
            describing_anno = {
                "id": f"{canvas['id']}/annotations/{ITEMS_ANNOS_COUNT}",
                "type": "Annotation",
                "motivation": "describing",  # says "this is a tour", but we could have a "tour" motivation
                "target": {  # target the painting annotation
                    "id": anno["id"],
                    "type": "Annotation"
                }
                # There is no "body", just use the info on the painting anno - unless it's a TextualBody
            }

            canvas["annotations"][0]["items"].append(describing_anno)

            nl_body = get_html_from_label_and_summary(anno, "nl", True)
            en_body = get_html_from_label_and_summary(anno, "en", True)
            if nl_body is None and en_body is None:
                # log for information
                ANNOS_WITH_NO_DESC.append(anno["id"])
            elif anno["body"]["type"] == "TextualBody":
                for_removal.append(anno)  # later we'll take this out of canvas.items
                id_root = f"{anno['id']}/desc"
                describing_anno["body"] = []
                describing_anno["target"] = anno["target"]
                if nl_body is not None:
                    describing_anno["body"].append(make_textual_body(nl_body, "text/html", "nl", f"{id_root}/nl"))
                if en_body is not None:
                    describing_anno["body"].append(make_textual_body(en_body, "text/html", "en", f"{id_root}/en"))

    if len(for_removal) > 0:
        print(f"{len(for_removal)} TextualBody annos to remove from the painting annos")
        for moved in for_removal:
            anno_page["items"].remove(moved)
            REMOVED_ANNOS.append(moved["id"])


def update_anno_counters(anno):
    global ITEMS_ANNOS_COUNT
    global ITEMS_ANNOS_WITH_LABELS_COUNT
    global ITEMS_ANNOS_WITH_SUMMARIES_COUNT
    global ANNOS_WITHOUT_LABELS
    global ANNOS_WITHOUT_SUMMARIES

    global ITEMS_ANNOS_COUNT, ITEMS_ANNOS_WITH_LABELS_COUNT, ITEMS_ANNOS_WITH_SUMMARIES_COUNT
    ITEMS_ANNOS_COUNT += 1
    label = anno.get("label", None)
    if label is not None:
        ITEMS_ANNOS_WITH_LABELS_COUNT += 1
    else:
        ANNOS_WITHOUT_LABELS.append(anno["id"])
    summary = anno.get("summary", None)
    if summary is not None:
        ITEMS_ANNOS_WITH_SUMMARIES_COUNT += 1
    else:
        ANNOS_WITHOUT_SUMMARIES.append(anno["id"])


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
            canvas["behavior"].append("left")  # we might remove this if there is no summary - see novieten.json
        elif "column" in behaviors or "bottom" in behaviors:
            canvas["behavior"].append("bottom")  # (there is no top)
        elif "right" in behaviors:
            canvas["behavior"].append("right")
    canvas["behavior"].append(w_)
    canvas["behavior"].append(h_)
    print("to")
    print(canvas["behavior"])


def convert_info_canvas(canvas):
    """
    An info canvas has no media on it, but shows text directly, and links to a pop-up with longer text.
    In the old version, the canvas has label and summary that are displayed directly, and the text annotation
    has label and summary that are displayed in the pop-up.
    """
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
        # Convert the canvas label and summary into a direct painting annotation on the canvas, of type text/html
        # QUESTION - do we want to do this?
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
        # Convert the label and summary of the textual annotation into a non-painting annotation
        # (introducing an annotations property to the canvas)
        # QUESTION - do we want to do this?
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


def move_thumbnails_from_painting_annos_to_their_bodies(canvas):
    anno_page = required_single_item(canvas)
    for anno in anno_page["items"]:
        if anno["motivation"] != "painting":
            raise ValueError(f"Unexpected motivation '{anno['motivation']}' in canvas.items")
        if anno["body"]["type"] != "Image" and anno["body"]["type"] != "Video":
            raise ValueError(f"Unexpected body type '{anno['body']['type']}' in canvas.items")
        thumbnail = anno.get("thumbnail", None)
        if thumbnail is None or PAINTING_ANNO_THUMBS == "Annotation":
            return

        anno["body"]["thumbnail"] = thumbnail
        del anno["thumbnail"]

        # TODO: We should tidy up these thumbnails, the Video ones are... odd.


def remodel_cropped_painting_annos(canvas):
    anno_page = required_single_item(canvas)
    for anno in anno_page["items"]:

        if anno.get("body.id", None) is None:
            # The body.id property is how the old editor signified a crop
            continue

        region = anno["body"]["id"].split("/")[-4]
        anno["body"]["id"] = anno["body"]["id"].replace(f"/{region}/", "/full/")
        specific_resource = {
            "id": f"{anno['id']}/specificResource",
            "type": "SpecificResource",
            "source": anno["body"],
            "selector": {
                "@context": "http://iiif.io/api/annex/openannotation/context.json",
                "type": "iiif:ImageApiSelector",
                "region": region
            }
        }
        anno["body"] = specific_resource
        del anno["body.id"]


def remodel_av_and_3d_painting_annos(canvas):
    anno_page = required_single_item(canvas)
    youtube = "https://www.youtube.com"
    youtube_short = "https://youtu.be"  # transform this!
    sketchfab = "https://sketchfab.com"
    tourmake = "https://tourmake.nl"
    known_embeds = [youtube, youtube_short, sketchfab, tourmake]
    for anno in anno_page["items"]:
        if not anno["body"]["type"] == "Video":
            continue

        body_id = anno["body"]["id"]

        if not body_id.startswith(tuple(known_embeds)):
            raise ValueError("Unknown embed source")

        if body_id.startswith(youtube_short):
            body_id = f"{youtube}/watch?v={body_id.split('/')[-1]}"

        if body_id.startswith(youtube):
            youtube_id = body_id.split("=")[-1]
            if YOUTUBE_CONVERT == "Objectifier":
                anno["body"] = {
                    "id": body_id,
                    "type": "Video",  # tbc
                    "service": {
                        "profile": "http://digirati.com/objectifier",
                        "params": {
                            "data": f"https://www.youtube.com/embed/{youtube_id}"
                        }  # leave width and height to the client?
                    }
                }
            else:
                anno["body"] = {
                    "id": body_id,
                    "service": {
                        "id": body_id,
                        "profile": youtube
                    }
                }
            return

        if body_id.startswith(sketchfab) or body_id.startswith(tourmake):
            # paint the thumbnail onto the canvas and supply the model as a rendering
            # We could also do this with the objectifier, but not as a painting on the canvas because it's
            # not an annotatable space
            anno["body"] = {
                "id": anno["thumbnail"][0]["id"],
                "type": "Image",
                "format": "image/jpg"
            }
            img_service = anno["thumbnail"][0].get("service", None)
            if img_service is not None and img_service.get("type", None) is not None:
                # some weird IIIF for the sketchfab
                anno["body"]["service"] = [img_service]
            canvas["behavior"] = ["placeholder"]
            canvas["rendering"] = [{
                "id": body_id,  # this is the sketchfab embed ID rather than the actual model but...
                "type": "Model",
                "format": "text/html",  # maybe this tells
                "behavior": ["original"]
            }]


def get_html_from_label_and_summary(resource, lang, convert_label=True):
    html = ""
    if convert_label:
        label = get_value(resource.get('label', None), lang)
        if label is not None:
            html = f"<h1>{label[0]}</h1>\n\n"
    summary = get_value(resource.get("summary", None), lang)
    if summary is not None:
        for val in summary:
            if len(val) > 0:
                if val[0] == "<":
                    html += f"{val}\n\n"
                else:
                    html += f"<p>{val}</p>\n\n"
    if len(html) == 0:
        return None

    return html.strip()


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
