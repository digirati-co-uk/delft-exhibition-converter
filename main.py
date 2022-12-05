import json
import sys
from os import listdir
from os.path import join


def convert_folder(old_folder, new_folder):
    print(f"source: {old_folder}")
    print(f"dest: {new_folder}")
    for exhibition in listdir(old_folder):
        with open(join(old_folder, exhibition)) as source:
            print(f"Converting {exhibition}")
            manifest = json.load(source)
            new_manifest = convert_manifest(manifest, exhibition)
            with open(join(new_folder, exhibition), 'w', encoding='utf-8') as dest:
                json.dump(new_manifest, dest, ensure_ascii=False, indent=4)


def convert_manifest(manifest, filename):
    slug = filename.replace(".json", "")
    manifest["@context"] = "http://iiif.io/api/presentation/3/context.json"
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
    return manifest


if __name__ == '__main__':
    convert_folder(sys.argv[1], sys.argv[2])
