
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

Rather than content from media, we're going to give this Canvas a `painting` annotation made of text.

> TODO - what exactly do you do in the ME here?

The values to use are:

English (en):

```
<h1>Introduction</h1>

<p>In the past, new members of the 'Delftste Vrouwelijke Studentenvereniging' (DVSV – Delft student society for women) were called ‘novieten’ (‘novices’) as opposed to ‘feuten’ (with the connotation of ‘foetuses’), the term used for their male counterparts. After the first year, male students were welcomed into a robust community of men. Women, on the other hand, were a minority group. They were ‘politely ignored’ and expected to first prove themselves worthy. In the past, how did women deal with their role as a minority group?</p>
```

Dutch (nl):

```
<h1>Introductie</h1>

<p>Nieuwe leden van de Delftste Vrouwelijke Studentenvereniging (DVSV) werden in het verleden ‘novieten’ genoemd, tegenover de gebruikelijke term ‘feuten’ voor mannen. Maar anders dan hun mannelijke medestudenten, die na het eerste jaar werden opgenomen in een robuuste mannengemeenschap, werden de vrouwen als minderheid ‘beleefd genegeerd’ en geacht zich eerst maar eens te bewijzen. Hoe zijn vrouwen in het verleden omgegaan met hun minderheidsrol?</p>
```

This text is the content of the Canvas - but we also need to add the text that appears in the exhibition as a pop-up (from the "Read more" link), which is supplied as a regular `describing` annotation that targets the whole Canvas, rather than a region as in the previous example. The text to use is:

English (en):

```
<h1>Novices</h1>

<p>In the past, new members of the <em>Delftste Vrouwelijke Studentenvereniging</em> (DVSV – Delft student society for women) were called ‘<em>novieten</em>’ (‘novices’) as opposed to ‘<em>feuten</em>’ (with the connotation of ‘foetuses’), the term used for their male counterparts. After the first year, male students were welcomed into a robust community of men. Women, on the other hand, were a minority group. They were ‘politely ignored’ and expected to first prove themselves worthy.</p><p>The last year about which TU Delft published statistical data was 2018. Even though in that year an equal number of men and women were studying Architecture and Industrial Design, overall, the percentage of female first-year students at TU Delft remained below 30%. How did this develop over time and, in the past, how did women deal with their role as a minority group?</p><p>This digital exhibition starts with a graph that gives an overview of the number and percentage of female first-year students from 1905 to 2018. The year 1905 was chosen as the starting date because that was when the Polytechnic School became the 'Technische Hogeschool' (Institute of Technology) and women were able to study in Delft on a full-time basis. The graph does not show a linear progression, but rather a dynamic process with peaks and troughs. Using the graph, we can see several stories unfolding.</p><p>The first involves the DVSV, established in 1904. Female students came together and were active in this society, largely without an overarching emancipation programme. The speeches given to novices by presidents demonstrate how ‘girl students’ were expected to behave within the university community: ‘Above all, don’t stand out too much,’ was the main motto prior to WWII.</p><p>Out of a relatively high number of women in the pre-war years, the spotlight is turned on Antonia Korvezee who, in 1954, became the first female professor appointed at the Institute of Technology. Korvezee, who trained at the institute and obtained a PhD there, had worked at the famous lab of Marie Curie for some time in the early 1930s, focusing on the then new specialism of radioactivity. Later, as a professor, she used this knowledge to focus attention on that field in the Netherlands.</p><p>The story of the DVSV continues after WWII: Marian Geense wrote a book on the lives of the women who had been DVSV freshers with her in 1956. This exhibition contains a preprint version of the book. Another recent publication is featured. It tells the story of a still existing girls house in the heart of Delft: the Boterbrug, established in 1969. An interview with one of the founders of the house is reprinted here.</p><p>Mart van de Busken’s '<em>Mejuffrouw, Mijne Heren'</em> (Miss and Gentlemen) also dates back to the 1960s. This wonderful film provides a fascinating portrait of the institute at that time. The narrator is one of the ‘rare female students elevated to an icon’, the only ‘miss’ seated among all the ‘gentlemen’ in the lecture hall.</p><p>In the 1970s, both the absolute number and relative percentage of women started to increase. This marked the beginning of a new era in which women’s emancipation played a central role. For the exhibition, recent graduate Noortje Weenink interviewed Anna Vos, the founder of the Women’s Studies discipline within the Architecture Faculty. The interview reveals how female students challenged all kinds of norms that constituted the basis of their own field of study.</p><p>Anna Vos graduated under Franziska Bollerey who, in 1979, was the second female professor appointed at the Institute of Technology, 25 years after Korvezee. In the 1980s, Vos acted in a play during an information day for female students. The aim was to attract more women to enrol in technical studies.</p><p>The exhibition ends with the book '<em>Technische Universiteit, een mannenwereld'</em> (University of Technology, a Man’s World) published by Studium Generale in 1989. In this book, the perspective is reversed, and what it means to be a community of men is provocatively examined alongside what it would take to bring about change.</p><p>Despite the increasing number of 'novices' and the long tradition of female students and researchers at Delft, the university is still identified as a community of men. Diversity and inclusion are given high priority and it’s no longer just about the binary distinction between men and women. Nonetheless, the past experiences of women that are dealt with in this exhibition can serve as reference points for new generations so that – to paraphrase Anna Vos – they don’t have to keep rediscovering the wheel, but can build on the work of their predecessors.</p><p><em>Curated by Sarah Edrisy, Jules Schoonman and Abel Streefland (Academisch Erfgoed team, TU Delft Library). Graph design by Studio Mellegers van Dam.</em></p><p>With thanks to:</p><ul><li>Ted Barendse (Education &amp; Student Affairs)</li><li>Margreet de Boer</li><li>Marjan van den Bos</li><li>Mart van den Busken</li><li><a href="https://mariangeense.nl" rel="noopener noreferrer" target="_blank">Marian Geense</a></li><li>Marcel Janssen</li><li>Frida de Jong</li><li>Elizabeth Poot</li><li>Roland van Roijen (NewMedia Centre)</li><li>Anna Vos</li><li>Noortje Weenink</li><li>Charlotte van Wijk (Faculty of Architecture and the Built Environment)</li><li>Royal Library of the Netherlands</li><li>Atria, institute on gender equality and women's history</li></ul>
```

