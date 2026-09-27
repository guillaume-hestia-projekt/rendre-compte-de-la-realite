# ADR 0023 — Banc comparatif : Brain contre les mémoires tierces

| | |
|---|---|
| **Statut** | Proposed — 2026-09-23, amendé le 2026-09-24 (décisions 8 et 9). Décision de Guillaume Aubry : « on compare aux deux, mais d'abord le nôtre » ; puis « ce que je veux vérifier, c'est la capacité des mémoires à citer la réalité des faits, sans commettre d'erreur ou d'oubli — et des faits business d'un côté, et des faits juridiques de l'autre ». |
| **Chantier** | Issue #117 (mère), sous-issues #118 (cet ADR et le protocole), #119 (adaptateurs et étage 2), #120 (étage 3, bras homogène), #121 (LoCoMo), #127 (axe juridique, dossier MOREAU), #129 (instrument de présence à deux modes) |
| **Décisions liées** | Protocole du banc « rendre compte de la réalité » v1.1 et amendement 2 (`~/.agents/var/banc-realite/`, page d'atelier `banc-realite-protocole`) ; adjudication de la notation (#106) ; politique Git commune, `AGENTS.md` § « Cycle traçable des chantiers de code », point 7 (l'autorité d'évaluation est distincte du système modifié) |
| **Implémentation** | `scripts/banc_realite/` (adaptateurs, mesures), `tests/banc_realite/` ; sorties sous `~/.agents/var/banc-realite/sorties/comparatif/` ; aucune écriture dans `src/brain` |

## Contexte

Le banc « rendre compte de la réalité » (dossier GreenLoop, 28 pièces, 141 questions dont 28
disputes, trois étages : fidélité, restitution, réponse) a servi depuis le 2026-09-20 à
mesurer Brain contre lui-même : sans mémoire (bras A), dossier entier (B), Brain en
production (C), puis les configurations successives de la chaîne à trois couches. La
référence du 2026-09-23 est la fine hybride 12 + 6 avec douze fenêtres de deux phrases
choisies par cosinus : 84/141 contextes complets à l'étage 2, 75/141 réponses conformes et
26/28 disputes rendues des deux côtés à l'étage 3 (Grok 4.5 servi par Cursor, notation
adjugée), pour ≈ 2 380 tokens d'entrée.

