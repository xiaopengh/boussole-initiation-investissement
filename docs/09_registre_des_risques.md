# Registre des risques du projet

*Présenté en séance 2 · mis à jour à chaque séance · responsable de la tenue : CP*

Probabilité (P) et impact (I) notés de 1 (faible) à 3 (fort). **Criticité = P × I** ; ≥ 6 = à traiter en priorité, revu à chaque séance.

| # | Risque | P | I | Criticité | Parade (prévention / plan B) | Resp. | Statut |
|---|---|---|---|---|---|---|---|
| R1 | Moins de 2 testeurs sur 3 interprètent correctement l'indicateur | 2 | 3 | **6** | Pictogramme + encadré « pas un maximum » ; tests dès S2→S3 pour garder du temps de correction ; variantes de formulation prêtes (protocole §8) ; re-test sur un nouveau participant | RQ | Ouvert |
| R2 | Erreur de calcul ou code non reproductible détectée à la relecture croisée | 2 | 3 | **6** | Données gelées (`prix.csv`), mode `--offline`, contrôles automatiques (`controles.txt`), tests unitaires, recalcul d'un exemple au tableur avant S4 | RQ | Ouvert, atténué |
| R3 | Indicateur scientifiquement contestable (sous-estimation du risque) | 2 | 3 | **6** | Backtest de Kupiec et Christoffersen ; **constat** : l'historique seul est rejeté pour le Prudent → règle de prudence adoptée ; limites documentées (dépassements groupés en 2022) | RQ | **Survenu, traité** |
| R4 | Page réglementaire non validée par le commanditaire | 2 | 3 | **6** | Envoi dès S2 ; liste fermée de 5 points à valider ; ne pas prétendre faire une analyse juridique | RC | Ouvert |
| R5 | Validations du commanditaire tardives | 2 | 3 | **6** | Calendrier des validations annoncé en S1 ; CR sous 48 h avec « décisions attendues » ; relance à J+5 | RC | Ouvert |
| R6 | Dépassement des 3 h de travail personnel par intervalle | 3 | 2 | **6** | Charges estimées par tâche (écart connu de 4 h) ; Figma et re-test seulement si nécessaires ; priorité au minimum | CP | Ouvert |
| R7 | Recrutement difficile de 3 testeurs vraiment non spécialistes | 2 | 2 | 4 | Recruter dès S2, hors master et hors finance ; 1 participant de réserve ; test à distance possible | RC | Ouvert |
| R8 | Biais de recrutement (testeurs trop jeunes ou trop à l'aise) | 2 | 2 | 4 | Critères d'éligibilité ; au moins un participant de plus de 45 ans (profil Nadia) | RQ | Ouvert |
| R9 | Maquette HTML refusée (Figma, Canva ou PowerPoint attendus) | 2 | 2 | 4 | Confirmer en S1 ; plan B : reproduire les 6 écrans dans Figma à partir de captures (≈ 3 h) | RC | Ouvert |
| R10 | Source de données indisponible ou modifiée (`yfinance` n'est pas une API officielle) | 2 | 2 | 4 | Cours gelés dans le dépôt ; date de gel documentée ; source alternative : sites des émetteurs | RQ | Atténué |
| R11 | Glissement du périmètre (bonus avant le minimum) | 2 | 2 | 4 | Règle « minimum d'abord » ; revue du périmètre en début de séance | CP | Ouvert |
| R12 | Absence d'un membre ou passation de rôles ratée en S3 | 2 | 2 | 4 | Fiches de passation ; documents uniques dans l'espace partagé ; binômes sur les tâches critiques | CP | Ouvert |
| R13 | Maquette perçue comme incitative (ludification, mise en avant des gains) | 1 | 3 | 3 | Liste anti-incitation (`05_maquette_ecrans.md`) ; question de débriefing « envie d'investir » | RQ | Ouvert |
| R14 | Indicateur instable d'un mois sur l'autre, ce qui trouble l'utilisateur | 2 | 1 | 2 | Règle de prudence sur fenêtres longues ; arrondi à 2 chiffres significatifs ; mention « mis à jour chaque mois » | RQ | Ouvert |
| R15 | Utilisation de données de l'employeur d'un membre | 1 | 3 | 3 | Rappel en S1 ; seules les données publiques listées dans les conventions sont autorisées | RQ | Ouvert |

## Historique des mises à jour

| Séance | Changements |
|---|---|
| S2 | Création du registre. R3 survenu lors du premier backtest et traité par la règle de prudence. |
| S3 | |
| S4 | |
| S5 | |
