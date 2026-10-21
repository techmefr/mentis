# image-alt-text-writing-pitfalls §1 — Attribute and the three kinds of image

The first decision is not what to write but whether to write anything.

## 1.1 The attribute is not the text
1. **The alt attribute is markup; alt text is the description between its quotes.** Every image needs the
   attribute, not every image needs text (A11Y Project, "five mistakes" post, mistake 1, Daniel Sage).
2. **A decorative image gets an empty attribute, never a missing one.** The automation post (Eric Bailey)
   says some screen readers fall back to image recognition when no text is provided, and that this
   fallback is unreliable.
3. **Own guidance:** in a social tool or a CMS the same split applies. An empty field is a decision to
   record, not an omission to fix.
4. **The W3C images tutorial agrees on the empty attribute.** It says a null alt value lets assistive software
   skip a decorative image, that leaving the attribute out is not an option because some screen readers then
   announce the file name, and that deciding between decorative and informative is a judgment only the author
   can make from the reason the image is on the page (W3C WAI, decorative and informative images pages).

## 1.2 Three kinds
1. **Decorative**: its only value is aesthetic; if it were removed the page would still make sense. Banners
   without text are the example. Empty attribute.
2. **Informative**: it adds context to the content, such as graphs, diagrams, poll results and product
   screenshots. Describe what it conveys (same post).
3. **Active**: it acts as a link or button, for signing up, downloading or uploading. Describe the action,
   not the picture, and avoid "click here"; the post's examples are "Sign up for a Twitter account" and "Go
   to the account page". The W3C functional images page says the same: the alternative states the action the
   image starts, "print this page" and not "printer".
4. **The standards split images a little differently.** The W3C tutorial names decorative, informative,
   functional, complex and images of text; the French RGAA criteria 1.1 to 1.3 ask that an informative image
   has a relevant alternative and that a decorative one is ignored by assistive technology. Our three kinds
   (decorative, informative, active) fold complex and text images into informative and keep functional as
   active, which is a simplification and not the standards' wording. For a conformance claim cite the standard.
5. **An icon next to a visible label can be decorative.** The "Using alt text properly" post (Susan
   Robertson) gives a phone icon inside a "contact" link: the link text already says it, so the attribute
   is empty.

## 1.3 Same image, different role
1. **The same logo can need different text in different places.** A header logo that links home reads
   usefully as the company name plus its destination; a footer logo placed beside the company name written
   out gets an empty attribute so the name is not announced twice ("Using alt text properly"). The W3C pages
   make both cases explicit: an image inside a link whose text already says it can take an empty value, and an
   image that is the whole link should say where the link goes ("homepage" and not "logo").
2. **So decide per placement, not per file.** A shared asset library cannot store the alt text with the
   file. Own guidance.
