# Rapport — étage 3 comparatif

Date : 2026-09-26
Dossier : moreau
Langue invite : fr

Juge must_not_claim : 5 (250/250 jugés)

## Règle conforme_lettre

1. Passage verbatim d'au moins 40 caractères significatifs de la citation (normalisation espaces et guillemets ; extrait réponse → sous-chaîne citation).
2. Tous les discriminants de la citation présents dans la réponse (nombres ancrés, dates, identifiants — `discriminants()`).
3. Pièce d'appui nommée dans la réponse.
4. Pas d'aveu d'ignorance sur le point (« ne l'établit pas », « ne précise pas », « sans citer le libellé », « par ex. » avec formes candidates).

| Bras | conforme_valeur | conforme_lettre | refus non établi | refus fautifs | fautes juge | deux côtés | stabilité | tokens invite médians | usage relais médian | formes ISO | illisibles | tout tient (verbatim) étage 2 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | 7/50 | 0/50 | 6/7 | 6 | 0 (250/250 jugés) | 0/4 | 0/5 | 30 | 59618 | 0 | 0 | — |
| brain_prod | 25/50 | 3/50 | 3/7 | 2 | 1 (250/250 jugés) | 1/4 | 4/5 | 515 | 191303 | 3 | 0 | 1/43 |
| rag_naif | 39/50 | 30/50 | 3/7 | 0 | 3 (250/250 jugés) | 4/4 | 5/5 | 2838 | 32641 | 0 | 0 | 35/43 |
| brain_banc | 36/50 | 19/50 | 3/7 | 1 | 0 (250/250 jugés) | 4/4 | 4/5 | 1557 | 126136 | 0 | 0 | 12/43 |
| mem0 | 31/50 | 5/50 | 2/7 | 0 | 1 (250/250 jugés) | 4/4 | 3/5 | 1770 | 63618 | 0 | 0 | 0/43 |

Passe v1 anglaise (valeur seule) archivée dans `etage3-v1-anglais/` (A 7, brain_prod 11, rag_naif 15, brain_banc 12, mem0 21 conformes /50).

## Par forme

### A

- chronologie : incomplete=3, refus_fautif=2
- citation : incomplete=6, refus_fautif=1
- contradiction : incomplete=4
- date : incomplete=6, refus_fautif=1
- delai : conforme=1, incomplete=4
- montant : incomplete=8, refus_fautif=2
- non_etabli : conforme=6, fautive=1
- qualification : incomplete=5

### brain_prod

- chronologie : conforme=1, incomplete=4
- citation : conforme=4, incomplete=3
- contradiction : conforme=1, incomplete=3
- date : conforme=4, incomplete=2, refus_fautif=1
- delai : conforme=4, incomplete=1
- montant : conforme=6, incomplete=3, refus_fautif=1
- non_etabli : conforme=3, fautive=4
- qualification : conforme=2, incomplete=3

### rag_naif

- chronologie : conforme=4, incomplete=1
- citation : conforme=6, incomplete=1
- contradiction : conforme=3, incomplete=1
- date : conforme=6, incomplete=1
- delai : conforme=4, incomplete=1
- montant : conforme=9, incomplete=1
- non_etabli : conforme=3, fautive=4
- qualification : conforme=4, incomplete=1

### brain_banc

- chronologie : conforme=2, incomplete=3
- citation : conforme=4, incomplete=2, refus_fautif=1
- contradiction : conforme=3, incomplete=1
- date : conforme=5, incomplete=2
- delai : conforme=5
- montant : conforme=9, incomplete=1
- non_etabli : conforme=3, fautive=4
- qualification : conforme=5

### mem0

- chronologie : conforme=2, incomplete=3
- citation : conforme=6, incomplete=1
- contradiction : conforme=3, incomplete=1
- date : incomplete=7
- delai : conforme=4, incomplete=1
- montant : conforme=10
- non_etabli : conforme=2, fautive=5
- qualification : conforme=4, incomplete=1
