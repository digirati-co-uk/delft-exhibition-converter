# novieten.json (Novices)

## Canvas 0

```
"height": 2749,
"width": 2666,
"behavior": ["w-8", "h-8"]
```


(Image of lecture hall with only one female student)

Canvas has two annos.

### First one is a painting anno.
This is setting a crop from a slightly larger image as the canvas content.
The Image is a region of a full service: 559,0,2666,2749
This matches the Canvas Size, but the Image w and h are given for the full image:
Image and its service are both:              
```
"height": 2749,
"width": 3637
```

Those values are correct for the image service itself but they are not correct for the Image - it's just a jpeg!

Painting anno has label "The only woman in the lecture hal (Orientation Week 1965)"
Painting anno has summary "TU Delft Library, Special Collections"

There is an extra property of the painting anno, `body.id`, which gives the Image `id` again.
What does this signify? I think it tells the viewer what the crop is because it's not otherwise specified; this is obviously non-standard.

We need to target this properly, as a crop; the image service belongs to the image that has been cropped so that doesn't need anything extra.
The client has to work that out.

### The second anno is a textualBody

```
"type": "TextualBody",
"value": "",
"format": "text/plain",
"language": "nl",
```

This has motivation describing.
It targets the female student.
It is visible when the exhibition loads.

It has NO text for the value of the textual body.

It has the same label and summary as the painting anno.
Describing anno has label "The only woman in the lecture hal (Orientation Week 1965)"
Describing anno has summary "TU Delft Library, Special Collections"

?? Move this anno to `annotations`?

This becomes a tour with two steps: the initial canvas, then zoom in on the 

Compare with Canvas 2 where the anno is not visible

## Canvas 1

```
"height": 1000,
"width": 1000,      
"behavior": ["info", "info", "w-4", "h-4"]
```

This is a text panel. It has an arbitrary dimension of 1000,1000.
The _Canvas_ has the label "Introduction"
The _Canvas_ has the summary "In the past, new members of the..."

This is the text displayed _on the canvas_ (the black square) as part of the exhibition.
Separate string values in the summary become the paragraphs on the info black panel itself (only one here)
When this is rendered, a "Read more" link pops open the full text which is carried in HTML as the `summary` property of the single painting anno, which is a TextualBody:

`"<p>In the past, new members of the <em>Delftste Vrouwelijke Studentenvereniging</em> (..."`
(Note HTML)

The label of the TextualBody anno is the heading on this popup. `info` behavior indicates the popup.

Note that the Textual Body itself is not used to carry the anno text.

It has NO text for the value of the textual body.

```
"type": "TextualBody",
"value": "new annotation",
"format": "text/plain",
"language": "nl"
```

This Painting anno has label "Novices". This is used as the heading on the opened text panel.
Painting anno has summary "`<p>`In the past, new members of the..." (the full text)

## Canvas 2

This single Canvas supplies both panels - the image and its description (arrow points)
So here the text is not a separate canvas.

```
"height": 991,
"width": 992,
"behavior": [ "right", "w-12", "h-8" ]
```

w-12 - is the full width of the exhibition - it knows to turn this into 8 + 4 with the 4 on the right.

These canvas props give the text panel on the right:
Canvas label is "First-year students at the Delft Institute of Technology and TU Delft in the period 1905-2018"
Canvas summary is "This graph shows the absolute number of first-year students, ..."
Canvas requiredStatement is "Sources: Delft Institute of Technology Yearbooks and reports ..." (no label prop supplied)

The first anno is a painting anno, an Image with an image service. It's the full image. 7088 x 7087
It targets 0,0,992,991 (the full canvas).

The second anno is a painting anno, a TextualBody, targeting 49,567,327,330 (the highlight)

When you launch the tour, the heading and sub come from the label and summary of the canvas, but the summary is only the first line of the canvas summary's multiple strings.

The two painting annos give the heading and sub for the two "slides" of the tour:

First, painting Image anno has the label "First-year students at the Delft Institute of Technology and TU Delft in the period 1905-2018"
First, painting Image anno has the summary "Sources: Delft Institute of Technology Yearbooks and reports..."

Second, painting TextualBody anno has the label "Before the Second World War"
Second, painting TextualBody anno has the summary "A striking aspect of the graph is that the percentage ... "


## Canvas 3

This single Canvas supplies both panels - the image and its description (arrow points)
So here the text is not a separate canvas.
Is this the same as 2 just on the left?

```
"height": 762,
"width": 999,
"behavior": [ "left", "w-12", "h-6" ]
```

These canvas props supply the panel on the left:
The Canvas label is "'Don’t be a prudish little miss'"
The Canvas summary is "The DVSV (Delft student society for women), established in 1904..."
The Canvas requiredStatement is "Click ‘Start tour' and then 'View object' to view the complete yearbooks." (_blank_ label)

