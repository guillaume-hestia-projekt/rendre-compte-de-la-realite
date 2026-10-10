---
title: Rendre compte de la réalité — papier intermédiaire
authors: Hestia. (Guillaume Aubry)
date: 2026-10-10
lang: fr
---

Papier intermédiaire du banc « rendre compte de la réalité », chantiers brain#140, #154, #158. Version anglaise : paper.intermediaire-2026-10-10.en.md. Les ors, les pièces des dossiers et les sorties ne sont pas publiés. Licence : CC BY 4.0.

# Rendre compte de la réalité : ce que le banc a mesuré jusqu'ici

*Papier intermédiaire, 10 octobre 2026. Chantiers brain#140, #154, #158. Auteurs : Guillaume Aubry (or, décisions, critère) et les agents du banc (construction, mesure). Destiné au dépôt public « Ambactos Brain » ; ne contient aucune pièce des dossiers.*

## Résumé

Nous cherchons la meilleure façon de donner à un modèle de langage le contexte qui lui permet de répondre à une question sur un dossier d'entreprise sans inventer, et surtout en décelant ce qu'un dossier a de subtil : les contradictions entre pièces, les versions qui changent, ce qui n'est pas établi. Trois dossiers, trois ors écrits ou validés par un humain, plus de vingt lignes de recherche essayées à budget égal, aucun appel de modèle à la requête. Trois résultats tiennent sur les trois dossiers :

1. **Le RAG seul ne décèle pas les contradictions.** Il tient les faits simples et les citations ; sur les disputes il rend un seul côté (14/28 sur GreenLoop, 0/8 sur Les Granges).
2. **La reconstitution à l'ingestion, c'est-à-dire relire les pièces entité par entité et écrire les faits, les règles, les désaccords et le non établi avec la ligne exacte, ne vaut rien seule, et change tout en composition.** Seule : 37 d'écart sur GreenLoop, 1 sur MOREAU, 15/34 sur Les Granges. Composée avec le RAG : la meilleure ligne sur les trois dossiers.
3. **Le filtre fait tout.** Avec un filtre parfait qui connaît les bonnes pièces, le RAG tient 113 questions sur 141 ; aucun filtre réel construit à partir des questions ne s'en approche. Le seul filtre qui marche vient de la structure du contenu, pas de la question.

Ce dernier point rejoint, par l'expérience, le « composite retrieval » que Jonas Roman décrit en production : filtre par structure, hybride sur l'espace réduit, relations ensuite. La différence est l'origine de la structure : chez lui un schéma posé à la main ; chez nous, une ontologie proposée par le contenu puis décidée en conversation avec l'utilisateur. C'est ce que nous mesurons ensuite.

## 1. Le banc

**L'objet mesuré est l'étage 2** : le contexte rendu au modèle, pas la réponse. Une question est « tenue » quand toute la lettre attendue par l'or (les assertions d'appui, citées mot pour mot avec leur pièce) se trouve dans le contexte rendu, dans un budget fixé en caractères. Le modèle n'est pas appelé à la mesure : la mesure est déterministe et rejouable.

**Le témoin de brassage.** Pour chaque ligne on mesure aussi le même compte avec un contexte tiré pour une autre question. L'écart signal moins témoin est ce qui classe : une ligne qui remplit le contexte de tout le dossier a un signal élevé et un témoin élevé, et ne vaut rien.

**Le budget égal.** Toutes les lignes sont comparées à 12 000 caractères, parfois 24 000. Une ligne mesurée à 24 000 contre une autre à 12 000 n'a rien prouvé ; nous l'avons fait une fois (étage 3 du 27/09) et l'avons retiré.

**L'or ne sert qu'à mesurer.** Il n'entre jamais dans l'ingestion ni dans la recherche. Le plafond « filtre parfait » est le seul instrument qui le lit, et il n'est pas une ligne du comparatif. Le banc n'est pas modifié pour améliorer un score ; une correction du banc (découpeur qui perdait des lignes, 10/10) est rejouée sur toutes les lignes.

**Trois dossiers**, pour ne pas retenir une ligne par chance :

| Dossier | Nature | Pièces | Questions | Or |
|---|---|---:|---:|---|
| GreenLoop | business, prose et registres courts | 28 | 141 | écrit avant les mesures, 28 disputes |
| MOREAU | juridique, courriers et conclusions | ~10 | 43 | écrit avant les mesures |
| Les Granges | tableurs, devis, factures, prévisionnels, lus depuis un Drive sans import, OCR local | 118 | 37 (34 mesurables) | 37 questions proposées depuis les désaccords trouvés, validées et corrigées par Guillaume (une « contradiction » était deux acomptes) |

## 2. Les lignes

