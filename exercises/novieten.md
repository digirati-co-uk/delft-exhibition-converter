
# Novieten (Novices)

This task creates a new Exhibition that is a reproduction of an existing one (to make comparison easier).

It also exercises creating an exhibition in both English and Dutch, as the single manifest drives both versions.

Here's the live version:

[English](https://heritage.tudelft.nl/en/exhibitions/novieten) | [Dutch](https://heritage.tudelft.nl/nl/exhibitions/novieten)

This exercise provides the text and the source IIIF resources to make the exhibition.

# Steps

Create a new Manifest and give it a `label` with two language values:

English (en):

```
Novices
```

Dutch (nl):

```
Novieten
```

## Canvas 1: The only woman in the lecture hall

Create a Canvas from an Image Service.

The Image Service to use is:

```
https://dlc.services/iiif-img/7/21/e16c7a6b-9672-d551-70d7-08c88609efb1
```

This image is in landscape format. However, you want a **crop** - use the full height of the image, but make it square.

You still want the _cropped_ image to fill the Canvas, so you may need to adjust the canvas dimensions to fit the cropped content.

The label to give the Canvas is:

English (en):

```
The only woman in the lecture hal
```

Dutch (nl):

```
De enige vrouw in de collegezaal
```

You're now going to use a special feature of Delft exhibitions that is not something you usually do in a general purpose manifest: you're going to give this piece of media its own `label` and `summary` properties. 

> _Technically speaking, you are going to set the `label` and `summary` properties of the `painting` annotation itself - rather than the Canvas. This is so the media can be used a tour step._

The `label` of the annotation is:

English (en):

```
The only woman in the lecture hall (Orientation Week 1965)
```

Dutch (nl):

```
De enige vrouw in de collegezaal (Introductieweek 1965)
```

And the `summary` is:

English (en):

```
TU Delft Library, Special Collections
```

Dutch (nl):

```
TU Delft Library, Bijzondere Collecties
```

> _In future this model might use `requiredStatement` for the latter - but the summary part of the tour step isn't always just an attribution._

We also need to set the custom `behavior` properties that guide the layout of the exhibition. For this canvas, we have two values to set:

```
w-8
h-8
```

...which makes the display panel square in the web page.

This panel is going to be a **Tour** - clicking the image will launch a tour. Tour steps are a sequence of annotations with the `motivation` property of `describing`. Tour steps can target the media on the canvas - the `painting` annotation(s) - or they can target arbitrary regions of the canvas. The latter is the more normal mode for a descriptive annotation, but the former is a handy way of explicitly tying tour steps to particular media on the canvas.

The first step of the tour is the whole image, so for this step we just create a `describing` annotation that targets (points to) the media we just added. The Manifest Editor will have created an entry in the media list that uses the label we gave it - "The only woman in the lecture hall (Orientation Week 1965)". It might also say "Image from Image Service".

> _The Manifest Editor uses assigned `label` properties for painting annotations in the UI - this is useful when building up exhibitions, guided viewing etc. Most normal manifests won't have labels for these `painting` annotations, so the Manifest Editor uses a summary of the type - where "Image from Image Service" or "Image with Image Service" are the most common, and just "Image" would be an image without an accompanying Image service._

> TODO: show exactly how to make this describing anno

The second (and last) step of the tour is a more conventional `describing` annotation - a step that focuses on a particular region of the canvas. 

Create a new `describing` annotation with a box target on the canvas, showing the only woman present (she's on the right hand side, about halfway down). Don't draw the box too tightly around her face, the exhibition will zoom in to this region. You want the box to be roughly square, but it doesn't have to be exact.

Now we need to provide a text body for this tour step. As this is a completely normal `describing` annotation we give it a standard textual body. In fact, we give it two bodies, one English and one Dutch. We'll need to specify the language for each, and also that the textual bodies are HTML. Here are the values:

English (en):

```
<h1>The only woman in the lecture hall (Orientation Week 1965)</h1>

<p>TU Delft Library, Special Collections</p>
```

Dutch (nl):

```
<h1>De enige vrouw in de collegezaal (Introductieweek 1965)</h1>

<p>TU Delft Library, Bijzondere Collecties</p
```

> _Again, this tour step looks slightly odd; we're matching the appearance of the other tour step where the heading and "body" are derived from the painting annotation label and summary. The other exercise, which builds an exhibition from scratch rather than re-creates a "legacy" exhibition, will show more flexible use of these properties._

The last step is to give the Canvas a thumbnail. If we go to edit the `thumbnail` property of the Canvas, we can see that we could get the Manifest Editor to generate one automatically from the existing image content. But in this case we know that we have a better thumbnail - so we paste in this image service:

```
https://dlc.services/thumbs/7/21/e16c7a6b-9672-d551-70d7-08c88609efb1
```

> _The Manifest Editor analyses this and creates a Thumbnail (as "Image from Image Service", or "Image with Image Service")._

## Canvas 2: Introduction

The next Canvas is a special _info_ text-only Canvas. For this we need to create an **empty** Canvas. Give it a matching height and width of `1000` (although it's not critical what the dimensions are).

Give the Canvas the following `behavior` property values:

```
info
w-4
h-4
```