This canvas is a collage with 7 painting annos
None of the target the full canvas.

When you launch the tour, the heading and sub come from the label and summary of the canvas, but the summary is only the first line of the canvas summary's multiple strings.

Anno 0 is a painting anno, a full image, target 67,80,220,307
Label: "Speech to the new members in 1930"
Summary: "1/2"

Anno 1 is a painting anno, a full image, target 259,58,217,299
Label: "Speech to the new members in 1930"
Summary: "2/2"

Anno 2 is a painting anno, a CROP 376,407,1042,758 from an image 1643 x 2312, target 466,93,342,245.
The painting anno body Image therefore (as above) has an incorrect size (should be 1042 x 758).
This anno uses the body.id construct to point at the Image body to find this size.
Label: "Board of D.V.S.V. 1928-1929"
Summary: (no summary)

Anno 3 is a painting anno, a full image, target 332,386,211,294
Label: "Speech to the new members in 1931"
Summary: "1/3"

Anno 4 is a painting anno, a full image, target 524,416,214,303
Label: "Speech to the new members in 1931"
Summary: "2/3"

Anno 5 is a painting anno, a full image, target 719,396,211,294
Label: "Speech to the new members in 1931"
Summary: "3/3"

Anno 6 is a painting anno, a CROP 377,522,1040,591 from an image 1684 x 2362, target 48,481,299,165.
The painting anno body Image therefore (as above) has an incorrect size (should be 1040 x 591).
This anno uses the body.id construct to point at the Image body to find this size.
Label: "Board of D.V.S.V. 1929-1930"
Summary: (no summary)

## Canvas 4

```
"height": 906,
"width": 1000,
"behavior": [ "w-8", "h-6" ]
```

(no left or right behavior)

This is a regular "show the object" canvas.
There's no tour - but is that just because there's only one anno and it's a painting anno?

Canvas label is "Tube with the PhD award certificate of Antonia Korvezee"
Canvas summary - (no summary)

When you launch the object, as earlier the Annotation label and summary provide the heading and sub:
First painting anno label: "Tube with the PhD award certificate of Antonia Korvezee"
First painting anno summary: "TU Delft Library, Special Collections, 2016.0290.LIB"

First (and only) painting anno has target 0,0,1000,906 which is the whole canvas.


## Canvas 5

This is the info panel for the above object, as with Canvas 1

```
"height": 1000,
"width": 1000,            
"behavior": [ "info", "w-4", "h-6" ]
```

It's an info panel like Canvas 1 which means it has popup text.

This is a text panel. It has an arbitrary dimension of 1000,1000.
The _Canvas_ has the label "Prof. Antonia Korvezee"
The _Canvas_ has the summary "In 1954, Antonia Korvezee (1899-1978) became the first female professor..."
Separate string values in the summary become the paragraphs on the info black panel itself (3 here)

This is the text displayed _on the canvas_ (the black square) as part of the exhibition.
When this is rendered, a "Read more" link pops open the full text which is carried in HTML as the `summary` property of the single painting anno, which is a TextualBody:

`"<p>In 1954, Antonia (Toos) Korvezee (1899-1978) became the first female professor..."`
(Note HTML)

The label of the TextualBody anno is the heading on this popup. `info` behavior indicates the popup.

Note that the Textual Body itself is not used to carry the anno text.

It has NO text for the value of the textual body.


## Canvas 6

This and Canvas 7 are the same as 4 and 5, just with the info panel (this canvas) first.
The behavior height is 5 rather than 6:

```
"height": 1000,
"width": 1000,
"behavior": [ "info", "info", "w-4", "h-5" ]
```

This also has info twice but I don't think that's significant:

Copying the text above to make sure it's true:

It's an info panel like Canvas 1 which means it has popup text.

This is a text panel. It has an arbitrary dimension of 1000,1000.
The _Canvas_ has the label "‘My husband is not an architect – The architecture firm is mine'"
The _Canvas_ has the summary "The legal 'incapacity of women' was abolished in the Netherlands ..."
Separate string values in the summary become the paragraphs on the info black panel itself (2 here)

This is the text displayed _on the canvas_ (the black square) as part of the exhibition.
When this is rendered, a "Read more" link pops open the full text which is carried in HTML as the `summary` property of the single painting anno, which is a TextualBody:

`"<p><em>A preprint version based on eight quotations. Visit "`
(Note HTML)

The label of the TextualBody anno is the heading on this popup. `info` behavior indicates the popup.
(label is "Eight Women in a Man’s World: From Delft Novices to Engineers")

Note that the Textual Body itself is not used to carry the anno text.

It has NO text for the value of the textual body.

## Canvas 7

```
"height": 656,
"width": 1000,
"behavior": [ "left", "w-8", "h-5" ]
```

Why does this have behavior left?

