# ADR 0024 — Portage de la chaîne du banc en production : trois portes, et le passage entier quand la lettre fait foi

| | |
|---|---|
| **Statut** | **Accepted — 2026-09-27**, validé par Guillaume Aubry (« je valide ») après lecture des deux dossiers aux trois étages, de la grille à unités et budgets égaux et du témoin. Proposed le 2026-09-26. |
| **Chantier** | Issue #135 (mère) ; sous-issues à ouvrir : ADR (celle-ci), couche brute en production, recherche à trois portes, rendu du passage, preuve par le banc |
| **Décisions liées** | ADR 0023 (banc comparatif, décisions 4, 6, 8, 9 ; « hors périmètre : le portage ») ; ADR 0021 (cycle traçable, §7 : l'autorité d'évaluation est distincte du système modifié) ; adjudication de la notation (#106) |
| **Implémentation** | `src/brain` (recherche, `compile_call_frame`, ingestion) ; le banc `scripts/banc_realite/` reste l'instrument, jamais modifié par ce chantier pour améliorer son propre score |

## Contexte — ce que le banc a établi

Deux dossiers, trois étages, unités et budgets égaux pour tous, témoin de brassage recalculé à
chaque budget (atelier `banc-moreau-etage2`, v7 ; #127, #120).

1. **Brain en production est le dernier ou l'avant-dernier partout.** Le chemin réel
   (`run_search` k = 8 → `compile_call_frame`) rend 39/141 sur GreenLoop (écart net 32), 1/43 sur
   MOREAU, 25 | 3 sur 50 à l'étage 3 juridique. L'écart entre ce qui tourne et ce que le banc sait
   faire est plus grand que l'écart entre Brain et n'importe quel concurrent mesuré.
2. **La chaîne du banc `hybride_fenetres_g12`** — recherche hybride 12 + 6 sur les atomes, plus
   douze fenêtres de deux phrases choisies par similarité dans la couche brute — a le meilleur
   écart net du banc sur le business à tous les budgets : 56 à 61 sur 141, témoin plat à 23, pour
   9 417 caractères rendus là où le RAG naïf en rend 23 465 pour un écart net de 31 à 39. Lui donner
   plus d'unités (24, 36, 48) ne l'améliore jamais en net au-dessus de la g12 et la dégrade
   nettement sous 12 000 caractères : les viviers larges réordonnent la fusion et la coupe au budget
   garde les mauvais éléments.
3. **Sur le juridique, la même chaîne plafonne à 12/43 quel que soit le nombre d'unités et le
   volume rendu** (6 128 à 21 330 caractères). Cause vérifiée dans le code : elle ne rend que des
   atomes (12 caractères de médiane) et des fenêtres de deux phrases ; 26 des 42 citations de l'or
   tiennent dans une fenêtre, jamais une clause de 590 caractères. Le RAG, qui rend la pièce, tient
   42 — mais par volume : à 32 000 il rend le dossier entier, témoin 40/43, écart net 2.
4. **La lettre et la valeur ne sont pas la même mesure.** À l'étage 3 juridique, Brain banc répond
   juste 36 fois sur 50 et cite la lettre 19 fois ; mem0 31 et 5 ; le RAG 39 et 30. Un dossier où
   la lettre fait foi exige de rendre le passage, pas de le résumer.

## Décision

1. **Ce qu'on porte, c'est la g12, pas une variante plus large.** La recherche de production adopte
   la chaîne `hybride_fenetres_g12` telle qu'elle a été mesurée : trois portes vers les mêmes objets
   — atomes, fenêtres, passages — sans fusion de scores entre portes ; k = 12 + 6 sur les atomes et
   douze fenêtres par défaut. Toute autre valeur est un réglage à déclarer, mesuré en ligne séparée.

2. **La couche brute entre en production.** Chaque aire reçoit ses passages (recouvrement calculé
   depuis les documents du dossier, règle « taille de passage ≥ 4 × recouvrement ») et son cache de
   fenêtres, isolés par aire, construits par le pipeline officiel (`brain.claims → public.claims`
   pour les atomes, même exigence de parité pour les passages). Aucun lecteur ne cherche dans une
   table que l'ingestion n'écrit pas — les six couplages trouvés pendant le banc sont la raison de
   cette phrase.

3. **Le passage entier est rendu quand la lettre fait foi.** `compile_call_frame` sait rendre, à la
   place d'une fenêtre, le **passage entier** dont elle est extraite, dans trois cas : la question
   vise une clause (forme `citation`, `qualification`, ou demande explicite de la lettre), la fenêtre
   retenue est tronquée (borne de caractères, ligne de tableau), ou le budget restant le permet sans
   évincer un autre appui. Le rendu porte la pièce et la ligne. Hors de ces cas, la fenêtre reste la
   règle : c'est elle qui donne le témoin le plus bas du banc.

4. **Les unités ne sont plus coupées par une borne aveugle.** La borne de 600 caractères par unité
   et l'exclusion des lignes de tableau des fenêtres, toutes deux à l'origine du plafond juridique,
   disparaissent : une unité tabulaire est une ligne entière ; une clause plus longue que la fenêtre
   est portée par son passage.

5. **Le budget de rendu se lit en part du corpus.** 12 000 caractères valent 5 % de GreenLoop et
   40 % de MOREAU. Le budget par défaut d'une aire est fixé par sa taille, et le rapport de contexte
   dit toujours quelle part du dossier il verse.

6. **Le banc reste le juge, et il n'est pas modifié par ce chantier.** La preuve du portage est le
   banc rejoué avec le chemin `brain_prod` réel, sur les deux dossiers, aux trois étages. Conditions
   de sortie : GreenLoop ≥ 84/141 en verbatim avec témoin ≤ 23 ; MOREAU > 12/43 en verbatim avec un
   témoin inférieur à celui du RAG à budget égal ; étage 3 juridique > 19/50 en lettre. Toute
   modification de l'instrument pendant le portage passe par l'ADR 0023, jamais par ce chantier.

## Conséquences

- Le chemin de production change de forme, pas seulement de paramètres : ingestion (passages,
  fenêtres), recherche (trois portes), rendu (passage entier conditionnel). Le chantier se découpe
  en sous-issues indépendantes, chacune avec sa preuve, et rien n'atterrit sans que le banc ait
  rejoué.
- Les aires existantes ne régressent pas : la g12 est activée aire par aire, l'ancien chemin reste
  disponible tant que le banc n'a pas rendu sur l'aire concernée.
- Le RAG naïf du banc reste la borne à battre et la référence de loyauté : il n'est pas « mauvais »,
  il gagne par volume sur les petits dossiers, et le rapport le dit dans ces termes.

## Hors périmètre

mem0, Letta et LoCoMo (#121) ; l'étage 3 GreenLoop homogène en cours (#120), qui pourra amender
les seuils de la décision 6 ; toute refonte du claiming (ADR 0022).
