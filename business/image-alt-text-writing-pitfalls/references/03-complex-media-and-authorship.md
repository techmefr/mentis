# image-alt-text-writing-pitfalls §3 — Complex images, other media and authorship

## 3.1 Charts and other complex images
1. **A long alt attribute is the wrong place for a chart.** The "five mistakes" post sends complex
   graphics such as research charts to the W3C tutorial on complex images, and notes the old longdesc
   method is no longer valid (mistake 4).
2. **Put the information as text beside the image** (a data table, a summary paragraph) and keep the alt
   text short. The Microsoft style guide says to link to a separate page with more details for complex
   elements. The W3C complex images page confirms the pattern: a two-part alternative, a short description that
   names the image and says where the long one is, and a long description in text, reached by an adjacent link
   or sitting next to the image. RGAA criterion 1.6 asks for such a detailed description where one is
   needed, and still lists the old longdesc attribute among accepted techniques although the A11Y post calls
   it no longer valid: prefer the adjacent text or link.
3. **A reader should get the whole story from either the picture or the written description** (Microsoft
   style guide, "Images, image maps, and multimedia").

## 3.2 Audio, video, animation and image maps
1. **Give brief, accurate alt text for graphics, audio, video, animations, GIFs and pictures of text**
   (Microsoft style guide).
2. **Provide captions, transcripts or descriptions for audio and video** (same page).
3. **Provide text links in addition to image maps** (same page).
4. **A picture of text belongs in the page as text** where the presentation can be done in real text; RGAA
   criterion 1.8 and the W3C images-of-text page both say to prefer styled text. The alt text of an image of
   text that stays then carries the text.

## 3.3 A human who looked
1. **Alt text needs a person's input to be effective** (A11Y Project, automation post).
2. **Automated descriptions are literal and often wrong**: the post lists multiple subjects, high detail,
   abstract illustrations, foreign languages, obscure subjects and algorithmic bias as the weak spots. Its
   example turns a family holiday photo into "4 people outdoors", which is true and says nothing of why the
   photo is there.
3. **Why the image is included is the part only the author knows**, and it matters most for images used as
   metaphor (same post).
4. **Products that promise to add accurate alt text automatically**, as an overlay or at creation time,
   cannot deliver it, according to the same post, which points to a court filing as evidence. Own guidance:
   treat such a promise as an unverified claim.
5. **Own guidance:** use generated text only as a draft that a person corrects, and say so in the workflow.
6. **Training and review help more than tools**: make a check for concise, accurate alt text part of
   editorial and review steps (same post).
7. **Platforms offer an alt field on images**, and the automatic descriptions some use when it is empty are
   described as almost always insufficient. Memes need the joke or reference described, not only the pixels
   (same post).