Ce banc ne dit rien de Brain **contre les autres mémoires** : mem0, Letta, et derrière eux
Zep/Graphiti, LangMem, Cognee. Ce sont des mémoires *conversationnelles* — souvenirs d'une
phrase extraits par un modèle, blocs auto-édités par un agent, passages d'archive — dont les
bancs publics (LoCoMo, LongMemEval) rappellent des conversations, pas des dossiers avec
des tableaux et des sources qui se contredisent. Les comparer sur GreenLoop répond à la
question du produit (« quelle mémoire rend compte d'un dossier ? ») ; les comparer sur
leur terrain répond à l'objection prévisible (« vous les avez jugés hors de chez eux »).

## Décision

1. **L'objet comparé est un fournisseur de contexte.** Tout concurrent se met derrière
   la même interface : `ingérer(pièces)` puis `contexte(question, budget) → éléments`.
   Le répondant, la notation et le juge sont identiques pour tous. Letta est en outre
   mesuré comme **agent complet** (le modèle édite sa mémoire et répond lui-même), sur
   une ligne distincte : c'est là qu'est sa valeur, et elle n'est pas séparable du
   répondant.

2. **Deux terrains, dans cet ordre.** GreenLoop d'abord (#119, #120) ; LoCoMo ensuite,
   sur un sous-ensemble (#121). Aucune affirmation publique « Brain contre X » avant que
   les deux terrains soient mesurés.

3. **Premier lot de concurrents** : RAG naïf (la couche brute du banc, borne à battre),
   Brain en production (recherche simple k = 8, CallFrame courante), Brain du banc
   (`hybride_fenetres_g12`), mem0 (vecteurs sur pgvector du cluster privé du banc),
   Letta (mémoire d'archive, puis agent complet). Second lot sur décision : Zep/Graphiti.

4. **Le même instrument.** L'étage 2 (l'or est-il dans le contexte, par forme, « tout
   tient » et « au moins un appui », caractères et tokens) ne coûte aucun appel de
   modèle et se mesure pour tous, avec un balayage de k et de budget par concurrent.
   L'étage 3 reprend la notation adjugée (#106), le juge `must_not_claim` et vingt rejeux
   de stabilité.

5. **Un bras homogène pour l'étage 3, un juge à part.** Un seul modèle sert d'extracteur
   mem0, d'agent Letta et de répondant — et Brain est ré-atomisé par ce même modèle sur
   les 28 pièces, pour ne pas comparer une atomisation Grok 4.5 à une extraction d'un
   autre modèle. **Décision de Guillaume du 2026-09-25 : ce modèle est Grok 4.5, servi par
   Cursor** (`cursor-grok-4.5-high`) — « l'important, c'est de n'avoir qu'un même modèle
   pour tous les tests ». Mistral, pressenti à l'origine, est écarté : son compte n'a aucun
   quota de chat, et Grok 4.5 est déjà l'extracteur de mem0 et de l'atomisation Brain sur
   les deux dossiers, si bien que l'homogénéité est acquise sans réingestion. L'API
   Anthropic reste exclue ; tout appel est précédé d'un comptage à blanc et plafonné.
   **Le juge `must_not_claim` n'est jamais le modèle qui répond** : le répondant étant
   désormais Grok 4.5, le juge change et devient **`gpt-5.6-sol-high` servi par Cursor**,
   le même pour toutes les lignes, y compris Letta agent complet où le répondant fait
   partie du système comparé. La règle « un même modèle pour tous les tests » porte sur les
   systèmes mesurés et le répondant ; le juge est extérieur par construction. La référence
   Grok 4.5 du 23/09 (75/141, juge Grok 4.5 de l'adjudication #106) reste dans son tableau
   avec son juge d'origine nommé ; elle n'est pas mélangée au bras homogène.

6. **Règles de loyauté.** La chaîne Brain a été réglée sur GreenLoop (quatorze disputes
   de réglage, quatorze d'écart, graine 20260922) et les concurrents arrivent tels quels :
   la moitié d'écart est rapportée à part ; chacun reçoit un balayage de k et de budget,
   pas ses défauts ; la comparaison se fait à budget de contexte égal autant qu'à qualité ;
   les résultats sont par forme (single, dispute, aggregate, status, trajectory, unknown),
   jamais une moyenne seule ; le résultat GreenLoop se lit « mémoire d'un dossier ».

7. **L'autorité d'évaluation est distincte des systèmes comparés.** L'or, la notation et le
   juge ne sont pas modifiés par ce chantier ; les adaptateurs vivent dans
   `scripts/banc_realite/` et n'écrivent aucune base d'aire de production. Tout appel de
   modèle nomme son fournisseur dans le journal `appels.jsonl`.

8. **Deux natures de faits, deux modes de présence, les deux toujours publiés.** Un fait
   **business** est rendu si sa *valeur* est juste : une reformulation fidèle est acceptable.
   Un fait **juridique** n'est rendu que si la *lettre* est citée, avec sa pièce : une
   reformulation n'est pas opposable et déplace la portée sans qu'on le voie. L'étage 2
   mesure donc la présence dans deux modes — *verbatim + source* et *valeur + source* — pour
   **tous** les fournisseurs et **les deux** dossiers, et rapporte les deux colonnes côte à
   côte. Jamais le mode valeur seul, jamais le mode verbatim seul.

   Le mode valeur exige la même pièce que le mode verbatim, puis tous les discriminants de
   la citation : nombres comparés en valeur et non en sous-chaîne, dates reconnues sous
   leurs formes équivalentes, noms propres et identifiants en texte normalisé. Une citation
   sans aucun discriminant retombe sur une exigence lexicale — sans quoi n'importe quel
   passage de la bonne pièce tiendrait la clause.

   **Trace du biais, inscrite ici parce qu'elle ne doit pas se perdre** : le mode valeur a
   été décidé *après* avoir vu mem0 obtenir 2/141 au critère verbatim sur GreenLoop. Le mode
   verbatim est donc figé dans son comportement d'origine, et toute mesure déjà publiée
   reste comparable. Un changement d'instrument décidé après avoir vu un score se déclare.

9. **Un banc qui ne mesure pas son propre bruit ne mesure rien.** Toute mesure de présence
   est accompagnée d'un **témoin de brassage** : la même mesure avec les contextes
   délibérément mal appariés (chaque question évaluée contre le contexte d'une autre,
   appariement déterministe et reproductible). La note publiée est un triplet — **signal,
   témoin, écart** — et c'est l'**écart** qui classe, jamais le signal seul.

   Ce que le témoin mesure : la part du score qu'un contexte atteint sans répondre à la
   question, que ce soit par permissivité de l'instrument ou parce que le fournisseur verse
   une large part du corpus. Les deux se confondent dans le chiffre, et le rapport le dit :
   le témoin est une mesure de **précision**, pas un plancher de bruit pur. Mesuré le
   2026-09-24 sur GreenLoop au budget 12 000, il a montré que le 85/141 du RAG naïf — la
   meilleure note brute du banc jusque-là — est atteint à 46/141 par un contexte qui ne
   répond pas à la question, et que Brain banc passe devant sur l'écart (61 contre 39).

   Le témoin **consomme** l'instrument, il ne le corrige pas : les assertions qu'il tient à
   tort sont listées avec le discriminant qui a suffi, et tout resserrement de l'instrument
   est une décision prise sur pièces, jamais un réglage silencieux du score espéré.

## Conséquences

- Le rapport de clôture donne une table par forme, par concurrent, avec le coût
  d'ingestion (appels, tokens, secondes) et le coût de lecture (tokens d'entrée médians).
  Il atterrit sur l'atelier, et la décision durable qu'il porte revient dans cet ADR.
- **Deux dossiers, deux critères** : GreenLoop porte les faits business, MOREAU c/ ATELIER
  RIVIÈRE (#127) les faits juridiques. Chaque dossier est mesuré dans les deux modes — un
  dossier juridique lu au mode valeur et un dossier business lu au mode verbatim sont des
  contrôles, pas des erreurs : l'écart entre les deux modes sur un même dossier est un
  résultat en soi.
- L'or juridique est validé par Guillaume avant toute mesure, clause par clause, sur une
  page d'atelier. Aucun fournisseur mesuré n'écrit l'or.
- Un concurrent qui perd les tableaux ou un côté des disputes sur GreenLoop n'est pas
  « mauvais » : il est hors de son terrain, et le rapport le dit dans ces termes.
- Le témoin « Brain en production » est mesuré à chaque édition du banc : c'est l'écart
  entre ce qui existe dans les aires et ce que la chaîne du banc promet.

## Hors périmètre

Le portage de la chaîne du banc dans `src/brain` (recherche à trois portes, porte
« phrase », couche brute) est un chantier séparé ; ce banc mesure la chaîne telle qu'elle
tourne dans `scripts/banc_realite/`.
