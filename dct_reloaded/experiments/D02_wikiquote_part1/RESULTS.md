# D02 — Partie 1 : K2 tirée d'une phrase de Wikiquote — résultats (2026-10-04)

Pré-inscription : `PREREGISTRATION.md`. Sorties : `logs/`.

| Base | Clés | Essais (K2 × w1) | Durée | IDP maximale | Candidats ≥ 0,30 |
|---|---:|---:|---:|---:|---:|
| contrôles plantés (vraie K2 parmi 200 000 leurres) | | | | **0,40–0,45** (5/5 en tête) | |
| « prefix » : débuts de phrase en mots entiers | 8 481 956 | 38 076 364 | 36 min | **0,205** | **0** |
| « trunc » + « windows » (20–27 premières lettres ; toute suite de mots entiers de 20–27 lettres) — GitHub Actions, 20 machines | **112 856 857** | **507 005 605** | 40 min | **0,209** | **0** |

Base « prefix » : **aucun candidat** ; le maximum (0,205, « heyifyouregivingoutfree », w1 = 27) est au niveau des
meilleurs leurres des contrôles (0,19–0,25). K2 n'est pas un début de phrase de Wikiquote en mots entiers.

Bases « trunc » et « windows » (avenant de la pré-inscription), calculées sur GitHub Actions (run 37183957616,
`logs/actions_run_37183957616.md`) : **aucun candidat** ; le maximum (0,209, « marigoldbragabouthow », w1 = 27) est encore
au niveau du bruit. Tout se passe à w1 = 27, la plus grande largeur, où le plafond du bruit est le plus haut.

## Conclusion (critère pré-inscrit)
K2 de *DCT Reloaded 1* n'est **aucune suite de mots de Wikiquote anglais** (début de phrase, phrase coupée à 20–27
lettres, ou suite de mots entiers prise n'importe où) : 121 millions de clés distinctes, 545 millions d'essais, aucune
au-dessus de 0,21 alors qu'une vraie K2 donne 0,40–0,45 (contrôles 5/5). Le workflow `phrase-scan` (20 machines)
a fait en 40 minutes ce qui aurait pris environ deux jours sur le conteneur.
