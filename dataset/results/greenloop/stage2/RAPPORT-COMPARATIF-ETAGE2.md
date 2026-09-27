# Rapport comparatif étage 2 — GreenLoop

Note de biais : le mode valeur a été ajouté après observation du score mem0 (2/141). Le mode verbatim reste inchangé pour la comparabilité ; les deux colonnes sont toujours rapportées côte à côte.

Date : 2026-09-27

## Par forme — tout tient / au moins une

| Fournisseur | k | budget | forme | tout tient (verbatim) | tout tient (valeur) | ≥1 (verbatim) | ≥1 (valeur) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| rag_naif | 12 | 8000 | aggregate | 11/21 | 11/21 | 17/21 | 17/21 |
| rag_naif | 12 | 8000 | dispute | 2/28 | 2/28 | 28/28 | 28/28 |
| rag_naif | 12 | 8000 | single | 43/50 | 44/50 | 43/50 | 44/50 |
| rag_naif | 12 | 8000 | status | 0/21 | 0/21 | 5/21 | 5/21 |
| rag_naif | 12 | 8000 | trajectory | 1/7 | 1/7 | 5/7 | 5/7 |
| rag_naif | 12 | 8000 | unknown | 7/14 | 7/14 | 12/14 | 12/14 |
| rag_naif | 12 | 12000 | aggregate | 13/21 | 13/21 | 18/21 | 18/21 |
| rag_naif | 12 | 12000 | dispute | 14/28 | 14/28 | 28/28 | 28/28 |
| rag_naif | 12 | 12000 | single | 47/50 | 48/50 | 47/50 | 48/50 |
| rag_naif | 12 | 12000 | status | 0/21 | 0/21 | 9/21 | 9/21 |
| rag_naif | 12 | 12000 | trajectory | 2/7 | 2/7 | 7/7 | 7/7 |
| rag_naif | 12 | 12000 | unknown | 9/14 | 9/14 | 12/14 | 12/14 |
| rag_naif | 12 | 16000 | aggregate | 15/21 | 15/21 | 21/21 | 21/21 |
| rag_naif | 12 | 16000 | dispute | 22/28 | 22/28 | 28/28 | 28/28 |
| rag_naif | 12 | 16000 | single | 47/50 | 48/50 | 47/50 | 48/50 |
| rag_naif | 12 | 16000 | status | 1/21 | 1/21 | 14/21 | 14/21 |
| rag_naif | 12 | 16000 | trajectory | 2/7 | 2/7 | 7/7 | 7/7 |
| rag_naif | 12 | 16000 | unknown | 9/14 | 9/14 | 12/14 | 12/14 |
| brain_prod | 8 | 8000 | aggregate | 3/21 | 3/21 | 17/21 | 17/21 |
| brain_prod | 8 | 8000 | dispute | 1/28 | 1/28 | 6/28 | 6/28 |
| brain_prod | 8 | 8000 | single | 33/50 | 35/50 | 33/50 | 35/50 |
| brain_prod | 8 | 8000 | status | 0/21 | 5/21 | 17/21 | 17/21 |
| brain_prod | 8 | 8000 | trajectory | 0/7 | 0/7 | 4/7 | 4/7 |
| brain_prod | 8 | 8000 | unknown | 2/14 | 2/14 | 3/14 | 3/14 |
| brain_prod (variante k=12) | 12 | 8000 | aggregate | 3/21 | 3/21 | 17/21 | 17/21 |
| brain_prod (variante k=12) | 12 | 8000 | dispute | 3/28 | 3/28 | 10/28 | 10/28 |
| brain_prod (variante k=12) | 12 | 8000 | single | 34/50 | 37/50 | 34/50 | 37/50 |
| brain_prod (variante k=12) | 12 | 8000 | status | 0/21 | 6/21 | 18/21 | 18/21 |
| brain_prod (variante k=12) | 12 | 8000 | trajectory | 0/7 | 0/7 | 4/7 | 4/7 |
| brain_prod (variante k=12) | 12 | 8000 | unknown | 2/14 | 2/14 | 3/14 | 3/14 |
| brain_prod (variante k=20) | 20 | 8000 | aggregate | 3/21 | 3/21 | 17/21 | 17/21 |
| brain_prod (variante k=20) | 20 | 8000 | dispute | 3/28 | 3/28 | 16/28 | 16/28 |
| brain_prod (variante k=20) | 20 | 8000 | single | 35/50 | 38/50 | 35/50 | 38/50 |
| brain_prod (variante k=20) | 20 | 8000 | status | 1/21 | 8/21 | 20/21 | 20/21 |
| brain_prod (variante k=20) | 20 | 8000 | trajectory | 0/7 | 0/7 | 4/7 | 4/7 |
| brain_prod (variante k=20) | 20 | 8000 | unknown | 2/14 | 2/14 | 4/14 | 4/14 |
| brain_prod (variante k=40) | 40 | 8000 | aggregate | 3/21 | 3/21 | 17/21 | 17/21 |
| brain_prod (variante k=40) | 40 | 8000 | dispute | 3/28 | 3/28 | 16/28 | 16/28 |
| brain_prod (variante k=40) | 40 | 8000 | single | 35/50 | 38/50 | 35/50 | 38/50 |
| brain_prod (variante k=40) | 40 | 8000 | status | 1/21 | 8/21 | 20/21 | 20/21 |
| brain_prod (variante k=40) | 40 | 8000 | trajectory | 0/7 | 0/7 | 4/7 | 4/7 |
| brain_prod (variante k=40) | 40 | 8000 | unknown | 2/14 | 2/14 | 4/14 | 4/14 |
| brain_prod | 8 | 12000 | aggregate | 3/21 | 3/21 | 17/21 | 17/21 |
| brain_prod | 8 | 12000 | dispute | 1/28 | 1/28 | 6/28 | 6/28 |
| brain_prod | 8 | 12000 | single | 33/50 | 35/50 | 33/50 | 35/50 |
| brain_prod | 8 | 12000 | status | 0/21 | 5/21 | 17/21 | 17/21 |
| brain_prod | 8 | 12000 | trajectory | 0/7 | 0/7 | 4/7 | 4/7 |
| brain_prod | 8 | 12000 | unknown | 2/14 | 2/14 | 3/14 | 3/14 |
| brain_prod (variante k=12) | 12 | 12000 | aggregate | 3/21 | 3/21 | 17/21 | 17/21 |
| brain_prod (variante k=12) | 12 | 12000 | dispute | 3/28 | 3/28 | 10/28 | 10/28 |
| brain_prod (variante k=12) | 12 | 12000 | single | 34/50 | 37/50 | 34/50 | 37/50 |
| brain_prod (variante k=12) | 12 | 12000 | status | 0/21 | 6/21 | 18/21 | 18/21 |
| brain_prod (variante k=12) | 12 | 12000 | trajectory | 0/7 | 0/7 | 4/7 | 4/7 |
| brain_prod (variante k=12) | 12 | 12000 | unknown | 2/14 | 2/14 | 3/14 | 3/14 |
| brain_prod (variante k=20) | 20 | 12000 | aggregate | 3/21 | 3/21 | 17/21 | 17/21 |
| brain_prod (variante k=20) | 20 | 12000 | dispute | 3/28 | 3/28 | 16/28 | 16/28 |
| brain_prod (variante k=20) | 20 | 12000 | single | 35/50 | 38/50 | 35/50 | 38/50 |
| brain_prod (variante k=20) | 20 | 12000 | status | 1/21 | 8/21 | 20/21 | 20/21 |
| brain_prod (variante k=20) | 20 | 12000 | trajectory | 0/7 | 0/7 | 4/7 | 4/7 |
| brain_prod (variante k=20) | 20 | 12000 | unknown | 2/14 | 2/14 | 4/14 | 4/14 |
| brain_prod (variante k=40) | 40 | 12000 | aggregate | 3/21 | 3/21 | 17/21 | 17/21 |
| brain_prod (variante k=40) | 40 | 12000 | dispute | 3/28 | 3/28 | 16/28 | 16/28 |
| brain_prod (variante k=40) | 40 | 12000 | single | 35/50 | 38/50 | 35/50 | 38/50 |
| brain_prod (variante k=40) | 40 | 12000 | status | 1/21 | 8/21 | 20/21 | 20/21 |
| brain_prod (variante k=40) | 40 | 12000 | trajectory | 0/7 | 0/7 | 4/7 | 4/7 |
| brain_prod (variante k=40) | 40 | 12000 | unknown | 2/14 | 2/14 | 4/14 | 4/14 |
| brain_prod | 8 | 16000 | aggregate | 3/21 | 3/21 | 17/21 | 17/21 |
| brain_prod | 8 | 16000 | dispute | 1/28 | 1/28 | 6/28 | 6/28 |
| brain_prod | 8 | 16000 | single | 33/50 | 35/50 | 33/50 | 35/50 |
| brain_prod | 8 | 16000 | status | 0/21 | 5/21 | 17/21 | 17/21 |
| brain_prod | 8 | 16000 | trajectory | 0/7 | 0/7 | 4/7 | 4/7 |
| brain_prod | 8 | 16000 | unknown | 2/14 | 2/14 | 3/14 | 3/14 |
| brain_prod (variante k=12) | 12 | 16000 | aggregate | 3/21 | 3/21 | 17/21 | 17/21 |
| brain_prod (variante k=12) | 12 | 16000 | dispute | 3/28 | 3/28 | 10/28 | 10/28 |
| brain_prod (variante k=12) | 12 | 16000 | single | 34/50 | 37/50 | 34/50 | 37/50 |
| brain_prod (variante k=12) | 12 | 16000 | status | 0/21 | 6/21 | 18/21 | 18/21 |
| brain_prod (variante k=12) | 12 | 16000 | trajectory | 0/7 | 0/7 | 4/7 | 4/7 |
| brain_prod (variante k=12) | 12 | 16000 | unknown | 2/14 | 2/14 | 3/14 | 3/14 |
| brain_prod (variante k=20) | 20 | 16000 | aggregate | 3/21 | 3/21 | 17/21 | 17/21 |
| brain_prod (variante k=20) | 20 | 16000 | dispute | 3/28 | 3/28 | 16/28 | 16/28 |
| brain_prod (variante k=20) | 20 | 16000 | single | 35/50 | 38/50 | 35/50 | 38/50 |
| brain_prod (variante k=20) | 20 | 16000 | status | 1/21 | 8/21 | 20/21 | 20/21 |
| brain_prod (variante k=20) | 20 | 16000 | trajectory | 0/7 | 0/7 | 4/7 | 4/7 |
| brain_prod (variante k=20) | 20 | 16000 | unknown | 2/14 | 2/14 | 4/14 | 4/14 |
| brain_prod (variante k=40) | 40 | 16000 | aggregate | 3/21 | 3/21 | 17/21 | 17/21 |
| brain_prod (variante k=40) | 40 | 16000 | dispute | 3/28 | 3/28 | 16/28 | 16/28 |
| brain_prod (variante k=40) | 40 | 16000 | single | 35/50 | 38/50 | 35/50 | 38/50 |
| brain_prod (variante k=40) | 40 | 16000 | status | 1/21 | 8/21 | 20/21 | 20/21 |
| brain_prod (variante k=40) | 40 | 16000 | trajectory | 0/7 | 0/7 | 4/7 | 4/7 |
| brain_prod (variante k=40) | 40 | 16000 | unknown | 2/14 | 2/14 | 4/14 | 4/14 |
| brain_prod | 8 | 24000 | aggregate | 3/21 | 3/21 | 17/21 | 17/21 |
| brain_prod | 8 | 24000 | dispute | 1/28 | 1/28 | 6/28 | 6/28 |
| brain_prod | 8 | 24000 | single | 33/50 | 35/50 | 33/50 | 35/50 |
| brain_prod | 8 | 24000 | status | 0/21 | 5/21 | 17/21 | 17/21 |
| brain_prod | 8 | 24000 | trajectory | 0/7 | 0/7 | 4/7 | 4/7 |
| brain_prod | 8 | 24000 | unknown | 2/14 | 2/14 | 3/14 | 3/14 |
| brain_prod (variante k=12) | 12 | 24000 | aggregate | 3/21 | 3/21 | 17/21 | 17/21 |
| brain_prod (variante k=12) | 12 | 24000 | dispute | 3/28 | 3/28 | 10/28 | 10/28 |
| brain_prod (variante k=12) | 12 | 24000 | single | 34/50 | 37/50 | 34/50 | 37/50 |
| brain_prod (variante k=12) | 12 | 24000 | status | 0/21 | 6/21 | 18/21 | 18/21 |
| brain_prod (variante k=12) | 12 | 24000 | trajectory | 0/7 | 0/7 | 4/7 | 4/7 |
| brain_prod (variante k=12) | 12 | 24000 | unknown | 2/14 | 2/14 | 3/14 | 3/14 |
| brain_prod (variante k=20) | 20 | 24000 | aggregate | 3/21 | 3/21 | 17/21 | 17/21 |
| brain_prod (variante k=20) | 20 | 24000 | dispute | 3/28 | 3/28 | 16/28 | 16/28 |
| brain_prod (variante k=20) | 20 | 24000 | single | 35/50 | 38/50 | 35/50 | 38/50 |
| brain_prod (variante k=20) | 20 | 24000 | status | 1/21 | 8/21 | 20/21 | 20/21 |
| brain_prod (variante k=20) | 20 | 24000 | trajectory | 0/7 | 0/7 | 4/7 | 4/7 |
| brain_prod (variante k=20) | 20 | 24000 | unknown | 2/14 | 2/14 | 4/14 | 4/14 |
| brain_prod (variante k=40) | 40 | 24000 | aggregate | 3/21 | 3/21 | 17/21 | 17/21 |
| brain_prod (variante k=40) | 40 | 24000 | dispute | 3/28 | 3/28 | 16/28 | 16/28 |
| brain_prod (variante k=40) | 40 | 24000 | single | 35/50 | 38/50 | 35/50 | 38/50 |
| brain_prod (variante k=40) | 40 | 24000 | status | 1/21 | 8/21 | 20/21 | 20/21 |
| brain_prod (variante k=40) | 40 | 24000 | trajectory | 0/7 | 0/7 | 4/7 | 4/7 |
| brain_prod (variante k=40) | 40 | 24000 | unknown | 2/14 | 2/14 | 4/14 | 4/14 |
| brain_banc | figé | 8000 | aggregate | 8/21 | 9/21 | 21/21 | 21/21 |
| brain_banc | figé | 8000 | dispute | 24/28 | 24/28 | 28/28 | 28/28 |
| brain_banc | figé | 8000 | single | 40/50 | 41/50 | 40/50 | 41/50 |
| brain_banc | figé | 8000 | status | 1/21 | 1/21 | 19/21 | 19/21 |
| brain_banc | figé | 8000 | trajectory | 1/7 | 1/7 | 6/7 | 6/7 |
| brain_banc | figé | 8000 | unknown | 5/14 | 5/14 | 11/14 | 11/14 |
| brain_banc | figé | 12000 | aggregate | 9/21 | 10/21 | 21/21 | 21/21 |
| brain_banc | figé | 12000 | dispute | 24/28 | 24/28 | 28/28 | 28/28 |
| brain_banc | figé | 12000 | single | 43/50 | 45/50 | 43/50 | 45/50 |
| brain_banc | figé | 12000 | status | 2/21 | 2/21 | 19/21 | 19/21 |
| brain_banc | figé | 12000 | trajectory | 1/7 | 1/7 | 6/7 | 6/7 |
| brain_banc | figé | 12000 | unknown | 5/14 | 5/14 | 11/14 | 11/14 |
| brain_banc | figé | 16000 | aggregate | 9/21 | 10/21 | 21/21 | 21/21 |
| brain_banc | figé | 16000 | dispute | 24/28 | 24/28 | 28/28 | 28/28 |
| brain_banc | figé | 16000 | single | 43/50 | 45/50 | 43/50 | 45/50 |
| brain_banc | figé | 16000 | status | 2/21 | 2/21 | 19/21 | 19/21 |
| brain_banc | figé | 16000 | trajectory | 1/7 | 1/7 | 6/7 | 6/7 |
| brain_banc | figé | 16000 | unknown | 5/14 | 5/14 | 11/14 | 11/14 |
| Brain banc (g24, réglé sur le budget) | figé | 8000 | aggregate | 3/21 | 3/21 | 16/21 | 16/21 |
| Brain banc (g24, réglé sur le budget) | figé | 8000 | dispute | 9/28 | 9/28 | 27/28 | 27/28 |
| Brain banc (g24, réglé sur le budget) | figé | 8000 | single | 23/50 | 25/50 | 23/50 | 25/50 |
| Brain banc (g24, réglé sur le budget) | figé | 8000 | status | 1/21 | 1/21 | 20/21 | 20/21 |
| Brain banc (g24, réglé sur le budget) | figé | 8000 | trajectory | 0/7 | 0/7 | 3/7 | 3/7 |
| Brain banc (g24, réglé sur le budget) | figé | 8000 | unknown | 3/14 | 3/14 | 4/14 | 5/14 |
| Brain banc (g24, réglé sur le budget) | figé | 12000 | aggregate | 4/21 | 4/21 | 16/21 | 17/21 |
| Brain banc (g24, réglé sur le budget) | figé | 12000 | dispute | 24/28 | 24/28 | 27/28 | 27/28 |
| Brain banc (g24, réglé sur le budget) | figé | 12000 | single | 34/50 | 36/50 | 34/50 | 36/50 |
| Brain banc (g24, réglé sur le budget) | figé | 12000 | status | 1/21 | 1/21 | 20/21 | 20/21 |
| Brain banc (g24, réglé sur le budget) | figé | 12000 | trajectory | 0/7 | 0/7 | 5/7 | 5/7 |
| Brain banc (g24, réglé sur le budget) | figé | 12000 | unknown | 4/14 | 4/14 | 10/14 | 10/14 |
| Brain banc (g24, réglé sur le budget) | figé | 16000 | aggregate | 9/21 | 9/21 | 20/21 | 21/21 |
| Brain banc (g24, réglé sur le budget) | figé | 16000 | dispute | 24/28 | 24/28 | 28/28 | 28/28 |
| Brain banc (g24, réglé sur le budget) | figé | 16000 | single | 43/50 | 44/50 | 43/50 | 44/50 |
| Brain banc (g24, réglé sur le budget) | figé | 16000 | status | 1/21 | 1/21 | 20/21 | 20/21 |
| Brain banc (g24, réglé sur le budget) | figé | 16000 | trajectory | 1/7 | 1/7 | 7/7 | 7/7 |
| Brain banc (g24, réglé sur le budget) | figé | 16000 | unknown | 5/14 | 5/14 | 11/14 | 11/14 |
| Brain banc (g24, réglé sur le budget) | figé | 24000 | aggregate | 10/21 | 11/21 | 21/21 | 21/21 |
| Brain banc (g24, réglé sur le budget) | figé | 24000 | dispute | 25/28 | 25/28 | 28/28 | 28/28 |
| Brain banc (g24, réglé sur le budget) | figé | 24000 | single | 44/50 | 45/50 | 44/50 | 45/50 |
| Brain banc (g24, réglé sur le budget) | figé | 24000 | status | 2/21 | 2/21 | 20/21 | 20/21 |
| Brain banc (g24, réglé sur le budget) | figé | 24000 | trajectory | 2/7 | 2/7 | 7/7 | 7/7 |
| Brain banc (g24, réglé sur le budget) | figé | 24000 | unknown | 6/14 | 6/14 | 11/14 | 11/14 |
| Brain banc (g36, réglé sur le budget) | figé | 8000 | aggregate | 3/21 | 3/21 | 15/21 | 15/21 |
| Brain banc (g36, réglé sur le budget) | figé | 8000 | dispute | 6/28 | 6/28 | 27/28 | 27/28 |
| Brain banc (g36, réglé sur le budget) | figé | 8000 | single | 23/50 | 25/50 | 23/50 | 25/50 |
| Brain banc (g36, réglé sur le budget) | figé | 8000 | status | 0/21 | 0/21 | 19/21 | 19/21 |
| Brain banc (g36, réglé sur le budget) | figé | 8000 | trajectory | 0/7 | 0/7 | 3/7 | 3/7 |
| Brain banc (g36, réglé sur le budget) | figé | 8000 | unknown | 2/14 | 2/14 | 3/14 | 4/14 |
| Brain banc (g36, réglé sur le budget) | figé | 12000 | aggregate | 3/21 | 3/21 | 15/21 | 15/21 |
| Brain banc (g36, réglé sur le budget) | figé | 12000 | dispute | 13/28 | 13/28 | 27/28 | 27/28 |
| Brain banc (g36, réglé sur le budget) | figé | 12000 | single | 23/50 | 26/50 | 23/50 | 26/50 |
| Brain banc (g36, réglé sur le budget) | figé | 12000 | status | 1/21 | 1/21 | 20/21 | 20/21 |
| Brain banc (g36, réglé sur le budget) | figé | 12000 | trajectory | 0/7 | 0/7 | 3/7 | 3/7 |
| Brain banc (g36, réglé sur le budget) | figé | 12000 | unknown | 3/14 | 3/14 | 4/14 | 5/14 |
| Brain banc (g36, réglé sur le budget) | figé | 16000 | aggregate | 3/21 | 3/21 | 16/21 | 16/21 |
| Brain banc (g36, réglé sur le budget) | figé | 16000 | dispute | 24/28 | 24/28 | 27/28 | 27/28 |
| Brain banc (g36, réglé sur le budget) | figé | 16000 | single | 27/50 | 31/50 | 27/50 | 31/50 |
| Brain banc (g36, réglé sur le budget) | figé | 16000 | status | 1/21 | 1/21 | 20/21 | 20/21 |
| Brain banc (g36, réglé sur le budget) | figé | 16000 | trajectory | 0/7 | 0/7 | 4/7 | 4/7 |
| Brain banc (g36, réglé sur le budget) | figé | 16000 | unknown | 4/14 | 4/14 | 9/14 | 9/14 |
| Brain banc (g36, réglé sur le budget) | figé | 24000 | aggregate | 9/21 | 9/21 | 20/21 | 21/21 |
| Brain banc (g36, réglé sur le budget) | figé | 24000 | dispute | 25/28 | 25/28 | 27/28 | 27/28 |
| Brain banc (g36, réglé sur le budget) | figé | 24000 | single | 44/50 | 45/50 | 44/50 | 45/50 |
| Brain banc (g36, réglé sur le budget) | figé | 24000 | status | 1/21 | 1/21 | 20/21 | 20/21 |
| Brain banc (g36, réglé sur le budget) | figé | 24000 | trajectory | 2/7 | 2/7 | 7/7 | 7/7 |
| Brain banc (g36, réglé sur le budget) | figé | 24000 | unknown | 5/14 | 5/14 | 11/14 | 11/14 |
| Brain banc (g48, réglé sur le budget) | figé | 8000 | aggregate | 3/21 | 3/21 | 15/21 | 15/21 |
| Brain banc (g48, réglé sur le budget) | figé | 8000 | dispute | 11/28 | 11/28 | 26/28 | 26/28 |
| Brain banc (g48, réglé sur le budget) | figé | 8000 | single | 23/50 | 25/50 | 23/50 | 25/50 |
| Brain banc (g48, réglé sur le budget) | figé | 8000 | status | 0/21 | 0/21 | 19/21 | 19/21 |
| Brain banc (g48, réglé sur le budget) | figé | 8000 | trajectory | 0/7 | 0/7 | 3/7 | 3/7 |
| Brain banc (g48, réglé sur le budget) | figé | 8000 | unknown | 1/14 | 1/14 | 2/14 | 3/14 |
| Brain banc (g48, réglé sur le budget) | figé | 12000 | aggregate | 3/21 | 3/21 | 16/21 | 16/21 |
| Brain banc (g48, réglé sur le budget) | figé | 12000 | dispute | 11/28 | 11/28 | 27/28 | 27/28 |
| Brain banc (g48, réglé sur le budget) | figé | 12000 | single | 23/50 | 26/50 | 23/50 | 26/50 |
| Brain banc (g48, réglé sur le budget) | figé | 12000 | status | 0/21 | 0/21 | 19/21 | 19/21 |
| Brain banc (g48, réglé sur le budget) | figé | 12000 | trajectory | 0/7 | 0/7 | 3/7 | 3/7 |
| Brain banc (g48, réglé sur le budget) | figé | 12000 | unknown | 2/14 | 2/14 | 3/14 | 4/14 |
| Brain banc (g48, réglé sur le budget) | figé | 16000 | aggregate | 3/21 | 3/21 | 17/21 | 17/21 |
| Brain banc (g48, réglé sur le budget) | figé | 16000 | dispute | 22/28 | 22/28 | 27/28 | 27/28 |
| Brain banc (g48, réglé sur le budget) | figé | 16000 | single | 23/50 | 26/50 | 23/50 | 26/50 |
| Brain banc (g48, réglé sur le budget) | figé | 16000 | status | 1/21 | 1/21 | 20/21 | 20/21 |
| Brain banc (g48, réglé sur le budget) | figé | 16000 | trajectory | 0/7 | 0/7 | 3/7 | 3/7 |
| Brain banc (g48, réglé sur le budget) | figé | 16000 | unknown | 3/14 | 3/14 | 4/14 | 5/14 |
| Brain banc (g48, réglé sur le budget) | figé | 24000 | aggregate | 5/21 | 6/21 | 17/21 | 17/21 |
| Brain banc (g48, réglé sur le budget) | figé | 24000 | dispute | 24/28 | 24/28 | 27/28 | 27/28 |
| Brain banc (g48, réglé sur le budget) | figé | 24000 | single | 37/50 | 39/50 | 37/50 | 39/50 |
| Brain banc (g48, réglé sur le budget) | figé | 24000 | status | 1/21 | 1/21 | 20/21 | 20/21 |
| Brain banc (g48, réglé sur le budget) | figé | 24000 | trajectory | 1/7 | 1/7 | 5/7 | 5/7 |
| Brain banc (g48, réglé sur le budget) | figé | 24000 | unknown | 4/14 | 4/14 | 10/14 | 10/14 |
| porte 3 voisinage, 1 arête (atomes) | figé | 8000 | aggregate | 8/21 | 9/21 | 21/21 | 21/21 |
| porte 3 voisinage, 1 arête (atomes) | figé | 8000 | dispute | 24/28 | 24/28 | 28/28 | 28/28 |
| porte 3 voisinage, 1 arête (atomes) | figé | 8000 | single | 40/50 | 41/50 | 40/50 | 41/50 |
| porte 3 voisinage, 1 arête (atomes) | figé | 8000 | status | 1/21 | 1/21 | 19/21 | 19/21 |
| porte 3 voisinage, 1 arête (atomes) | figé | 8000 | trajectory | 1/7 | 1/7 | 6/7 | 6/7 |
| porte 3 voisinage, 1 arête (atomes) | figé | 8000 | unknown | 5/14 | 5/14 | 11/14 | 11/14 |
| porte 3 voisinage, 1 arête (atomes) | figé | 12000 | aggregate | 9/21 | 10/21 | 21/21 | 21/21 |
| porte 3 voisinage, 1 arête (atomes) | figé | 12000 | dispute | 24/28 | 24/28 | 28/28 | 28/28 |
| porte 3 voisinage, 1 arête (atomes) | figé | 12000 | single | 43/50 | 45/50 | 43/50 | 45/50 |
| porte 3 voisinage, 1 arête (atomes) | figé | 12000 | status | 2/21 | 2/21 | 19/21 | 19/21 |
| porte 3 voisinage, 1 arête (atomes) | figé | 12000 | trajectory | 1/7 | 1/7 | 6/7 | 6/7 |
| porte 3 voisinage, 1 arête (atomes) | figé | 12000 | unknown | 5/14 | 5/14 | 11/14 | 11/14 |
| porte 3 voisinage, 1 arête (atomes) | figé | 16000 | aggregate | 9/21 | 10/21 | 21/21 | 21/21 |
| porte 3 voisinage, 1 arête (atomes) | figé | 16000 | dispute | 24/28 | 24/28 | 28/28 | 28/28 |
| porte 3 voisinage, 1 arête (atomes) | figé | 16000 | single | 43/50 | 45/50 | 43/50 | 45/50 |
| porte 3 voisinage, 1 arête (atomes) | figé | 16000 | status | 2/21 | 2/21 | 19/21 | 19/21 |
| porte 3 voisinage, 1 arête (atomes) | figé | 16000 | trajectory | 1/7 | 1/7 | 6/7 | 6/7 |
| porte 3 voisinage, 1 arête (atomes) | figé | 16000 | unknown | 5/14 | 5/14 | 11/14 | 11/14 |
| porte 3 voisinage, 2 arêtes (atomes) | figé | 8000 | aggregate | 8/21 | 9/21 | 21/21 | 21/21 |
| porte 3 voisinage, 2 arêtes (atomes) | figé | 8000 | dispute | 24/28 | 24/28 | 28/28 | 28/28 |
| porte 3 voisinage, 2 arêtes (atomes) | figé | 8000 | single | 40/50 | 41/50 | 40/50 | 41/50 |
| porte 3 voisinage, 2 arêtes (atomes) | figé | 8000 | status | 1/21 | 1/21 | 19/21 | 19/21 |
| porte 3 voisinage, 2 arêtes (atomes) | figé | 8000 | trajectory | 1/7 | 1/7 | 6/7 | 6/7 |
| porte 3 voisinage, 2 arêtes (atomes) | figé | 8000 | unknown | 5/14 | 5/14 | 11/14 | 11/14 |
| porte 3 voisinage, 2 arêtes (atomes) | figé | 12000 | aggregate | 9/21 | 10/21 | 21/21 | 21/21 |
| porte 3 voisinage, 2 arêtes (atomes) | figé | 12000 | dispute | 24/28 | 24/28 | 28/28 | 28/28 |
| porte 3 voisinage, 2 arêtes (atomes) | figé | 12000 | single | 43/50 | 45/50 | 43/50 | 45/50 |
| porte 3 voisinage, 2 arêtes (atomes) | figé | 12000 | status | 2/21 | 2/21 | 19/21 | 19/21 |
| porte 3 voisinage, 2 arêtes (atomes) | figé | 12000 | trajectory | 1/7 | 1/7 | 6/7 | 6/7 |
| porte 3 voisinage, 2 arêtes (atomes) | figé | 12000 | unknown | 5/14 | 5/14 | 11/14 | 11/14 |
| porte 3 voisinage, 2 arêtes (atomes) | figé | 16000 | aggregate | 9/21 | 10/21 | 21/21 | 21/21 |
| porte 3 voisinage, 2 arêtes (atomes) | figé | 16000 | dispute | 24/28 | 24/28 | 28/28 | 28/28 |
| porte 3 voisinage, 2 arêtes (atomes) | figé | 16000 | single | 43/50 | 45/50 | 43/50 | 45/50 |
| porte 3 voisinage, 2 arêtes (atomes) | figé | 16000 | status | 2/21 | 2/21 | 19/21 | 19/21 |
| porte 3 voisinage, 2 arêtes (atomes) | figé | 16000 | trajectory | 1/7 | 1/7 | 6/7 | 6/7 |
| porte 3 voisinage, 2 arêtes (atomes) | figé | 16000 | unknown | 5/14 | 5/14 | 11/14 | 11/14 |
| porte 3 voisinage, 1 arête (phrases) | figé | 8000 | aggregate | 8/21 | 9/21 | 21/21 | 21/21 |
| porte 3 voisinage, 1 arête (phrases) | figé | 8000 | dispute | 24/28 | 24/28 | 28/28 | 28/28 |
| porte 3 voisinage, 1 arête (phrases) | figé | 8000 | single | 40/50 | 41/50 | 40/50 | 41/50 |
| porte 3 voisinage, 1 arête (phrases) | figé | 8000 | status | 1/21 | 1/21 | 19/21 | 19/21 |
| porte 3 voisinage, 1 arête (phrases) | figé | 8000 | trajectory | 1/7 | 1/7 | 6/7 | 6/7 |
| porte 3 voisinage, 1 arête (phrases) | figé | 8000 | unknown | 5/14 | 5/14 | 11/14 | 11/14 |
| porte 3 voisinage, 1 arête (phrases) | figé | 12000 | aggregate | 9/21 | 10/21 | 21/21 | 21/21 |
| porte 3 voisinage, 1 arête (phrases) | figé | 12000 | dispute | 26/28 | 26/28 | 28/28 | 28/28 |
| porte 3 voisinage, 1 arête (phrases) | figé | 12000 | single | 43/50 | 45/50 | 43/50 | 45/50 |
| porte 3 voisinage, 1 arête (phrases) | figé | 12000 | status | 2/21 | 2/21 | 19/21 | 19/21 |
| porte 3 voisinage, 1 arête (phrases) | figé | 12000 | trajectory | 1/7 | 1/7 | 6/7 | 6/7 |
| porte 3 voisinage, 1 arête (phrases) | figé | 12000 | unknown | 6/14 | 6/14 | 11/14 | 11/14 |
| porte 3 voisinage, 1 arête (phrases) | figé | 16000 | aggregate | 9/21 | 10/21 | 21/21 | 21/21 |
| porte 3 voisinage, 1 arête (phrases) | figé | 16000 | dispute | 26/28 | 26/28 | 28/28 | 28/28 |
| porte 3 voisinage, 1 arête (phrases) | figé | 16000 | single | 43/50 | 45/50 | 43/50 | 45/50 |
| porte 3 voisinage, 1 arête (phrases) | figé | 16000 | status | 2/21 | 2/21 | 19/21 | 19/21 |
| porte 3 voisinage, 1 arête (phrases) | figé | 16000 | trajectory | 1/7 | 1/7 | 6/7 | 6/7 |
| porte 3 voisinage, 1 arête (phrases) | figé | 16000 | unknown | 6/14 | 6/14 | 11/14 | 11/14 |
| porte 3 voisinage, 2 arêtes (phrases) | figé | 8000 | aggregate | 8/21 | 9/21 | 21/21 | 21/21 |
| porte 3 voisinage, 2 arêtes (phrases) | figé | 8000 | dispute | 24/28 | 24/28 | 28/28 | 28/28 |
| porte 3 voisinage, 2 arêtes (phrases) | figé | 8000 | single | 40/50 | 41/50 | 40/50 | 41/50 |
| porte 3 voisinage, 2 arêtes (phrases) | figé | 8000 | status | 1/21 | 1/21 | 19/21 | 19/21 |
| porte 3 voisinage, 2 arêtes (phrases) | figé | 8000 | trajectory | 1/7 | 1/7 | 6/7 | 6/7 |
| porte 3 voisinage, 2 arêtes (phrases) | figé | 8000 | unknown | 5/14 | 5/14 | 11/14 | 11/14 |
| porte 3 voisinage, 2 arêtes (phrases) | figé | 12000 | aggregate | 9/21 | 10/21 | 21/21 | 21/21 |
| porte 3 voisinage, 2 arêtes (phrases) | figé | 12000 | dispute | 26/28 | 26/28 | 28/28 | 28/28 |
| porte 3 voisinage, 2 arêtes (phrases) | figé | 12000 | single | 43/50 | 45/50 | 43/50 | 45/50 |
| porte 3 voisinage, 2 arêtes (phrases) | figé | 12000 | status | 2/21 | 2/21 | 19/21 | 19/21 |
| porte 3 voisinage, 2 arêtes (phrases) | figé | 12000 | trajectory | 1/7 | 1/7 | 6/7 | 6/7 |
| porte 3 voisinage, 2 arêtes (phrases) | figé | 12000 | unknown | 6/14 | 6/14 | 11/14 | 11/14 |
| porte 3 voisinage, 2 arêtes (phrases) | figé | 16000 | aggregate | 9/21 | 10/21 | 21/21 | 21/21 |
| porte 3 voisinage, 2 arêtes (phrases) | figé | 16000 | dispute | 26/28 | 26/28 | 28/28 | 28/28 |
| porte 3 voisinage, 2 arêtes (phrases) | figé | 16000 | single | 43/50 | 45/50 | 43/50 | 45/50 |
| porte 3 voisinage, 2 arêtes (phrases) | figé | 16000 | status | 2/21 | 2/21 | 19/21 | 19/21 |
| porte 3 voisinage, 2 arêtes (phrases) | figé | 16000 | trajectory | 1/7 | 1/7 | 6/7 | 6/7 |
| porte 3 voisinage, 2 arêtes (phrases) | figé | 16000 | unknown | 6/14 | 6/14 | 11/14 | 11/14 |
| mem0 | 12 | 8000 | aggregate | 0/21 | 2/21 | 0/21 | 5/21 |
| mem0 | 12 | 8000 | dispute | 1/28 | 1/28 | 1/28 | 1/28 |
| mem0 | 12 | 8000 | single | 1/50 | 18/50 | 1/50 | 18/50 |
| mem0 | 12 | 8000 | status | 0/21 | 0/21 | 1/21 | 1/21 |
| mem0 | 12 | 8000 | trajectory | 0/7 | 0/7 | 0/7 | 6/7 |
| mem0 | 12 | 8000 | unknown | 0/14 | 2/14 | 0/14 | 6/14 |
| mem0 | 20 | 8000 | aggregate | 0/21 | 2/21 | 0/21 | 7/21 |
| mem0 | 20 | 8000 | dispute | 1/28 | 1/28 | 1/28 | 1/28 |
| mem0 | 20 | 8000 | single | 1/50 | 18/50 | 1/50 | 18/50 |
| mem0 | 20 | 8000 | status | 0/21 | 0/21 | 1/21 | 1/21 |
| mem0 | 20 | 8000 | trajectory | 0/7 | 0/7 | 0/7 | 6/7 |
| mem0 | 20 | 8000 | unknown | 0/14 | 2/14 | 0/14 | 7/14 |
| mem0 | 40 | 8000 | aggregate | 0/21 | 2/21 | 0/21 | 7/21 |
| mem0 | 40 | 8000 | dispute | 1/28 | 1/28 | 1/28 | 1/28 |
| mem0 | 40 | 8000 | single | 1/50 | 19/50 | 1/50 | 19/50 |
| mem0 | 40 | 8000 | status | 0/21 | 0/21 | 1/21 | 1/21 |
| mem0 | 40 | 8000 | trajectory | 0/7 | 0/7 | 0/7 | 6/7 |
| mem0 | 40 | 8000 | unknown | 0/14 | 2/14 | 0/14 | 7/14 |
| mem0 | 12 | 12000 | aggregate | 0/21 | 2/21 | 0/21 | 5/21 |
| mem0 | 12 | 12000 | dispute | 1/28 | 1/28 | 1/28 | 1/28 |
| mem0 | 12 | 12000 | single | 1/50 | 18/50 | 1/50 | 18/50 |
| mem0 | 12 | 12000 | status | 0/21 | 0/21 | 1/21 | 1/21 |
| mem0 | 12 | 12000 | trajectory | 0/7 | 0/7 | 0/7 | 6/7 |
| mem0 | 12 | 12000 | unknown | 0/14 | 2/14 | 0/14 | 6/14 |
| mem0 | 20 | 12000 | aggregate | 0/21 | 2/21 | 0/21 | 7/21 |
| mem0 | 20 | 12000 | dispute | 1/28 | 1/28 | 1/28 | 1/28 |
| mem0 | 20 | 12000 | single | 1/50 | 18/50 | 1/50 | 18/50 |
| mem0 | 20 | 12000 | status | 0/21 | 0/21 | 1/21 | 1/21 |
| mem0 | 20 | 12000 | trajectory | 0/7 | 0/7 | 0/7 | 6/7 |
| mem0 | 20 | 12000 | unknown | 0/14 | 2/14 | 0/14 | 7/14 |
| mem0 | 40 | 12000 | aggregate | 0/21 | 2/21 | 0/21 | 7/21 |
| mem0 | 40 | 12000 | dispute | 1/28 | 1/28 | 1/28 | 1/28 |
| mem0 | 40 | 12000 | single | 1/50 | 19/50 | 1/50 | 19/50 |
| mem0 | 40 | 12000 | status | 0/21 | 0/21 | 1/21 | 1/21 |
| mem0 | 40 | 12000 | trajectory | 0/7 | 0/7 | 0/7 | 6/7 |
| mem0 | 40 | 12000 | unknown | 0/14 | 2/14 | 0/14 | 7/14 |
| mem0 | 12 | 16000 | aggregate | 0/21 | 2/21 | 0/21 | 5/21 |
| mem0 | 12 | 16000 | dispute | 1/28 | 1/28 | 1/28 | 1/28 |
| mem0 | 12 | 16000 | single | 1/50 | 18/50 | 1/50 | 18/50 |
| mem0 | 12 | 16000 | status | 0/21 | 0/21 | 1/21 | 1/21 |
| mem0 | 12 | 16000 | trajectory | 0/7 | 0/7 | 0/7 | 6/7 |
| mem0 | 12 | 16000 | unknown | 0/14 | 2/14 | 0/14 | 6/14 |
| mem0 | 20 | 16000 | aggregate | 0/21 | 2/21 | 0/21 | 7/21 |
| mem0 | 20 | 16000 | dispute | 1/28 | 1/28 | 1/28 | 1/28 |
| mem0 | 20 | 16000 | single | 1/50 | 18/50 | 1/50 | 18/50 |
| mem0 | 20 | 16000 | status | 0/21 | 0/21 | 1/21 | 1/21 |
| mem0 | 20 | 16000 | trajectory | 0/7 | 0/7 | 0/7 | 6/7 |
| mem0 | 20 | 16000 | unknown | 0/14 | 2/14 | 0/14 | 7/14 |
| mem0 | 40 | 16000 | aggregate | 0/21 | 2/21 | 0/21 | 7/21 |
| mem0 | 40 | 16000 | dispute | 1/28 | 1/28 | 1/28 | 1/28 |
| mem0 | 40 | 16000 | single | 1/50 | 19/50 | 1/50 | 19/50 |
| mem0 | 40 | 16000 | status | 0/21 | 0/21 | 1/21 | 1/21 |
| mem0 | 40 | 16000 | trajectory | 0/7 | 0/7 | 0/7 | 6/7 |
| mem0 | 40 | 16000 | unknown | 0/14 | 2/14 | 0/14 | 7/14 |
| mem0 | 12 | 24000 | aggregate | 0/21 | 2/21 | 0/21 | 5/21 |
| mem0 | 12 | 24000 | dispute | 1/28 | 1/28 | 1/28 | 1/28 |
| mem0 | 12 | 24000 | single | 1/50 | 18/50 | 1/50 | 18/50 |
| mem0 | 12 | 24000 | status | 0/21 | 0/21 | 1/21 | 1/21 |
| mem0 | 12 | 24000 | trajectory | 0/7 | 0/7 | 0/7 | 6/7 |
| mem0 | 12 | 24000 | unknown | 0/14 | 2/14 | 0/14 | 6/14 |
| mem0 | 20 | 24000 | aggregate | 0/21 | 2/21 | 0/21 | 7/21 |
| mem0 | 20 | 24000 | dispute | 1/28 | 1/28 | 1/28 | 1/28 |
| mem0 | 20 | 24000 | single | 1/50 | 18/50 | 1/50 | 18/50 |
| mem0 | 20 | 24000 | status | 0/21 | 0/21 | 1/21 | 1/21 |
| mem0 | 20 | 24000 | trajectory | 0/7 | 0/7 | 0/7 | 6/7 |
| mem0 | 20 | 24000 | unknown | 0/14 | 2/14 | 0/14 | 7/14 |
| mem0 | 40 | 24000 | aggregate | 0/21 | 2/21 | 0/21 | 7/21 |
| mem0 | 40 | 24000 | dispute | 1/28 | 1/28 | 1/28 | 1/28 |
| mem0 | 40 | 24000 | single | 1/50 | 19/50 | 1/50 | 19/50 |
| mem0 | 40 | 24000 | status | 0/21 | 0/21 | 1/21 | 1/21 |
| mem0 | 40 | 24000 | trajectory | 0/7 | 0/7 | 0/7 | 6/7 |
| mem0 | 40 | 24000 | unknown | 0/14 | 2/14 | 0/14 | 7/14 |
## Synthèse — budgets 4 000 / 8 000 / 12 000