| Ligne | Ce qu'elle rend |
|---|---|
| RAG naïf | passages de la couche brute (BM25 + vecteurs), contexte rempli au budget |
| g12 | la chaîne hybride du Brain de production, fenêtres de phrases, volume fixe |
| MRFS seul / g12 puis MRFS | faits extraits énoncé par énoncé (52 à 97 caractères), classés |
| Situations composites | situations reconstituées (type, acteurs, chronologie, ce que chaque partie dit, lignes entières), 1 366 caractères en médiane |
| Reconstitution par entité | faits, règles, désaccords, non établi, par entité et par plage de mois, avec la ligne exacte |
| Désaccords en tête puis RAG | les trois désaccords les plus proches de la question devant, le RAG derrière |
| Filtre (entités, sens, RAG, situations) puis RAG | des pièces choisies, puis le RAG dans ces seules pièces |
| Objets par le sens puis RAG filtré | les objets reconstitués classés par vecteur, puis le RAG filtré sur leurs pièces |

Toutes les lignes de reconstitution font leurs appels de modèle à l'ingestion, une fois (167 appels pour GreenLoop, 309 pour Les Granges), jamais à la requête.

## 3. Les résultats

### GreenLoop, 141 questions, 12 000 caractères (signal / témoin / écart)

| Ligne | Signal | Témoin | Écart | Disputes deux côtés /28 |
|---|---:|---:|---:|---:|
| Plafond : filtre parfait puis RAG | 113 | — | — | 26 |
| g12 puis situations composites | 88 | 26 | 62 | 24 |
| g12 | 84 | 23 | 61 | 24 |
| Désaccords en tête puis g12 | 83 | 22 | 61 | 28 |
| Objets classés puis RAG filtré | 95 | 43 | 52 | 22 |
| Désaccords en tête puis RAG filtré par le sens | 92 | 45 | 47 | 28 |
| RAG naïf | 84 | 44 | 40 | 14 |
| MRFS seul (meilleur budget, 24 000) | 45 | 8 | 37 | 0 |
| Filtre par entités puis RAG | 85 | 48 | 37 | 21 |

### MOREAU, 43 questions (écart au meilleur budget)

| Ligne | Écart verbatim | Budget |
|---|---:|---:|
| RAG naïf | 21 | 12 000 |
| g12 puis situations composites | 18 | 24 000 |
| Situations composites seules | 14 | 24 000 |
| g12 puis MRFS | 13 | 12 000 |
| g12 | 9 | 12 000 |
| MRFS seul | 1 | 12 000 |

Sur ce dossier court (30 000 caractères de pièces pour 52 000 de preuves), le RAG naïf garde le meilleur écart à 12 000 ; à 24 000 il tombe à 14 et la composition passe devant. Les chronologies ne sont rendues par aucune ligne (0/5).

### Les Granges, 34 questions, 12 000 caractères (« tout tient », sans témoin)

| Ligne | Tout tient | ≥ 1 preuve | Contradictions /8 | Montants /14 | Dates /4 | Citations /6 |
|---|---|---|---|---|---|---|
| RAG naïf | 3 | 12 | 0 | 2 | 0 | 1 |
| Reconstitution seule | 15 | 15 | 3 | 9 | 2 | 0 |
| Désaccords en tête puis RAG | 13 | 21 | 5 | 5 | 1 | 1 |
| Désaccords puis RAG filtré | 14 | 22 | 5 | 6 | 1 | 1 |
| Filtre par le sens puis RAG | 8 | 17 | 2 | 5 | 0 | 1 |
| **Objets par le sens puis RAG filtré** | **24** | **26** | **6** | **10** | **4** | 2 |
| RAG composite filtré par l'ontologie v1, sans reconstitution | 5 | 16 | 0 | 4 | 0 | 1 |

Sur un dossier de tableurs, le RAG seul ne tient presque rien : une ligne de tableau sans son en-tête ne dit rien, et le découpage en passages la sépare de ce qui lui donne sens. La reconstitution tient les montants ; la composition tient le reste. Le trou restant : les citations des pièces « en lecture simple » (statuts, bail, bilans), qui ne sont dans aucun objet reconstitué.

## 4. Ce qui est établi

- **Même dessin sur les trois dossiers** : RAG seul en bas, reconstitution seule au milieu, composition en haut ; la forme des pièces (prose, courriers, tableurs) change les chiffres, pas l'ordre.
- **La relation « versions d'un même fait » est ce qui ramène les contradictions.** Mettre les désaccords en tête rend 28/28 disputes sur GreenLoop quel que soit le reste du contexte. Aucune ligne sans reconstitution n'y arrive.
- **Le budget utile est 12 000 à 24 000 caractères.** Au-delà, le témoin monte plus vite que le signal : à 96 000, un contexte tiré pour une autre question tient déjà 25 questions sur 43.
- **Le filtre est le levier**, et il doit venir du contenu. Les filtres construits depuis la question (3 pièces par filtre) écartent les bonnes pièces plus d'une fois sur deux (55 à 67 questions bien filtrées sur 139) et font moins bien que pas de filtre.
- **Les statuts échouent partout**, même avec le filtre parfait (2/21) : la réponse demande de réunir une ligne, une règle et une facture, et rien ne les réunit encore.