Dutch (nl):

```
<h1>Novieten</h1>

<p>Nieuwe leden van de Delftste Vrouwelijke Studentenvereniging (DVSV) werden in het verleden ‘novieten’ genoemd, tegenover de gebruikelijke term ‘feuten’ voor mannen. Maar anders dan hun mannelijke medestudenten, die na het eerste jaar werden opgenomen in een robuuste mannengemeenschap, werden de vrouwen ‘beleefd genegeerd’ en geacht zich eerst maar eens te bewijzen.</p><p>Ondanks dat in 2018 – het laatste jaar waarover de TU Delft statistische data heeft gepubliceerd – de studentenpopulaties van de studies Bouwkunde en Industrieel Ontwerpen uit een gelijk aandeel mannen en vrouwen bestaan, is het percentage vrouwelijke eerstejaars studenten aan de TU Delft over het geheel genomen nog altijd niet hoger dan 30%. Hoe heeft dit zich in de loop der tijd ontwikkeld en hoe zijn vrouwen in het verleden omgegaan met hun minderheidsrol?</p><p>Deze digitale tentoonstelling begint met een nieuwe grafiek die een overzicht geeft van het aantal en het percentage vrouwelijke eerstejaars in de periode 1905-2018. Als startdatum is 1905 gekozen omdat in dat jaar de Polytechnische School werd omgevormd tot Technische Hogeschool, waarmee vrouwen voltijds in Delft konden gaan studeren. De grafiek laat geen lineair proces zien, maar een dynamisch proces met pieken en dalen. Aan de hand van de grafiek ontvouwen zich een aantal verhalen.</p><p>Allereerst over de DVSV, opgericht in 1904, waarin vrouwelijke studenten zich verenigden en ontplooiden, grotendeels zonder een overkoepelend emancipatorisch programma. De speeches van presidentes aan de novieten laten zien hoe ‘meisjes-studenten’ zich geacht werden te gedragen binnen de universitaire gemeenschap: "val vooral niet te veel op," was het voornaamste devies vóór de Tweede Wereldoorlog.</p><p>Van het relatief hoge aandeel vrouwen in de vooroorlogse jaren, wordt Antonia Korvezee uitgelicht, die in 1954 werd aangesteld als eerste vrouwelijke hoogleraar van de Technische Hogeschool. Korvezee, in Delft opgeleid en in Delft gepromoveerd, werkte begin jaren dertig enige jaren in Parijs bij madame Curie aan het toen nieuwe specialisme van radioactiviteit. Deze kennis gebruikte ze later als hoogleraar om het vakgebied in Nederland op de kaart te zetten.</p><p>Het verhaal over de DVSV loopt door na de Tweede Wereldoorlog: Marian Geense schreef een boek over de levensloop van de vrouwen uit haar jaarclub uit 1956. Deze tentoonstelling bevat een voorpublicatie. Ook wordt een recente publicatie uitgelicht over een nog steeds bestaand vrouwenhuis in de Delftse binnenstad: de Boterbrug, opgericht in 1969. Een interview met één van de oprichtsters van het huis is hier opnieuw gepubliceerd.</p><p>Tevens uit de jaren zestig stamt de fictieve documentaire ‘Mejuffrouw, Mijne Heren’ van Mart van de Busken. De glorieuze film geeft een geweldig tijdsbeeld van de TH. De verteller is een van de 'zeldzame, tot idool verheven' vrouwelijke studentes, die als enige 'mejuffrouw' plaatsneemt tussen de mannen in de collegezaal.</p><p>Vanaf de jaren zeventig loopt zowel het absolute aantal als het relatieve percentage vrouwen op. Hiermee dient zich een nieuw tijdperk aan waarin vrouwenemancipatie een centrale rol inneemt. Voor de tentoonstelling heeft de recent afgestudeerde Noortje Weenink een interview afgenomen met Anna Vos, de oprichtster van het vak Vrouwenstudies aan de Faculteit Bouwkunde. Het gesprek laat zien hoe vrouwelijke studenten allerlei normen aan de kaak stelden die de basis vormden van hun eigen vakgebied.</p><p>Anna Vos studeerde af bij Franziska Bollerey die in 1979 werd aangesteld als tweede vrouwelijke hoogleraar aan de TH Delft, 25 jaar na Korvezee. In de jaren tachtig speelde zij in een toneelstuk tijdens een van de <em>meisjesinformatiedagen</em>, bedoeld om meer vrouwelijke studenten aan te trekken voor technische studies.</p><p>De tentoonstelling sluit af met het boek <em>Technische Universiteit, een mannenwereld</em>, uitgegeven door Studium Generale in 1989. In het boek is de blik omgedraaid en wordt prikkelend onderzocht wat het betekent om een mannengemeenschap te zijn –&nbsp;en wat ervoor nodig is om deze te veranderen.</p><p>Ondanks het toenemende aantal 'novieten' en de lange geschiedenis van vrouwelijke studenten en onderzoekers in Delft, staat de universiteit tegenwoordig nog steeds te boek als een mannengemeenschap. De thema's diversiteit en inclusiviteit staan hoog op de agenda, waarbij het al lang niet meer gaat om enkel het binaire onderscheid tussen mannen en vrouwen. De eerdere ervaringen van vrouwen die in deze tentoonstelling aan bod komen, kunnen desalniettemin handvaten aanbieden voor nieuwe generaties zodat zij (in de woorden van Anna Vos) niet telkens het wiel opnieuw hoeven uit te vinden maar kunnen voortbouwen op het werk van hun voorgangers.</p><p><em>Samengesteld door Sarah Edrisy, Jules Schoonman en Abel Streefland (Academisch Erfgoed team, TU Delft Library). Opmaak grafiek door Studio Mellegers van Dam.</em></p><p>Met dank aan:</p><ul><li>Ted Barendse (Education &amp; Student Affairs)</li><li>Margreet de Boer</li><li>Marjan van den Bos</li><li>Mart van den Busken</li><li><a href="https://mariangeense.nl" rel="noopener noreferrer" target="_blank">Marian Geense</a></li><li>Marcel Janssen</li><li>Frida de Jong</li><li>Elizabeth Poot</li><li>Roland van Roijen (NewMedia Centre)</li><li>Anna Vos</li><li>Noortje Weenink</li><li>Charlotte van Wijk (Faculteit Bouwkunde)</li><li>Koninklijke Bibliotheek</li><li>Atria, kennisinstituut voor emancipatie en vrouwengeschiedenis</li></ul>
```