Budget 12 000 caractères = 5.1 % du corpus GreenLoop.

| Fournisseur | k | budget | car. médiane | tout tient (verbatim) | tout tient (valeur) | ≥1 (verbatim) | ≥1 (valeur) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| rag_naif | 12 | 8000 | 7543 | 64/141 | 65/141 | 110/141 | 111/141 |
| brain_prod | 8 | 8000 | 2793 | 39/141 | 46/141 | 80/141 | 82/141 |
| brain_banc | figé | 8000 | 7835 | 79/141 | 81/141 | 125/141 | 126/141 |
| Brain banc (g24, réglé sur le budget) | figé | 8000 | 7877 | 39/141 | 41/141 | 93/141 | 96/141 |
| Brain banc (g36, réglé sur le budget) | figé | 8000 | 7834 | 34/141 | 36/141 | 90/141 | 93/141 |
| Brain banc (g48, réglé sur le budget) | figé | 8000 | 7838 | 38/141 | 40/141 | 88/141 | 91/141 |
| porte 3 voisinage, 1 arête (atomes) | figé | 8000 | 7869 | 79/141 | 81/141 | 125/141 | 126/141 |
| porte 3 voisinage, 2 arêtes (atomes) | figé | 8000 | 7870 | 79/141 | 81/141 | 125/141 | 126/141 |
| porte 3 voisinage, 1 arête (phrases) | figé | 8000 | 7841 | 79/141 | 81/141 | 125/141 | 126/141 |
| porte 3 voisinage, 2 arêtes (phrases) | figé | 8000 | 7841 | 79/141 | 81/141 | 125/141 | 126/141 |
| mem0 | 12 | 8000 | 3435 | 2/141 | 23/141 | 3/141 | 37/141 |
| rag_naif | 12 | 12000 | 11458 | 85/141 | 86/141 | 121/141 | 122/141 |
| brain_prod | 8 | 12000 | 2793 | 39/141 | 46/141 | 80/141 | 82/141 |
| brain_banc | figé | 12000 | 9417 | 84/141 | 87/141 | 128/141 | 130/141 |
| Brain banc (g24, réglé sur le budget) | figé | 12000 | 11824 | 67/141 | 69/141 | 112/141 | 115/141 |
| Brain banc (g36, réglé sur le budget) | figé | 12000 | 11863 | 43/141 | 46/141 | 92/141 | 96/141 |
| Brain banc (g48, réglé sur le budget) | figé | 12000 | 11860 | 39/141 | 42/141 | 91/141 | 95/141 |
| porte 3 voisinage, 1 arête (atomes) | figé | 12000 | 9914 | 84/141 | 87/141 | 128/141 | 130/141 |
| porte 3 voisinage, 2 arêtes (atomes) | figé | 12000 | 10617 | 84/141 | 87/141 | 128/141 | 130/141 |
| porte 3 voisinage, 1 arête (phrases) | figé | 12000 | 11463 | 87/141 | 90/141 | 128/141 | 130/141 |
| porte 3 voisinage, 2 arêtes (phrases) | figé | 12000 | 11723 | 87/141 | 90/141 | 128/141 | 130/141 |
| mem0 | 12 | 12000 | 3435 | 2/141 | 23/141 | 3/141 | 37/141 |
| rag_naif | 12 | 16000 | 13204 | 96/141 | 97/141 | 129/141 | 130/141 |
| brain_prod | 8 | 16000 | 2793 | 39/141 | 46/141 | 80/141 | 82/141 |
| brain_banc | figé | 16000 | 9417 | 84/141 | 87/141 | 128/141 | 130/141 |
| Brain banc (g24, réglé sur le budget) | figé | 16000 | 15832 | 83/141 | 84/141 | 129/141 | 131/141 |
| Brain banc (g36, réglé sur le budget) | figé | 16000 | 15830 | 59/141 | 63/141 | 103/141 | 107/141 |
| Brain banc (g48, réglé sur le budget) | figé | 16000 | 15820 | 52/141 | 55/141 | 94/141 | 98/141 |
| porte 3 voisinage, 1 arête (atomes) | figé | 16000 | 9914 | 84/141 | 87/141 | 128/141 | 130/141 |
| porte 3 voisinage, 2 arêtes (atomes) | figé | 16000 | 10617 | 84/141 | 87/141 | 128/141 | 130/141 |
| porte 3 voisinage, 1 arête (phrases) | figé | 16000 | 11647 | 87/141 | 90/141 | 128/141 | 130/141 |
| porte 3 voisinage, 2 arêtes (phrases) | figé | 16000 | 12494 | 87/141 | 90/141 | 128/141 | 130/141 |
| mem0 | 12 | 16000 | 3435 | 2/141 | 23/141 | 3/141 | 37/141 |
| brain_prod | 8 | 24000 | 2793 | 39/141 | 46/141 | 80/141 | 82/141 |
| Brain banc (g24, réglé sur le budget) | figé | 24000 | 19253 | 89/141 | 91/141 | 131/141 | 132/141 |
| Brain banc (g36, réglé sur le budget) | figé | 24000 | 23802 | 86/141 | 87/141 | 129/141 | 131/141 |
| Brain banc (g48, réglé sur le budget) | figé | 24000 | 23847 | 72/141 | 75/141 | 116/141 | 118/141 |
| mem0 | 12 | 24000 | 3435 | 2/141 | 23/141 | 3/141 | 37/141 |
## Référence GreenLoop (budget 12 000)

