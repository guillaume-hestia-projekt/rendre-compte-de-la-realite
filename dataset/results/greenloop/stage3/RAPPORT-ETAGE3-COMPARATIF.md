# Rapport — étage 3 comparatif

Date : 2026-09-26
Dossier : greenloop
Langue invite : en

Juge must_not_claim : 18 (705/705 jugés)

## Colonne principale

Dossier business GreenLoop : la colonne principale est `conforme_valeur` (`conformes`). `conforme_lettre` est calculée avec la même règle à quatre conditions mais n'est pas la colonne business du dossier.

## Référence du 23/09 (hors bras homogène)

Ligne nommée : fine hybride k12+k6 (2026-09-23, juge Grok 4.5 adjudication #106).
Juge de référence : Grok 4.5 (adjudication #106).
Conformes : 75/141. Disputes des deux côtés : 26/28.

## Règle conforme_lettre

1. Passage verbatim d'au moins 40 caractères significatifs de la citation (normalisation espaces et guillemets ; extrait réponse → sous-chaîne citation).
2. Tous les discriminants de la citation présents dans la réponse (nombres ancrés, dates, identifiants — `discriminants()`).
3. Pièce d'appui nommée dans la réponse.
4. Pas d'aveu d'ignorance sur le point (« ne l'établit pas », « ne précise pas », « sans citer le libellé », « par ex. » avec formes candidates).

| Bras | conforme_valeur | conforme_lettre | refus unknown | refus fautifs | fautes juge | deux côtés | stabilité | tokens invite médians | usage relais médian | formes ISO | illisibles | tout tient (verbatim) étage 2 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | 15/141 | 0/141 | 14/14 | 126 | 1 (705/705 jugés) | 0/28 | 0/5 | 28 | 29146 | 0 | 0 | — |
| brain_prod | 49/141 | 1/141 | 4/14 | 10 | 8 (705/705 jugés) | 13/28 | 2/5 | 721 | 29992 | 0 | 0 | 39/141 |
| rag_naif | 65/141 | 4/141 | 4/14 | 7 | 7 (705/705 jugés) | 28/28 | 3/5 | 2886 | 33108 | 0 | 0 | 85/141 |
| brain_banc | 78/141 | 9/141 | 2/14 | 4 | 0 (705/705 jugés) | 27/28 | 3/5 | 2382 | 32437 | 0 | 0 | 84/141 |
| mem0 | 49/141 | 3/141 | 1/14 | 3 | 2 (705/705 jugés) | 12/28 | 3/5 | 1446 | 31160 | 0 | 0 | 2/141 |

## Par forme

### A

- aggregate : refus_fautif=21
- dispute : refus_fautif=28
- single : conforme=1, refus_fautif=49
- status : refus_fautif=21
- trajectory : refus_fautif=7
- unknown : conforme=14

### brain_prod

- aggregate : conforme=7, incomplete=12, refus_fautif=2
- dispute : conforme=1, incomplete=23, refus_fautif=4
- single : conforme=30, incomplete=19, refus_fautif=1
- status : conforme=7, incomplete=14
- trajectory : incomplete=4, refus_fautif=3
- unknown : conforme=4, fautive=10

### rag_naif

- aggregate : conforme=11, incomplete=9, refus_fautif=1
- dispute : conforme=13, incomplete=14, refus_fautif=1
- single : conforme=32, incomplete=17, refus_fautif=1
- status : conforme=2, incomplete=16, refus_fautif=3
- trajectory : conforme=3, incomplete=3, refus_fautif=1
- unknown : conforme=4, fautive=10

### brain_banc

- aggregate : conforme=8, incomplete=13
- dispute : conforme=24, incomplete=2, refus_fautif=2
- single : conforme=34, incomplete=15, refus_fautif=1
- status : conforme=8, incomplete=13
- trajectory : conforme=2, incomplete=4, refus_fautif=1
- unknown : conforme=2, fautive=12

### mem0

- aggregate : conforme=10, incomplete=11
- dispute : conforme=4, incomplete=23, refus_fautif=1
- single : conforme=28, incomplete=21, refus_fautif=1
- status : conforme=4, incomplete=16, refus_fautif=1
- trajectory : conforme=2, incomplete=5
- unknown : conforme=1, fautive=13