This is a regular "show the object" canvas.
There's no tour - but is that just because there's only one anno and it's a painting anno?

This has a `behavior: left` but Canvas 4 did not have a behavior `right`
I don't think this needs it!

Canvas label is  "The DVSV Club (circa 1956)"
Canvas summary - (no summary)

When you launch the object, as earlier the Annotation label and summary provide the heading and sub:
First painting anno label:  "The DVSV Club (circa 1956)"
First painting anno summary: "First-year Architecture students carrying wood for the fireplace to the storage..."

First (and only) painting anno has target 0,0,1000,656 which is the whole canvas.

## Canvas 8

```
"height": 1440,
"width": 1903,
"behavior": [ "w-12", "h-9" ]
```

Canvas label is "Mejuffrouw, Mijne Heren (Miss and Gentlemen, 1964)"
Canvas summary - (no summary)

(the canvas label overlays the text like this)

This is like a regular "Show the object" Canvas except that the painting anno is a VIDEO
The canvas does not have a duration
The video is on YouTube
It starts 89 seconds in



First (and only) painting anno has target 0,0,1903,1440 which is the whole canvas - but spatial!
So that's wrong

When you launch the object, as earlier the Annotation label and summary provide the heading and sub:
First painting anno label:  "Mejuffrouw, Mijne Heren (Miss and Gentlemen, 1964)"
First painting anno summary: "Mart van den Busken’s film about student life in Delft in the 1960s. Narrated by one of the few female students."


## Canvas 9

```
"height": 1000,
"width": 1000,
"behavior": [ "info", "info", "w-6", "h-4" ]
```
Canvases 9 and 10 are again an info canvas and an object canvas

It's an info panel like Canvas 1 which means it has popup text.

This is a text panel. It has an arbitrary dimension of 1000,1000.
The _Canvas_ has the label "'Sex wasn’t talked about'"
The _Canvas_ has the summary "Boterbrug 5, one of DVSV’s girls houses, was established..."
Separate string values in the summary become the paragraphs on the info black panel itself (2 here)

This is the text displayed _on the canvas_ (the black square) as part of the exhibition.
When this is rendered, a "Read more" link pops open the full text which is carried in HTML as the `summary` property of the single painting anno, which is a TextualBody:

`"<p><em>Interview by Sacha Klinkhamer. Source: Marjan van den ..."`
(Note HTML)

The label of the TextualBody anno is the heading on this popup. `info` behavior indicates the popup.
(label is "An interview with Margreet de Boer")

Note that the Textual Body itself is not used to carry the anno text.

It has NO text for the value of the textual body.

## Canvas 10


```
"height": 679,
 "width": 1000,
"behavior": [ "w-6", "h-4" ]
```

This is a regular "show the object" canvas.
There's no tour - but is that just because there's only one anno and it's a painting anno?

It does not have behavior `left` or `right`

Canvas label is  "Boterbrug 5 Girls House"
Canvas summary - (no summary)

When you launch the object, as earlier the Annotation label and summary provide the heading and sub:
First painting anno label:  "Boterbrug 5 Girls House"
First painting anno summary:  "From the 1970 DVSV Yearbook (Personal archives of Marjan van den Bos)."

First (and only) painting anno has target 0,0,1000,679 which is the whole canvas.

## Canvas 11

Canvas 11 is similar to Canvas 2, it's a full width canvas with a panel

```
"height": 1440,
"width": 2560,
"behavior": [ "right", "w-12", "h-5" ]
```

These canvas props give the text panel on the right:
Canvas label is "Women’s Studies"
Canvas summary is "From the mid-seventies, both the absolute number and the ..." (2 strings))
Canvas requiredStatement is "Here, you can watch Noortje Weenink, a recent gradu" (no label prop supplied)

This is like a regular "Show the object" Canvas except that the painting anno is a VIDEO
The canvas does not have a duration
The video is on YouTube
It starts at 0, no fragment selector this time


First (and only) painting anno has target 0,0,2560,1440 which is the whole canvas - but spatial!
So that's wrong

When you launch the object, as earlier the Annotation label and summary provide the heading and sub:
First painting anno label:  "Noortje Weenink interviews Anna Vos who founded Women’s Studies in 1979"
First painting anno summary:  "Produced in collaboration with the NewMedia Centre"

## Canvas 12

```
"height": 1000,
"width": 762,
"w-5",
"h-7"
```
Canvas 12 is similar to the collage in Canvas 3 except that it's not a two-part panel, it's a regular object panel but it's a collage.

This is like a regular "show the object" canvas, but there's a tour because there are painting annos.

Differences:
Tour can be one full painting anno (or crop via body.id) then a textual anno to highlight
Tour can be no full painting anno then tour through the regions


It does not have behavior `left` or `right`

Canvas label is  "Description of Womens’s Studies (1979)"
Canvas summary - (no summary)

