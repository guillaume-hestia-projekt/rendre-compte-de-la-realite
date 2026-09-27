# RAPPORT B02r3 — reprise 2 (dernière) de l'or GreenLoop

Annotateur: grok · 2026-09-08 · `annotation.blind`: true  
Fichier: `gold/situations.json` (`gold-situations/1.1.0`). Lecture limitée à `dossiers/greenloop/{README.md,manifest.json,documents/,gold/}` et au protocole §2 bis.

## Les six, une par ligne

`gl-tr0004` CONSERVÉE · stated_succession · 07 p.1 « Use this table for service after 2025-09-08, including the September closing invoice. » (taux imprimé/interne ; 02 p.2 n'est pas une version : une grille interne n'amende pas l'accord.)
`gl-tr0005` SUPPRIMÉE · identité · 11 p.1 « Issuer: Mosswheel Services Ltd » / 14 p.1 « Issuer: GreenLoop Collect Ltd » — aucune pièce n'énonce la succession, aucune n'a pouvoir sur l'autre.
`gl-tr0006` CONSERVÉE · stated_succession · 24 p.6 « The certificate names both facilities because its reporting window spans the change in receiving route. » (20 p.1 : « From 2024-07 the account notes identify Cinderbank Organics Ltd… »)
`gl-tr0008` CONSERVÉE · stated_succession · 05 p.1 « September restart announced by operations: **Roast Kitchen and Quarry Tower only, from 2025-09-09**. »
`gl-tr0009` SUPPRIMÉE · date inconnue · 08 énonce le changement (« after management's requested issuer change ») mais v1 a `validity_start` null : une version sans date n'est pas une version.
`gl-tr0011` CONSERVÉE · stated_succession · 08 p.1 « Its earlier estimate remains 1.287 t. »

## Supprimées — sort des assertions

`gl-tr0005` : `gl-a1929` (gl-s0520) et `gl-a1990` (gl-s0524) restent, sans lien. Inconnue `gl-u0017`.
`gl-tr0009` : `gl-a1745` (gl-s0499) et `gl-a2066` (gl-s0550) restent, sans lien. `trajectory` nul sur gl-s0499 / gl-s0500 / gl-s0550. Inconnue `gl-u0018`.

## validity_end posées (3)

`gl-a1736` et `gl-a1997` (14.83) → `2025-09-08` (début de 24.67), pas à l'émission de mars. `gl-a1162` (clôture) → `2025-09-09`. Déjà en place : Fenroot `2024-06`, estimation mars `2025-06-18`. Pas de fin sur `gl-a1735` : INV-2025-086 imprime le même 24.67.

## Ce que je n'ai PAS vérifié

- Le verbatim des 2 403 citations et les 765 ancrages temporels (reprise 1, directeur).
- L'arithmétique interne, le recompte CSV, `questions.json` / `tensions.json` (absents).
- Les pièces hors de celles citées par les six trajectoires, au-delà du test.

{"verdict":"OK","trajectoires_conservees":4,"trajectoires_supprimees":2,"validity_end_posees":3,"heures":1.5}
