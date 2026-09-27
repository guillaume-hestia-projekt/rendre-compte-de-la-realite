# Témoin de brassage

Date : 2026-09-27

MOREAU n'a pas servi au réglage.

Appariement : rotation d'un cran sur les questions triées par identifiant (question *i* évaluée contre le contexte de *i+1*).

Métrique : **tout tient** (toutes les assertions de soutien présentes dans le contexte).

Dénominateur appui : **43** (même sélection que la mesure étage 2).


## Hors étage 2

- `non_etabli` (7) : MOR-Q28, MOR-Q29, MOR-Q30, MOR-Q31, MOR-Q32, MOR-Q41, MOR-Q50.
- sans assertion d'appui (1) : MOR-Q28 (non_etabli) (jamais « tout tient », listées pour traçabilité).

| fournisseur | mode | signal (vrai appariement) | témoin (brassé) | écart |
| --- | --- | --- | --- | --- |
| brain_banc | verbatim | 12/43 | 3/43 | 9 |
| brain_banc | valeur | 16/43 | 3/43 | 13 |
| brain_banc_v3 | verbatim | 15/43 | 6/43 | 9 |
| brain_banc_v3 | valeur | 19/43 | 6/43 | 13 |
| brain_banc_v4 | verbatim | 15/43 | 6/43 | 9 |
| brain_banc_v4 | valeur | 19/43 | 6/43 | 13 |
| brain_banc_calibre | verbatim | 13/43 | 2/43 | 11 |
| brain_banc_calibre | valeur | 16/43 | 2/43 | 14 |

## Lecture

brain_banc : signal valeur 16/43, témoin 3/43 (écart 13). brain_banc_calibre : signal valeur 16/43, témoin 2/43 (écart 14). brain_banc_v3 : signal valeur 19/43, témoin 6/43 (écart 13). brain_banc_v4 : signal valeur 19/43, témoin 6/43 (écart 13).

## Grille témoin (budget × fournisseur)

k ou variante : même règle que la grille « à unités et budget égaux ». Métrique : **tout tient**, mode verbatim (colonne témoin) et valeur (colonne témoin valeur).

| Budget | Fournisseur | k / variante | témoin (verbatim) | témoin (valeur) | écart (verbatim) |
| --- | --- | --- | --- | --- | --- |
| 8000 | brain_banc | figé | 3/43 | 3/43 | 9 |
| 8000 | brain_banc (fenêtre calibrée sur l'or) | figé | 2/43 | 2/43 | 11 |
| 8000 | Brain banc (g24, réglé sur le budget) | figé | 2/43 | 3/43 | 9 |
| 8000 | Brain banc (g36, réglé sur le budget) | figé | 0/43 | 1/43 | 2 |
| 8000 | Brain banc (g48, réglé sur le budget) | figé | 0/43 | 1/43 | 0 |
| 8000 | porte 3 voisinage, 1 arête (atomes) | figé | 3/43 | 3/43 | 9 |
| 8000 | porte 3 voisinage, 2 arêtes (atomes) | figé | 3/43 | 3/43 | 9 |
| 8000 | porte 3 voisinage, 1 arête (phrases) | figé | 3/43 | 3/43 | 9 |
| 8000 | porte 3 voisinage, 2 arêtes (phrases) | figé | 3/43 | 3/43 | 9 |
| 8000 | brain_prod (variante k=20) | 20 | 0/43 | 1/43 | 1 |
| 8000 | mem0 | 40 | 0/43 | 5/43 | 0 |
| 8000 | rag_naif | 12 | 9/43 | 9/43 | 17 |
| 12000 | brain_banc | figé | 3/43 | 3/43 | 9 |
| 12000 | brain_banc (fenêtre calibrée sur l'or) | figé | 2/43 | 2/43 | 11 |
| 12000 | Brain banc (g24, réglé sur le budget) | figé | 5/43 | 7/43 | 7 |
| 12000 | Brain banc (g36, réglé sur le budget) | figé | 3/43 | 4/43 | 9 |
| 12000 | Brain banc (g48, réglé sur le budget) | figé | 2/43 | 3/43 | 7 |
| 12000 | porte 3 voisinage, 1 arête (atomes) | figé | 3/43 | 3/43 | 9 |
| 12000 | porte 3 voisinage, 2 arêtes (atomes) | figé | 3/43 | 3/43 | 9 |
| 12000 | porte 3 voisinage, 1 arête (phrases) | figé | 6/43 | 6/43 | 9 |
| 12000 | porte 3 voisinage, 2 arêtes (phrases) | figé | 6/43 | 6/43 | 9 |
| 12000 | brain_prod (variante k=20) | 20 | 0/43 | 1/43 | 1 |
| 12000 | mem0 | 40 | 0/43 | 5/43 | 0 |
| 12000 | rag_naif | 12 | 14/43 | 14/43 | 21 |
| 16000 | brain_banc | figé | 3/43 | 3/43 | 9 |
| 16000 | Brain banc (g24, réglé sur le budget) | figé | 6/43 | 8/43 | 6 |
| 16000 | Brain banc (g36, réglé sur le budget) | figé | 7/43 | 9/43 | 5 |
| 16000 | Brain banc (g48, réglé sur le budget) | figé | 5/43 | 6/43 | 7 |
| 16000 | porte 3 voisinage, 1 arête (atomes) | figé | 3/43 | 3/43 | 9 |
| 16000 | porte 3 voisinage, 2 arêtes (atomes) | figé | 3/43 | 3/43 | 9 |
| 16000 | porte 3 voisinage, 1 arête (phrases) | figé | 8/43 | 9/43 | 8 |
| 16000 | porte 3 voisinage, 2 arêtes (phrases) | figé | 8/43 | 9/43 | 8 |
| 16000 | brain_prod (variante k=20) | 20 | 0/43 | 1/43 | 1 |
| 16000 | mem0 | 40 | 0/43 | 5/43 | 0 |
| 16000 | rag_naif | 12 | 19/43 | 19/43 | 20 |
| 24000 | brain_banc | figé | 3/43 | 3/43 | 9 |
| 24000 | Brain banc (g24, réglé sur le budget) | figé | 6/43 | 8/43 | 6 |
| 24000 | Brain banc (g36, réglé sur le budget) | figé | 7/43 | 9/43 | 5 |
| 24000 | Brain banc (g48, réglé sur le budget) | figé | 7/43 | 9/43 | 5 |
| 24000 | porte 3 voisinage, 1 arête (atomes) | figé | 3/43 | 3/43 | 9 |
| 24000 | porte 3 voisinage, 2 arêtes (atomes) | figé | 3/43 | 3/43 | 9 |
| 24000 | porte 3 voisinage, 1 arête (phrases) | figé | 11/43 | 11/43 | 6 |
| 24000 | porte 3 voisinage, 2 arêtes (phrases) | figé | 11/43 | 11/43 | 7 |
| 24000 | brain_prod (variante k=20) | 20 | 0/43 | 1/43 | 1 |
| 24000 | mem0 | 40 | 0/43 | 5/43 | 0 |
| 24000 | rag_naif | 12 | 28/43 | 28/43 | 14 |
