
## Links to objects in the collection

The ideal way to do this is formally, in the Manifest, with a `homePage` link (not `seeAlso` which would go to a machine-readable catalogue record).

This `homePage` link could live on the painting annotations, which carry the actual object, and/or on the describing annotations (e.g., so you could describe three pages from the same book in a single describing annotation and only have one link to the object).

At the moment the static site generator (I assume) parses the image GUID from the painting annotation and looks up the object in (...?) to determine what the object URL is - it infers what that `homePage` id would be.

* Can we make the object page explicit in the manifest? As a `homePage` link from the painting annotation OR from the tour step that points to the painting annotation(s) or from... wherever?

Or is that a pain, would it be better for the static site generator to infer it by using the object IDs?

If we make annotations more flexible, the static site generator's rules about what UI element gets an object link become more complicated, so being explicit would help.

## Tour steps

The presence of `describing` annotations makes a Canvas into a tour. The new model is (I hope) more flexible than it appears from what we have now:

Can be seen in converted manifests now:

* The `describing` annotation might target a `painting` annotation and not provide a TextualBody (typical converted tour step, e.g., the 7 "prudish little miss" steps). The exhibition uses the painting annotation's `label` and `summary`.
* The `describing` annotation might target a region of the Canvas, in which case it should provide a TextualBody (e.g., "The only woman in the lecture hall").

The use of TextualBody for tour step describing annotations, rather than `label` and `summary`, is the sticking point here. I think TextualBody is appropriate for the pop-out info panels (see below). The problem is that tour step UI needs a clear heading and description, which the painting annotations provide in their `label` and `summary`, but which a TextualBody only provides if the user creates it in HTML with (for example) an `h1` tag and a `p` tag. For the controlled environment of the exhibition, this is undesirable, we'd rather the tour step text was a plain-text heading and description. So we need to decide whether tour step describing annotations have plain text `label` and `summary`, or whether they have a single `TextualBody`, or whether there's some compromise where the describing anno gets its heading from a `label` but the description from a `text/plain` TextualBody. We're trading ease-of-exhibition-building against idiomatic IIIF.

Natural extensions/variations on the new model:

* The `describing` annotation might target a `painting` anno, but provides its own TextualBody (or `label` and `summary` if we go that way) as well. In this case the exhibition renderer would use the text from the describing annotation as the tour step. If the painting body had a label and summary, they'd be ignored. 
* The `describing` annotation might target a region of the canvas (in which case it should provide its own text), AND ALSO have the `scope` of one or more painting annotations. So while the describing annotation targets the canvas and doesn't link directly to any painting annotation, the content creator makes the connection explicit.

The static site generator can then see that a particular tour step that's just a region of the canvas nevertheless is "about" one or more objects, and it could go and find the information needed to make the _View Object_ links by inspecting the linked painting annotations.

## Info Canvases

This is the model for the info panel canvas, tidied up to make it easier to see.

This model makes sense to me, the text visible initially on the panel is a painting TextualBody, and then the text that appears in the modal popup is the textualBody of a describing annotation. Both can be HTML allowing full control/flexibility of what those panels contain.

```
{
    "height": 1000,
    "width": 1000,
    "type": "Canvas",
    "id": "https://heritage.tudelft.nl/iiif/.../canvas/...",
    "items": [
        {
            "type": "AnnotationPage",
            "items": [
                {
                    "type": "Annotation",
                    "motivation": "painting",
                    "body": [
                        {
                            "type": "TextualBody",
                            "value": "<h1>Introduction</h1>\n\n<p>This text is painted onto the canvas, visible directly on the info panel.</p>",
                            "format": "text/html",
                            "language": "en"
                        }
                    ],
                    "target": "https://heritage.tudelft.nl/iiif/.../canvas/...",
                    "id": "https://heritage.tudelft.nl/iiif/..."
                }
            ]
        }
    ],
    "behavior": [
        "info",
        "w-4",
        "h-4"
    ],
    "annotations": [
        {
            "type": "AnnotationPage"
            "items": [
                {
                    "id": "https://heritage.tudelft.nl/iiif/...",
                    "type": "Annotation",
                    "motivation": "describing",
                    "target": "https://heritage.tudelft.nl/iiif/.../canvas/...",
                    "body": [
                        {
                            "type": "TextualBody",
                            "value": "<h1>Novices</h1>\n\n<p>This is the longer text that appears in the modal pop up.",
                            "format": "text/html",
                            "language": "en",
                            "id": "https://heritage.tudelft.nl/iiif/..."
                        }
                    ]
                }
            ]
        }
    ]
}
```