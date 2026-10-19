# French: the same mechanisms, in French

> Reference for `business/ai-prose-tells`. Read it when the text under audit is in French. It is written in
> French terms, not translated from the English lists: some English tells have no French equivalent and
> some French tells have no English one.

The method is unchanged: judge by families and clusters, add no fact, keep the user's own voice first.
What changes is the vocabulary and the conventions. Quoted phrases below are examples of a mechanism, not
a ban list; a word list ages, the mechanism does not.

## 1. The families, with French instances

1. **Hollow vocabulary.** "véritable", "incontournable", "innovant", "performant", "puissant", "robuste",
   "optimal", "à la pointe", "de bout en bout" used as approval. Same test: can a measure or a name
   replace it?
2. **Scope inflation.** "un tournant majeur", "une avancée significative", "une nouvelle ère" for a
   renamed option. Does the sentence match the size of the diff?
3. **Stock framing.** "dans un monde où", "à l'ère de", "dans le paysage actuel", "force est de constater
   que", "il est essentiel de souligner". The frame announces importance instead of giving the fact.
4. **Administrative filler.** "il convient de", "il est important de noter que", "il s'agit de", "afin de
   permettre de", "dans le cadre de", "au niveau de". Delete the phrase; if the sentence parses and means
   the same, it was padding.
5. **Positioning clichés.** "au cœur de", "s'inscrit dans une démarche de", "met l'accent sur", "offre une
   expérience", "répond aux enjeux de". Say what the thing does.
6. **Mechanical connectors.** "en outre", "par ailleurs", "de plus", "ainsi", "de surcroît" opening
   consecutive sentences. Keep a connector only when it names a real relation.
7. **Negative parallelism.** "ce n'est pas seulement X, c'est aussi Y", "non seulement ... mais
   également", "il ne s'agit pas de X mais de Y". Keep it when the negation corrects a belief the reader
   actually holds.
8. **Actorless passive and nominalisation.** "la mise en œuvre de la validation est effectuée", "une prise
   en compte des retours". French lets a noun carry the verb; name the actor and use the verb: "l'API
   valide la requête", "l'équipe a repris les retours".
9. **Chatbot closure.** "n'hésitez pas à", "j'espère que cela vous aide", "je reste à votre disposition"
   in a README or an MR description. A conversation formula in a document.
10. **Rule of three and aphorisms.** "rapide, fiable et évolutif"; a closing maxim built to be quoted.
11. **Inanimate subject.** "les données nous disent", "l'architecture embrasse le changement".
12. **Production narrative.** "après plusieurs itérations", "j'ai ensuite refactoré", "généré avec" in
    reader text: remove, the reader gets the result.

## 2. French-specific points

- **Politeness is not a tell.** "Vous", "Madame, Monsieur", "cordialement" and the formal register of a
  letter are conventions. Flag only formulas that carry no content in a document that is not a letter.
- **Typography is not a tell.** Guillemets « », a non-breaking space before `:` `;` `!` `?`, the typographic
  apostrophe and the ellipsis character are correct French typesetting. Missing them in a French text is
  a typography defect (`business/ux-writing` §5), not evidence of generation. A straight apostrophe in a
  commit message is a technical constraint.
- **The dash.** The rule from `02-more-tells.md` (family 35) applies unchanged: avoid by default, follow the
  user's sample. French dialogue and enumerations use dashes by convention; those are untouched.
- **Anglicisms and calques.** "adresser un problème", "supporter une fonctionnalité", "réaliser que"
  (meaning "se rendre compte") are mistranslation, not machine tells; fix them only when the text is
  yours to edit, and never as part of the tell audit.

## 3. Do not flag (French)

- **Legal, contractual and regulatory text**, where "il convient de", "en outre", "par ailleurs" and
  passive constructions are conventional.
- **Formal letters and official notices.**
- **Changelog and README conventions**: "Ajouté", "Modifié", "Corrigé", "Installation", "Utilisation".
- **Technical terms** that look like hollow vocabulary ("robuste" in statistics, "optimal" in
  optimisation, "performant" when a benchmark sits next to it).
- **Quoted text**, error messages, output, code.
- **Non-native or regional French.** Different from machine-made; do not correct a person.

## 4. Positive requirement

The same as for English (`01-tells.md` §5): every French document leaving this filter says what it is, for
whom, and carries one checkable detail. The filter's output is a text that is shorter and more specific, not
one with different synonyms.