This label appears OVER the canvas like a regular object canvas and not like a two-panel one (where the info panel supplies text)

In Canvas 3 when you launch the full view the canvas label and summary are used to populate the heading and sub, but here there is no canvas summary.

The two painting annos both have
label: "Description of Womens’s Studies (1979)"
summary: "Women’s Studies Archives"

... and this is also the text that appears when the full view is launched.
Need more examples to see how this goes together.

## Canvas 13

This is another two panel one but with the info panel on the bottom:

```
"height": 2778,
"width": 3735,            
"behavior": [ "bottom", "w-7", "h-7" ]
```


These canvas props give the text panel on the right:
Canvas label is "'You can even become a professor'"
Canvas summary is "News report by the Dutch public broadcasting service NOS on the ..."
Canvas requiredStatement is (none)

This is like a regular "Show the object" Canvas except that the painting anno is a VIDEO
The canvas does not have a duration
The video is on YouTube
It starts at 0, no fragment selector this time


First (and only) painting anno has target  which is the whole canvas - but spatial!
So that's wrong

When you launch the object, as earlier the Annotation label and summary provide the heading and sub:
First painting anno label:  "'You can even become a professor'"
First painting anno summary:  "News report by the Dutch public broadcasting service NOS on t..."

## Canvas 14

...is like Canvas 3

## Canvas 15

...is like Canvas 12

## Canvas 14

...is like Canvas 5


What should have the thumbnail?
The annotations themselves have thumbnails, just regular thumb services from dlcs
But does that make sense to edit in the ME?

older one has row and column as behaviors instead of left, bottom




## Jules comments

We only used html input for the text-only canvasses, in all other cases it should be plain text.

The problems to solve:
 - Where to store the individual image attributions? Can we add them as part of a property to the painting annotation? Or don’t you want those editable in the ME?
 - How to make visible the credits and/or links to other pages on the static site if the tour doesn’t visit all painting annotations? As tooltips for example?

Another way to put it:
In the UX of the mixed media canvas, captions, attributions and links to objects are now combined in a single, linear tour.
This limits the tour bc it visits each and every painting annotation (and is not able to highlight different types of regions: groups of images or fragments)
This limits the attributions/links bc they cannot be accessed directly on the canvas but only through navigating the tour.
Solution: separate the two both in terms of the data model and in the UX.
Attributions as part of a property of the painting annotation, and accessible directly through eg a tooltip or handle together with links to object pages if available
Tour areas by using describing annotations with a body containing the caption
Problem is (I presume) that this will require too much work on the UX side on the static site. Solution is perhaps to keep backward compatibility for existing exhibitions (w/o describing annotations on mixed-media canvasses) and update UX later.
Subsequently there’s also the issue of canvasses with just a single painting annotation, where the label/summary pair is also used for the caption/attribution in the zoom modal. I guess these will need to be separated in a similar way.


## Tom notes

We don't need backward compatibility for the manifests, because we'll convert them with this tool.
We want the new manifests to be something we're confident of creating in the ME.
The issue is the static site generator - but, I'm making an assumption here, it just needs to traverse the IIIF to get the data it needs.
That traversal will be different, but it's not a tricky UI change it's a mapping change, a change in the arrangement of the source data, which is much easier to deal with. Better to concentrate the changes there, where they are easier to deal with, than make compromises in either the manifest model or the ME.

Delft tour steps can:

 - target a region of the canvas
 - target an existing painting annotation
 - both

Why do both? Because any targeted painting anno can have its label and description (and other fields) pulled in to the display for credits/attribution etc.


For the transformer demo, have an additional transformation that adds in a couple of example tour steps that don't follow the current model.

> canvasses with just a single painting annotation, where the label/summary pair is also used for the caption/attribution in the zoom modal. I guess these will need to be separated in a similar way.

The first canvas of Novices is like this:
https://heritage.tudelft.nl/en/exhibitions/novieten

Having a describing anno is enough to make it a tour?
So that goes back to being a label/desc on the painting anno.



# Types

Single object

Catalogue link to object derived from GUID of image service. This information is not present in the source manifest and must be looked up by the static site generator.

1. Can we make it explicit in the manifest? As a seeAlso from the painting annotation OR from the tour step that points to the painting annotation or from... wherever?

Tour

Presence of describing annos makes it a tour

* describing anno might target a painting anno and not provide a TextualBody (typical converted tour step)
* describing anno might target a painting anno and provide a different label and description that overrides the painting annotation (in which case the painting anno label and desc, if it has one, would not be seen in the exhibition)
* describing anno might target a region of the canvas, in which case it should provide a textualBody (e.g., The only woman in the lecture hall)
* describing anno might target a region of the canvas, in which case it should provide a textualBody, AND have the `scope` of one or more painting annotations.