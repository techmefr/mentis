---
name: seo
description: Use quand on code ou revoit une page/app front destinée à être indexée (Nuxt/React SSR ou statique), checklist SEO technique : meta tags, sémantique HTML, structured data, performance Core Web Vitals, sitemap/robots. Pas de vécu de production Xefi dédié SEO à ce stade, sourcé sur les guidelines établies du marché (Google Search Central, web.dev).
---

# seo

Étape 6 du pipeline (`WORKFLOW.md`), en complément de `vue-nuxt-vuetify-conventions`/
`react-nextjs-conventions` : s'applique uniquement aux pages destinées à être
indexées par un moteur de recherche (pas aux back-offices, aux apps internes
authentifiées, ni aux dashboards).

## Quand
Dès qu'une page front est publique et doit être trouvable via recherche : 
pendant `code` (6) ou en review (`review`, 8) si le diff touche des pages
publiques.

## Étapes

### 1. Meta et indexation : la base non négociable
1. Chaque page a un `<title>` unique et une `<meta name="description">`
   propre (pas de doublon copié-collé entre pages, pas de valeur par défaut
   générique laissée en prod).
2. Balise `canonical` posée dès qu'une même page est accessible par plusieurs
   URLs (paramètres de tri/filtre, trailing slash, http/https).
3. `robots.txt` et balises `meta robots`/`noindex` cohérents avec l'intention
   réelle : une page volontairement exclue de l'index le dit explicitement,
   jamais par oubli d'un `noindex` qui traîne sur une page qu'on veut indexer.
4. Open Graph / Twitter Card renseignés sur les pages partageables (titre,
   description, image) : sinon le partage social affiche un aperçu vide ou
   générique.

### 2. Sémantique HTML : ce qu'un crawler et un lecteur d'écran lisent pareil
1. Une seule balise `<h1>` par page, hiérarchie `h1 > h2 > h3` sans saut de
   niveau arbitraire pour un effet visuel (le visuel se gère en CSS, pas en
   changeant la balise).
2. Contenu textuel réel dans le HTML servi (SSR/SSG), jamais uniquement injecté
   côté client après hydratation pour le contenu qui doit être indexé : un
   crawler qui n'exécute pas le JS ne voit rien.
3. Liens internes en vraies balises `<a href>` (navigables, crawlables),
   jamais un `<div onClick>` qui simule un lien.
4. Attribut `alt` descriptif sur les images porteuses de sens, vide (`alt=""`)
   sur les images purement décoratives : jamais absent.

### 3. Performance : Core Web Vitals
1. LCP (Largest Contentful Paint) : l'image/le bloc principal above-the-fold
   n'attend pas un chargement JS lourd ni un fetch client-side évitable ;
   `loading="eager"`/`fetchpriority="high"` sur l'image LCP, `lazy` sur le
   reste.
2. CLS (Cumulative Layout Shift) : dimensions explicites (`width`/`height` ou
   `aspect-ratio`) sur images/vidéos/embeds pour réserver l'espace avant
   chargement : jamais de contenu qui pousse la mise en page après coup.
3. INP (Interaction to Next Paint) : pas de tâche JS bloquante longue sur les
   interactions principales (clic, saisie) : voir les conventions perf déjà
   posées dans `vue-nuxt-vuetify-conventions`/`react-nextjs-conventions`.

### 4. Structured data et découverte
1. JSON-LD (`schema.org`) posé sur les types de contenu qui en bénéficient
   (article, produit, FAQ, breadcrumb) quand le besoin métier le justifie : 
   pas systématiquement par réflexe sur tout type de page.
2. `sitemap.xml` généré (pas maintenu à la main) et référencé dans
   `robots.txt`, mis à jour à chaque déploiement de contenu nouveau.
3. URLs lisibles et stables (slugs, pas d'ID technique exposé sans raison) : 
   un changement d'URL casse l'historique d'indexation, donc redirection 301
   obligatoire si une URL publique change.

## Sortie / checkpoint
Les quatre sections passées en revue sur le diff touché ; pour un audit plus
large d'un site déjà en prod (pas seulement le diff en cours), voir l'agent
`seo-auditor`.

## Garde-fous
- Ne s'applique jamais aux pages non publiques (auth, back-office, dashboard
  interne) : ne pas imposer cette checklist hors de son périmètre.
- Pas de sur-ingénierie JSON-LD : seulement les types de contenu qui en tirent
  un bénéfice réel (page produit, article), pas un ajout systématique.
- Cette brique n'a pas encore de vécu de production Xefi dédié : à confronter
  au premier vrai audit SEO réel, pas à traiter comme doctrine éprouvée.

## Origine
Sourcé sur les guidelines établies du marché : Google Search Central
(indexation, structured data, Core Web Vitals), web.dev (LCP/CLS/INP,
sémantique HTML, images). Mécanismes réécrits en checklist actionnable, pas de
texte copié. Recherche de marché, pas de retour de production interne à ce
stade.