| Fournisseur | k | tout tient (verbatim) | tout tient (valeur) | ≥1 (verbatim) | ≥1 (valeur) |
| --- | --- | --- | --- | --- | --- |
| brain_prod | 8 | 39/141 | 46/141 | 80/141 | 82/141 |
| rag_naif | 12 | 85/141 | 86/141 | 121/141 | 122/141 |
| brain_banc | figé | 84/141 | 87/141 | 128/141 | 130/141 |
| mem0 | 20 | 2/141 | 23/141 | 3/141 | 40/141 |
## Comparaison à unités et budget égaux

À chaque budget cible : k ou variante dont la médiane de caractères rendus est la plus proche.

| Budget | Fournisseur | k / variante | tout tient (verbatim) | tout tient (valeur) | témoin | écart | car. médiane |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 8000 | rag_naif | 12 | 64/141 | 65/141 | 27 | 37 | 7543 |
| 8000 | brain_prod (variante k=20) | 20 | 44/141 | 54/141 | 12 | 32 | 6601 |
| 8000 | brain_banc | figé | 79/141 | 81/141 | 23 | 56 | 7835 |
| 8000 | Brain banc (g24, réglé sur le budget) | figé | 39/141 | 41/141 | 15 | 24 | 7877 |
| 8000 | Brain banc (g36, réglé sur le budget) | figé | 34/141 | 36/141 | 12 | 22 | 7834 |
| 8000 | Brain banc (g48, réglé sur le budget) | figé | 38/141 | 40/141 | 15 | 23 | 7838 |
| 8000 | porte 3 voisinage, 1 arête (atomes) | figé | 79/141 | 81/141 | 23 | 56 | 7869 |
| 8000 | porte 3 voisinage, 2 arêtes (atomes) | figé | 79/141 | 81/141 | 23 | 56 | 7870 |
| 8000 | porte 3 voisinage, 1 arête (phrases) | figé | 79/141 | 81/141 | 23 | 56 | 7841 |
| 8000 | porte 3 voisinage, 2 arêtes (phrases) | figé | 79/141 | 81/141 | 23 | 56 | 7841 |
| 8000 | mem0 | 40 | 2/141 | 24/141 | 0 | 2 | 7844 |
| 12000 | rag_naif | 12 | 85/141 | 86/141 | 46 | 39 | 11458 |
| 12000 | brain_prod (variante k=20) | 20 | 44/141 | 54/141 | 12 | 32 | 6601 |
| 12000 | brain_banc | figé | 84/141 | 87/141 | 23 | 61 | 9417 |
| 12000 | Brain banc (g24, réglé sur le budget) | figé | 67/141 | 69/141 | 25 | 42 | 11824 |
| 12000 | Brain banc (g36, réglé sur le budget) | figé | 43/141 | 46/141 | 17 | 26 | 11863 |
| 12000 | Brain banc (g48, réglé sur le budget) | figé | 39/141 | 42/141 | 17 | 22 | 11860 |
| 12000 | porte 3 voisinage, 1 arête (atomes) | figé | 84/141 | 87/141 | 23 | 61 | 9914 |
| 12000 | porte 3 voisinage, 2 arêtes (atomes) | figé | 84/141 | 87/141 | 23 | 61 | 10617 |
| 12000 | porte 3 voisinage, 1 arête (phrases) | figé | 87/141 | 90/141 | 28 | 59 | 11463 |
| 12000 | porte 3 voisinage, 2 arêtes (phrases) | figé | 87/141 | 90/141 | 29 | 58 | 11723 |
| 12000 | mem0 | 40 | 2/141 | 24/141 | 0 | 2 | 11370 |
| 16000 | rag_naif | 12 | 96/141 | 97/141 | 54 | 42 | 13204 |
| 16000 | brain_prod (variante k=20) | 20 | 44/141 | 54/141 | 12 | 32 | 6601 |
| 16000 | brain_banc | figé | 84/141 | 87/141 | 23 | 61 | 9417 |
| 16000 | Brain banc (g24, réglé sur le budget) | figé | 83/141 | 84/141 | 31 | 52 | 15832 |
| 16000 | Brain banc (g36, réglé sur le budget) | figé | 59/141 | 63/141 | 25 | 34 | 15830 |
| 16000 | Brain banc (g48, réglé sur le budget) | figé | 52/141 | 55/141 | 20 | 32 | 15820 |
| 16000 | porte 3 voisinage, 1 arête (atomes) | figé | 84/141 | 87/141 | 23 | 61 | 9914 |
| 16000 | porte 3 voisinage, 2 arêtes (atomes) | figé | 84/141 | 87/141 | 23 | 61 | 10617 |
| 16000 | porte 3 voisinage, 1 arête (phrases) | figé | 87/141 | 90/141 | 28 | 59 | 11647 |
| 16000 | porte 3 voisinage, 2 arêtes (phrases) | figé | 87/141 | 90/141 | 29 | 58 | 12494 |
| 16000 | mem0 | 40 | 2/141 | 24/141 | 0 | 2 | 11370 |