The exhibition viewer knows what to do with this canvas, driven by the `info` value of the `behavior` property.

## Canvas 3: First-year students at the Delft Institute of Technology and TU Delft in the period 1905-2018

This canvas introduces another kind of exhibition special rendering. Whereas the previous canvas was a text-only info panel, this next canvas is a combination of info panel and multimedia content / tour steps in the same Canvas. The `behavior` property configures where the text sits in relation to the media, as well as the size:

```
right
w-12
h-8
```

Create a new canvas from an image service, as in the first example. The image service to use is:

```
https://dlc.services/iiif-img/7/21/4d8776d3-31a9-bf36-22ad-536c39f6ba5d
```

This time there's no crop - that's all you need to do for the image content itself, it automatically targets the whole Canvas. 

However, we will as before give this painting annotation itself a `label` and a `summary`:

The label is:

English (en):

```
First-year students at the Delft Institute of Technology and TU Delft in the period 1905-2018
```

Dutch (nl):

```
Eerstejaarsstudenten van de TH en TU Delft in de periode 1905-2018
```

And the summary is:

English (en):

```
Sources: Delft Institute of Technology Yearbooks and reports, TU Delft Statistical Yearbooks and OSIRIS
```

Dutch (nl):

```
Bronnen: Jaarboeken en -verslagen TH Delft, Statistisch jaarboeken TU Delft en OSIRIS
```

