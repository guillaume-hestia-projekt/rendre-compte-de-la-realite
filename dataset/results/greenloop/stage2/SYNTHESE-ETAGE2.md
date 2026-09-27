# Synthèse — banc comparatif, étage 2 (2026-09-23, issue #117 / #119, PR #123)

Même instrument que le banc (présence de l'or dans le contexte rendu, `restitution.compute_verdict`), 141
questions, 28 disputes (14 réglage / 14 écart). Aucun appel de modèle. Balayage k ∈ {4, 8, 12, 16, 20} ×
budget de rendu ∈ {4 000, 8 000, 12 000} caractères (les éléments du rang le plus bas sont retirés jusqu'à
tenir sous le budget, comme la CallFrame de Brain). Tokens = caractères / 4.

mem0 et Letta ne sont pas encore dans la table : mem0 attend un quota de chat Mistral (429,
`x-ratelimit-limit-req-minute: 0`) ; Letta attend un serveur (image Docker, disque à 4 Go).

## Table réduite (meilleur k par budget, et k = 8 pour Brain prod = réglage des aires)

| fournisseur | k | budget | tout tient /141 | ≥ 1 /141 | disputes 2 côtés /28 (réglage · écart) | car. méd. | tok. méd. |
|---|---|---|---|---|---|---|---|
| Brain prod (k = 8, ce que les aires ont) | 8 | 12 000 | 39 | 80 | 1 (0 · 1) | 2 795 | 699 |
| Brain prod, meilleur k | 20 | 12 000 | 44 | 96 | 3 (1 · 2) | 6 601 | 1 650 |
| RAG naïf | 16 | 4 000 | 52 | 91 | 0 | 3 392 | 848 |
| RAG naïf | 8 | 8 000 | 68 | 109 | 6 (4 · 2) | 7 491 | 1 873 |
| RAG naïf | 12 | 12 000 | **85** | 121 | 14 (8 · 6) | 11 458 | 2 865 |
| RAG naïf | 8 | 12 000 | 81 | 115 | 15 (8 · 7) | 8 796 | 2 199 |
| Brain banc (`hybride_fenetres_g12`) | figé | 4 000 | 31 | 87 | 3 (3 · 0) | 3 834 | 958 |
| Brain banc | figé | 8 000 | 79 | 125 | **24** (13 · 11) | 7 835 | 1 959 |
| Brain banc | figé | 12 000 | **84** | **128** | **24** (13 · 11) | 9 417 | 2 354 |

## Lecture

- **Brain prod est loin derrière tout le monde** : 39/141 « tout tient » et 1/28 dispute à k = 8, et k = 20
  n'y change presque rien (44, 3/28). C'est l'écart entre ce que les aires servent aujourd'hui et ce que la
  chaîne du banc promet — l'argument du portage. (Mesure rejouée après la revue Codex de #123 par le vrai
  chemin `run_search` → `compile_call_frame` : le chercheur « témoin » du banc donnait 28 · 0 — la requête
  structurée et le rendu de la CallFrame valent onze questions ; la ligne reste à 45 points de Brain banc.)
- **À budget 12 000, RAG naïf et Brain banc font jeu égal sur « tout tient » (85 contre 84)** ; Brain banc
  l'emporte sur « au moins un appui » (128 contre 121), sur les **disputes (24 contre 14)**, et coûte **18 % de
  moins** (9 417 car. contre 11 458). À budget 8 000 l'écart s'ouvre : 79 contre 68, et 24 contre 6 disputes.
  (Ligne RAG rejouée deux fois après les revues Codex : requête structurée du banc au lieu de la question nue
  — 84 → 85, 120 → 121, disputes inchangées — puis étiquettes de source rendues et comptées dans le budget
  — rien à 12 000, un point de moins à 8 000 : la brute est insensible à la forme de la requête, et les
  sources coûtent ≈ 40 caractères.)
- **Le RAG est instable en k** (disputes 15 → 14 → 5 → 7 de k = 8 à 20) : la fusion RRF change de rang avec k
  (piège connu, #110) ; Brain banc, lui, ne dépend que du budget.
- **À budget 4 000, Brain banc perd** (31 contre 50) : la coupe retire d'abord les fenêtres de phrases (rangées
  après la fine), et ce qui reste vaut Brain prod. Un ordre de rendu par score plutôt que par porte est un
  levier à mesurer si un budget serré devient un cas réel.
- Ces chiffres reproduisent les mesures antérieures du banc (Brain banc 84/141 · 24/28 = #114 ; Brain prod
  28/141 · 0/28 = « fine simple » de #109) : l'instrument comparatif est cohérent avec l'instrument d'origine.

Fichiers : `etage2-{rag_naif,brain_prod,brain_banc}.json` (par question, par k, par budget),
`RAPPORT-COMPARATIF-ETAGE2.md` (tables complètes générées).