### Plafond de rendu

- brain_banc : budget 12000 (au-delà, la médiane de caractères rendus ne croît plus)
- Brain banc (g24, réglé sur le budget) : budget 24000 (au-delà, la médiane de caractères rendus ne croît plus)
- Brain banc (g36, réglé sur le budget) : budget 24000 (au-delà, la médiane de caractères rendus ne croît plus)
- Brain banc (g48, réglé sur le budget) : budget 24000 (au-delà, la médiane de caractères rendus ne croît plus)
- porte 3 voisinage, 1 arête (atomes) : budget 12000 (au-delà, la médiane de caractères rendus ne croît plus)
- porte 3 voisinage, 2 arêtes (atomes) : budget 12000 (au-delà, la médiane de caractères rendus ne croît plus)
- porte 3 voisinage, 1 arête (phrases) : budget 16000 (au-delà, la médiane de caractères rendus ne croît plus)
- porte 3 voisinage, 2 arêtes (phrases) : budget 16000 (au-delà, la médiane de caractères rendus ne croît plus)
- brain_prod : budget 8000 (au-delà, la médiane de caractères rendus ne croît plus)
- mem0 : budget 12000 (au-delà, la médiane de caractères rendus ne croît plus)
- rag_naif : budget 16000 (au-delà, la médiane de caractères rendus ne croît plus)