The Canvas also needs a label, which can be the same as the annotation label (we will vary these in future for different effects).

English (en):

```
First-year students at the Delft Institute of Technology and TU Delft in the period 1905-2018
```

Dutch (nl):

```
Eerstejaarsstudenten van de TH en TU Delft in de periode 1905-2018
```

For this panel, the Canvas also gets a `summary` property - it's this that will provide the text panel. Note that here we don't have to provide HTML, we can provide several string values (as separate values) and leave the formatting up to the exhibition viewer:

English (en):

```
This graph shows the absolute number of first-year students, the distribution of men and women, and the percentage of women. It was only possible for women to follow a full-time technical study at Delft from 1905.

A striking aspect of the graph is that the percentage of women before WWII was higher than in the period that followed. The percentage only increases to more than 11% – the highest pre-war percentage – in 1983.

Over the course of time, the definition of first-year students changed. Up until 1982, no statistical distinction was made between different types of first-year students. From 1982, the numbers given for first-year students include 'internal switchers' (students who changed to a different study) because these figures were best in line with earlier data. The introduction of the bachelor’s-master’s system in 2002 also had an impact on the calculation method which probably explains the ‘dip' the graph shows in that year.
```

Dutch (nl):

```
Deze grafiek toont het absolute aantal eerstejaars studenten, de verdeling tussen man en vrouw en het percentage vrouwen. Pas vanaf 1905 is het voor vrouwen mogelijk om in Delft een volledige technische studie te volgen.

Opvallend aan de grafiek is dat het percentage vrouwen vóór de Tweede Wereldoorlog hoger is dan in de periode erna. Pas in 1983 stijgt het percentage weer uit boven de 11%, het maximum uit de vooroorlogse jaren.

In de loop der tijd is de definitie van eerstejaars studenten veranderd. Tot 1982 wordt er in de statistieken geen onderscheid gemaakt tussen verschillende soorten eerstejaars. Vanaf 1982 zijn de aantallen eerstejaars gebruikt inclusief 'interne omzwaaiers' (studenten die van studie wisselen), omdat deze het best overeenkwamen met de eerdere gegevens. Ook de invoering van de bachelor-masterstructuur in 2002 heeft impact gehad op de wijze van tellen, wat waarschijnlijk de 'dip' in de grafiek verklaart rond dat jaar.
```

The info panel also has a footer, which is provided by the `requiredStatement` property of the Canvas. Again we're going to repeat something used elsewhere but later we can vary these to demonstrate how flexible the model is.

English (en):

```
Sources: Delft Institute of Technology Yearbooks and reports, TU Delft Statistical Yearbooks and OSIRIS
```

Dutch (nl):

```
Bronnen: Jaarboeken en -verslagen TH Delft, Statistisch jaarboeken TU Delft en OSIRIS
```

Now you need to create a tour. Like the first example this will be a pointer to the whole image as the first step, and a detail of the canvas as the second.

For the first step all you need to do is create an annotation with motivation `describing` that points at the single media (painting) annotation. The exhbition viewer picks up that annotation's label and summary and uses them.

For the second step, you need to draw attention to the bottom-left region of the canvas. Create a describing annotation whose target is a square-ish box that captures the bottom-left of the graph, up to around 1945.

This tour step needs the following text bodies for the annotation:

English (en):

```
<h1>Before the Second World War</h1>

<p>A striking aspect of the graph is that the percentage of women before WWII was higher than in the period that followed. The percentage only increases to more than 11% – the highest pre-war percentage – in 1983.</p>
```

Dutch (nl):

```
<h1>Voor de Tweede Wereldoorlog</h1>

<p>Opvallend aan de grafiek is dat het percentage vrouwen vóór de Tweede Wereldoorlog hoger is dan in de periode erna. Pas in 1983 stijgt het percentage weer uit boven de 11%, het maximum uit de vooroorlogse jaren.</p>
```
 
The last step is to add a `thumbnail` to the Canvas; again, we have an existing one:

```
https://dlc.services/thumbs/7/21/4d8776d3-31a9-bf36-22ad-536c39f6ba5d
```




Notes - 

For the synthetic one we can build it up bit by bit

from image services
from picking whole canvases (already with their thumbnails)