## 5. Ce qui n'est pas établi

- **Aucune réponse n'a été jugée sur ces lignes** : tout est étage 2. L'étage 3 du 20–23/09 a montré que la notation « conforme » d'un juge est aveugle sur les disputes ; un protocole de jugement reste à refaire.
- **Les Granges n'ont pas de témoin de brassage** : les comptes sont des « tout tient » bruts.
- **Le coût n'est connu qu'à l'ingestion** (appels, durée) ; aucune comparaison de coût total par dossier.
- **Plus de vingt lignes sur le même or de GreenLoop** : le risque d'en retenir une par chance existe, c'est pourquoi les deux autres dossiers comptent.

## 6. Ce que la reconstitution a appris en se trompant

Les erreurs mesurées sont une partie du résultat ; elles disent où le modèle, laissé seul, invente de la structure.

| Piège | Mesure | Correction |
|---|---|---|
| Numéros de devis lus comme des mois (`2024-41`) | 97 unités sur des périodes fausses | mois 01–12 seulement |
| Une unité par grandeur de tableau | 798 unités, dont 740 minuscules | empaquetage, 304 unités |
| Lignes de tableau résumées au lieu d'être citées | 7 209 lignes jamais citées sur 9 404 | gardées comme blocs de lignes cherchables, pas comme faits |
| Découpeur qui coupait des lignes | 621 lignes perdues sur 888 passages | découpe sans perte, 0 ligne perdue, toutes les lignes rejouées |
| Entités en double (BPI / BPI-R, deux noms d'un même artisan) | 40 entités recensées, 2 fusions décidées par l'utilisateur | ontologie v1, 38 entités actives |

Jonas Roman prévient que les entités générées par le modèle font « du bordel ». Nous l'avons chiffré : 798 unités, 536 groupes de reliquat. La cause commune est qu'aucun schéma n'avait été posé avant.

## 7. Ce qui vient : l'ontologie, par la conversation

Le filtre doit venir du contenu. Chez Jonas Roman, c'est un modèle de données posé à la main par cas d'usage. Nous essayons autre chose : **le système propose l'ontologie du tenant depuis son contenu** (familles de pièces, types d'entités, entités et leurs clés, relations, concepts), puis **l'utilisateur la décide en conversation** : fusions, scissions, types manquants, pièces qui font foi seules. Chaque réponse est une décision horodatée ; rien n'est effacé. L'ontologie est **figée à l'usage** (une version étiquette, filtre, guide) et **évolutive entre versions**, le noyau (types, relations, familles) changeant rarement, les instances souvent. Les versions d'ontologie sont une pratique courante ailleurs ; nous ne la posons pas comme règle, nous la testerons.

Trois lignes de banc séparent trois questions :

| Ligne | Isole |
|---|---|
| RAG composite filtré par l'ontologie, sans reconstitution | ce que vaut l'ontologie seule (la voie de Jonas Roman, aucun appel de modèle après l'étiquetage) |
| Reconstitution guidée par l'ontologie, puis RAG composite filtré | ce que la reconstitution ajoute à l'ontologie |
| Objets par le sens puis RAG filtré (24/34, actuel) | la référence sans ontologie ; l'écart avec la ligne précédente est le prix, ou le gain, de la conversation |

La première est mesurée : 5/34. Sans reconstitution, l'ontologie ne fait que remonter le RAG naïf de 3 à 5 : 14 questions sur 37 ne nomment aucune entité (repli), et 443 passages sur 888, les lignes de tableaux, n'en portent aucune. L'ontologie dit *de quoi* parle une pièce ; seule la reconstitution rattache une ligne à son entité. La deuxième ligne devient la mesure décisive. Règle inchangée : aucun filtre déduit du sens de la question ; seules des clés de l'ontologie trouvées littéralement.

## 8. Reproduire

Code du banc : dépôt `brain`, `scripts/banc_realite/` (PR #155, #159). Les ors, les pièces et les sorties sont hors dépôt et ne se publient pas ; les rapports détaillés par mesure (`RAPPORT-*.md`) seront versés avec ce papier. Toute mesure est rejouable sans appel de modèle à partir des caches d'ingestion ; les plafonds d'appels et d'embeddings de chaque campagne sont consignés dans un journal de décisions.