## Disputes — réglage / écart

| Fournisseur | k | budget | 2 côtés (verbatim) | 2 côtés (valeur) | réglage (verbatim) | réglage (valeur) | écart (verbatim) | écart (valeur) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| rag_naif | 12 | 8000 | 2/28 | 2/28 | 1/14 | 1/14 | 1/14 | 1/14 |
| rag_naif | 12 | 12000 | 14/28 | 14/28 | 8/14 | 8/14 | 6/14 | 6/14 |
| rag_naif | 12 | 16000 | 22/28 | 22/28 | 13/14 | 13/14 | 9/14 | 9/14 |
| brain_prod | 8 | 8000 | 1/28 | 1/28 | 0/14 | 0/14 | 1/14 | 1/14 |
| brain_prod (variante k=12) | 12 | 8000 | 3/28 | 3/28 | 1/14 | 1/14 | 2/14 | 2/14 |
| brain_prod (variante k=20) | 20 | 8000 | 3/28 | 3/28 | 1/14 | 1/14 | 2/14 | 2/14 |
| brain_prod (variante k=40) | 40 | 8000 | 3/28 | 3/28 | 1/14 | 1/14 | 2/14 | 2/14 |
| brain_prod | 8 | 12000 | 1/28 | 1/28 | 0/14 | 0/14 | 1/14 | 1/14 |
| brain_prod (variante k=12) | 12 | 12000 | 3/28 | 3/28 | 1/14 | 1/14 | 2/14 | 2/14 |
| brain_prod (variante k=20) | 20 | 12000 | 3/28 | 3/28 | 1/14 | 1/14 | 2/14 | 2/14 |
| brain_prod (variante k=40) | 40 | 12000 | 3/28 | 3/28 | 1/14 | 1/14 | 2/14 | 2/14 |
| brain_prod | 8 | 16000 | 1/28 | 1/28 | 0/14 | 0/14 | 1/14 | 1/14 |
| brain_prod (variante k=12) | 12 | 16000 | 3/28 | 3/28 | 1/14 | 1/14 | 2/14 | 2/14 |
| brain_prod (variante k=20) | 20 | 16000 | 3/28 | 3/28 | 1/14 | 1/14 | 2/14 | 2/14 |
| brain_prod (variante k=40) | 40 | 16000 | 3/28 | 3/28 | 1/14 | 1/14 | 2/14 | 2/14 |
| brain_prod | 8 | 24000 | 1/28 | 1/28 | 0/14 | 0/14 | 1/14 | 1/14 |
| brain_prod (variante k=12) | 12 | 24000 | 3/28 | 3/28 | 1/14 | 1/14 | 2/14 | 2/14 |
| brain_prod (variante k=20) | 20 | 24000 | 3/28 | 3/28 | 1/14 | 1/14 | 2/14 | 2/14 |
| brain_prod (variante k=40) | 40 | 24000 | 3/28 | 3/28 | 1/14 | 1/14 | 2/14 | 2/14 |
| brain_banc | figé | 8000 | 24/28 | 24/28 | 13/14 | 13/14 | 11/14 | 11/14 |
| brain_banc | figé | 12000 | 24/28 | 24/28 | 13/14 | 13/14 | 11/14 | 11/14 |
| brain_banc | figé | 16000 | 24/28 | 24/28 | 13/14 | 13/14 | 11/14 | 11/14 |
| Brain banc (g24, réglé sur le budget) | figé | 8000 | 9/28 | 9/28 | 4/14 | 4/14 | 5/14 | 5/14 |
| Brain banc (g24, réglé sur le budget) | figé | 12000 | 24/28 | 24/28 | 13/14 | 13/14 | 11/14 | 11/14 |
| Brain banc (g24, réglé sur le budget) | figé | 16000 | 24/28 | 24/28 | 13/14 | 13/14 | 11/14 | 11/14 |
| Brain banc (g24, réglé sur le budget) | figé | 24000 | 25/28 | 25/28 | 14/14 | 14/14 | 11/14 | 11/14 |
| Brain banc (g36, réglé sur le budget) | figé | 8000 | 6/28 | 6/28 | 3/14 | 3/14 | 3/14 | 3/14 |
| Brain banc (g36, réglé sur le budget) | figé | 12000 | 13/28 | 13/28 | 6/14 | 6/14 | 7/14 | 7/14 |
| Brain banc (g36, réglé sur le budget) | figé | 16000 | 24/28 | 24/28 | 13/14 | 13/14 | 11/14 | 11/14 |
| Brain banc (g36, réglé sur le budget) | figé | 24000 | 25/28 | 25/28 | 14/14 | 14/14 | 11/14 | 11/14 |
| Brain banc (g48, réglé sur le budget) | figé | 8000 | 11/28 | 11/28 | 6/14 | 6/14 | 5/14 | 5/14 |
| Brain banc (g48, réglé sur le budget) | figé | 12000 | 11/28 | 11/28 | 6/14 | 6/14 | 5/14 | 5/14 |
| Brain banc (g48, réglé sur le budget) | figé | 16000 | 22/28 | 22/28 | 11/14 | 11/14 | 11/14 | 11/14 |
| Brain banc (g48, réglé sur le budget) | figé | 24000 | 24/28 | 24/28 | 13/14 | 13/14 | 11/14 | 11/14 |
| porte 3 voisinage, 1 arête (atomes) | figé | 8000 | 24/28 | 24/28 | 13/14 | 13/14 | 11/14 | 11/14 |
| porte 3 voisinage, 1 arête (atomes) | figé | 12000 | 24/28 | 24/28 | 13/14 | 13/14 | 11/14 | 11/14 |
| porte 3 voisinage, 1 arête (atomes) | figé | 16000 | 24/28 | 24/28 | 13/14 | 13/14 | 11/14 | 11/14 |
| porte 3 voisinage, 2 arêtes (atomes) | figé | 8000 | 24/28 | 24/28 | 13/14 | 13/14 | 11/14 | 11/14 |
| porte 3 voisinage, 2 arêtes (atomes) | figé | 12000 | 24/28 | 24/28 | 13/14 | 13/14 | 11/14 | 11/14 |
| porte 3 voisinage, 2 arêtes (atomes) | figé | 16000 | 24/28 | 24/28 | 13/14 | 13/14 | 11/14 | 11/14 |
| porte 3 voisinage, 1 arête (phrases) | figé | 8000 | 24/28 | 24/28 | 13/14 | 13/14 | 11/14 | 11/14 |
| porte 3 voisinage, 1 arête (phrases) | figé | 12000 | 26/28 | 26/28 | 14/14 | 14/14 | 12/14 | 12/14 |
| porte 3 voisinage, 1 arête (phrases) | figé | 16000 | 26/28 | 26/28 | 14/14 | 14/14 | 12/14 | 12/14 |
| porte 3 voisinage, 2 arêtes (phrases) | figé | 8000 | 24/28 | 24/28 | 13/14 | 13/14 | 11/14 | 11/14 |
| porte 3 voisinage, 2 arêtes (phrases) | figé | 12000 | 26/28 | 26/28 | 14/14 | 14/14 | 12/14 | 12/14 |
| porte 3 voisinage, 2 arêtes (phrases) | figé | 16000 | 26/28 | 26/28 | 14/14 | 14/14 | 12/14 | 12/14 |
| mem0 | 12 | 8000 | 1/28 | 1/28 | 0/14 | 0/14 | 1/14 | 1/14 |
| mem0 | 20 | 8000 | 1/28 | 1/28 | 0/14 | 0/14 | 1/14 | 1/14 |
| mem0 | 40 | 8000 | 1/28 | 1/28 | 0/14 | 0/14 | 1/14 | 1/14 |
| mem0 | 12 | 12000 | 1/28 | 1/28 | 0/14 | 0/14 | 1/14 | 1/14 |
| mem0 | 20 | 12000 | 1/28 | 1/28 | 0/14 | 0/14 | 1/14 | 1/14 |
| mem0 | 40 | 12000 | 1/28 | 1/28 | 0/14 | 0/14 | 1/14 | 1/14 |
| mem0 | 12 | 16000 | 1/28 | 1/28 | 0/14 | 0/14 | 1/14 | 1/14 |
| mem0 | 20 | 16000 | 1/28 | 1/28 | 0/14 | 0/14 | 1/14 | 1/14 |
| mem0 | 40 | 16000 | 1/28 | 1/28 | 0/14 | 0/14 | 1/14 | 1/14 |
| mem0 | 12 | 24000 | 1/28 | 1/28 | 0/14 | 0/14 | 1/14 | 1/14 |
| mem0 | 20 | 24000 | 1/28 | 1/28 | 0/14 | 0/14 | 1/14 | 1/14 |
| mem0 | 40 | 24000 | 1/28 | 1/28 | 0/14 | 0/14 | 1/14 | 1/14 |
## Coûts (estimations / journaux)

| Poste | Source | Détail |
| --- | --- | --- |
| mem0 ingestion (cursor) | a-blanc | quota Cursor, 61 appels prévus |
| mem0 contextes (cursor) | a-blanc | 141 embeddings · 0.0141 € |
| mem0 ingestion (.a-blanc) | a-blanc | 61 appels · 0.3904 € |
| mem0 contextes (.a-blanc) | a-blanc | 141 embeddings · 0.0141 € |

Notes :
- `brain_banc` : k ignoré (configuration `hybride_fenetres_g12`, arrivé tel quel).
- `brain_banc (fenêtre calibrée sur l'or)` : k ignoré (configuration `hybride_fenetres_calibrees`, cache séparé).
- `Brain banc (g24/g36/g48, réglé sur le budget)` : k ignoré (configurations `hybride_fenetres_g24` / `g36` / `g48` ; réglée sur le budget, pas comparable au réglage GreenLoop d'origine).
- `brain_prod` : ligne de production à k=8 ; autres k = variantes contre-factuelles.
- mem0 / Letta archive : requête = texte de la question tel quel.

