# Planning, découpage des tâches et matrice des responsabilités

*Jalon de fin de séance 2 · hypothèse : groupe de 4 membres (A, B, C, D), à adapter*

## 1. Rôles

| Rôle | Séances 1-2 | Séances 3-5 (rotation en S3) | Missions |
|---|---|---|---|
| **CP** Chef de projet | [A] | [B] | Planning, répartition, suivi des écarts, ordre du jour |
| **RQ** Resp. qualité et validation technique | [B] | [C] | Conventions, contrôles, dossier de validation, relecture croisée |
| **RC** Resp. relation commanditaire | [C] | [D] | Entretiens, demandes de validation, CR sous 48 h |
| Contributeur | [D] | [A] | Production (tous les membres produisent) |

La rotation se fait avec une **fiche de passation** (½ page par rôle : où en est-on, ce qui est en attente, contacts).

## 2. Découpage des tâches (WBS) et charge estimée

Budget : 4 intervalles × 3 h × 4 personnes = **48 h** de travail personnel, plus le temps en séance. La v1 des livrables étant rédigée, la charge porte surtout sur l'**appropriation**, la **validation**, les **tests** et la **soutenance**.

| Lot | Tâche | Charge (h) | Intervalle | Dépend de |
|---|---|---|---|---|
| **L0 Pilotage** | CR de réunion (×5) | 2,5 | tous | — |
| | Mise à jour du registre des risques (×4) | 2 | tous | — |
| | Fiches de passation des rôles | 1,5 | S2→S3 | — |
| **L1 Cadrage** | Relire et adapter note de cadrage et profils | 3 | avant S1 / S1→S2 | — |
| **L2 Réglementaire** | Vérifier les références citées, finaliser la page | 3 | S1→S2 | L1 |
| | Faire valider par le commanditaire | 0,5 | S2→S3 | — |
| **L3 Indicateur** | S'approprier le script, relancer `--offline`, recalculer un exemple à la main (tableur) | 4 | S1→S2 | — |
| | Rédiger les conventions techniques (pour le directeur du master) | 2 | S1→S2 | L3 |
| | Intégrer les retours de S2 (horizon, niveau, règle de prudence) | 2 | S2→S3 | validation S2 |
| **L4 Maquette** | Revue des 6 écrans, ajustements de textes | 3 | S1→S2 | L1, L3 |
| | (Si exigé) reproduction dans Figma | 3 | S2→S3 | décision S1 |
| **L5 Tests** | Recruter 3 + 1 participants | 1,5 | S2→S3 | — |
| | Faire passer les 3 tests (2 personnes × 30 min × 3) | 3 | S2→S3 | L4 |
| | Analyser, décider et appliquer les corrections | 4 | S3→S4 | tests |
| | Re-test de l'étape 3 si besoin | 1 | S3→S4 | corrections |
| **L6 Feuille de route** | Revue de la proposition V1 / V2 / V3 | 1,5 | S3→S4 | L5 |
| **L7 Validation technique** | Préparer la relecture croisée (grille, code, données gelées) | 2 | S3→S4 | L3 |
| | Relire le livrable du projet 5 | — (en séance) | S4 | — |
| | Dossier de validation technique | 3 | S3→S4 | L7 |
| **L8 Soutenance** | Support de 12 min + répétition chronométrée | 6 | S4→S5 | tout |
| | Retour d'expérience (2 pages) | 3 | S4→S5 | tout |
| | **Total** | **≈ 52 h** | | |

**Écart** : ≈ 52 h estimées pour 48 h disponibles. Leviers prévus : la reproduction Figma (3 h) n'a lieu que si elle est exigée ; le re-test (1 h) n'a lieu que si le critère n'est pas atteint.

## 3. Planning

| Tâche | Avant S1 | S1→S2 | S2→S3 | S3→S4 | S4→S5 |
|---|---|---|---|---|---|
| Note de cadrage | ■ | ■ | | | |
| Page réglementaire | | ■ | ■ (validation) | | |
| Indicateur : appropriation + conventions | | ■ | ■ | | |
| Maquette | | ■ | ■ | ■ (corrections) | |
| Tests utilisateurs | | | ■ | ■ | |
| Feuille de route | | | | ■ | |
| Relecture croisée + dossier de validation | | | | ■ | |
| Soutenance + retour d'expérience | | | | | ■ |
| Pilotage (CR, risques) | ■ | ■ | ■ | ■ | ■ |

Dates des séances : S1 [__/__], S2 [__/__], S3 [__/__], S4 [__/__], S5 [__/__].

## 4. Matrice des responsabilités (RACI)

R = réalise · A = approuve (un seul) · C = consulté · I = informé

| Livrable | CP | RQ | RC | Contributeur(s) | Commanditaire | Projet 5 / Dir. master |
|---|---|---|---|---|---|---|
| Note de cadrage | A | C | R | R | A (validation) | I |
| Planning, RACI | R/A | C | C | C | I | I (directeur) |
| Registre des risques | R/A | C | C | C | I | — |
| Comptes rendus | C | I | R/A | I | I | — |
| Profils utilisateurs | C | C | R | R/A | C | — |
| Page réglementaire | I | C | R | R | A (validation) | — |
| Spécification de l'indicateur | I | A | C | R | C (horizon, niveau) | C |
| Calcul Python | I | A | I | R | I | C (réexécution) |
| Maquette | C | C | C | R/A | C | — |
| Tests utilisateurs + corrections | C | A | R (recrutement) | R | I | — |
| Feuille de route | A | C | R | R | C | — |
| Dossier de validation technique | I | R/A | I | C | I | C (relecture) / I (avis) |
| Soutenance, retour d'expérience | A | R | R | R | I | I |

Note : la colonne « Commanditaire » indique sa validation formelle quand le cahier des charges l'exige. En interne, un seul A par ligne.
