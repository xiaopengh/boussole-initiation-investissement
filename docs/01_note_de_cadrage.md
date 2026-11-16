# Note de cadrage — Projet 1 : Boussole, application d'initiation à l'investissement

*Jalon de fin de séance 1 · version 1 · à valider par le commanditaire*

| | |
|---|---|
| **Groupe** | [noms des membres] |
| **Commanditaire** | Directeur produit, fintech Tradinvest |
| **Chef de projet / Resp. qualité / Resp. relation commanditaire** (jusqu'à la séance 3) | [nom] / [nom] / [nom] |
| **Date** | [jj/mm/2026] |

## 1. Contexte

Beaucoup de particuliers commencent à investir sans mesurer ce qu'ils peuvent perdre, souvent attirés par des contenus de réseaux sociaux qui mettent en avant les gains. Tradinvest veut une application **pédagogique, en argent virtuel**, qui apprenne à comprendre le risque **avant** de placer un euro réel. L'application n'exécutera aucun ordre réel. On nous demande la **conception** (utilisateurs, cadre réglementaire, écrans, indicateur de risque), pas le développement.

## 2. Objectifs

1. Concevoir une application qui fait comprendre à un débutant **combien il pourrait perdre, en euros**, avec un indicateur juste scientifiquement.
2. Respecter le cadre de la communication financière auprès des particuliers (AMF) : aucune promesse de gain, risques présentés clairement.
3. Démontrer par des tests que l'indicateur est compris (**au moins 2 utilisateurs sur 3**).

## 3. Périmètre

| Périmètre minimal (obligatoire) | État de la v1 |
|---|---|
| Deux profils d'utilisateurs, avec besoins et craintes | Rédigé : `02_profils_utilisateurs.md` |
| Page réglementaire : ce que l'application peut / ne peut pas faire | Rédigée : `03_page_reglementaire.md` (à valider) |
| Maquette cliquable de 5 à 6 écrans | Réalisée : `maquette/index.html` (outil à confirmer, voir §7) |
| Spécification de l'indicateur VaR (définition, calcul, formulation) | Rédigée : `04_specification_indicateur_risque.md` |
| Test auprès de 3 utilisateurs non spécialistes + corrections | Protocole prêt : `06_protocole_test_utilisateurs.md` ; **tests à réaliser** |

| Bonus (après le minimum) | État |
|---|---|
| Calcul de l'indicateur en Python sur 3 ou 4 portefeuilles types | Réalisé : `python/var_indicateur.py` (4 portefeuilles) |
| Feuille de route en trois versions | Rédigée : `07_feuille_de_route.md` |

**Hors périmètre** : développement de l'application, argent réel, exécution d'ordres, conseil personnalisé, crypto-actifs, produits à effet de levier, analyse juridique approfondie, données de nos employeurs.

## 4. Parties prenantes

| Partie prenante | Rôle | Attente principale | Mode d'échange |
|---|---|---|---|
| Directeur produit Tradinvest (commanditaire) | Valide note de cadrage, portefeuilles, paramètres, page réglementaire | Une conception juste, compréhensible, non incitative | Réunions de séance + CR sous 48 h |
| Équipe projet | Produit les livrables | Charge ≤ 3 h par personne entre deux séances | Espace partagé, point hebdomadaire |
| Groupe du projet 5 (mesure du risque de marché) | Relecture croisée en séance 4 ; questions techniques en séance 5 | Indicateur juste, code réexécutable | Séance 4 (45 min, grille commune) |
| Directeur du master | Avis écrit sur conventions (après S2) et dossier de validation (avant S5) | Rigueur, traçabilité | Dépôt des documents |
| Utilisateurs test (3 + 1 réserve) | Testent la maquette | Séance courte, anonyme | Entretiens de 30 min |
| Futurs utilisateurs (profils Léa et Nadia) | Bénéficiaires finaux | Comprendre sans être poussés à spéculer | Représentés par les profils |

## 5. Livrables et jalons

| Séance | Jalon | Livrables |
|---|---|---|
| S1 Lancement | Note de cadrage validée | Cette note ; proposition des 4 portefeuilles types |
| S2 Planification | Planning et registre des risques présentés | `08_planning_et_raci.md`, `09_registre_des_risques.md`, conventions techniques ; validation horizon (1 mois) et niveau (95 %) |
| S3 Mi-parcours | Démonstration intermédiaire + plan d'action | Maquette, indicateur calculé, premiers tests ; rotation des rôles |
| S4 Recette | Livrable figé + dossier de validation technique | Relecture croisée avec le projet 5 ; `10_dossier_validation_technique.md` |
| S5 Soutenance | Évaluation finale | 12 min de présentation + 8 min de questions ; retour d'expérience de 2 pages |

## 6. Critères de réussite

| Critère | Mesure | Cible |
|---|---|---|
| Indicateur compris | Grille d'interprétation (test, étape 3) | ≥ 2 participants sur 3 |
| Écrans utiles | Matrice écrans ↔ besoins des profils | 100 % des écrans reliés à un besoin |
| Conformité | Validation de la page réglementaire par le commanditaire | Validée avant S4 |
| Justesse scientifique | Backtest (Kupiec) ; relecture croisée du projet 5 | Non rejeté à 5 % ; remarques traitées |
| Non-incitation | Débriefing « envie d'investir tout de suite » | ≤ 2/5 en moyenne |
| Pilotage | CR sous 48 h, registre des risques à jour à chaque séance | 100 % |

## 7. Hypothèses, contraintes, décisions à obtenir

- **Contraintes** : aucun budget ; outils gratuits ; données publiques uniquement ; 3 h de travail personnel par étudiant entre deux séances.
- **À valider en S1** : les 4 portefeuilles types (Prudent 20/60/20, Équilibré 50/40/10, Dynamique 80/20/0, 100 % actions) et leurs indices.
- **À valider en S2** : horizon 1 mois, niveau 95 %, règle de prudence (max de l'historique complet et des 5 dernières années), arrondi par excès.
- **À confirmer** : la maquette HTML est-elle acceptée, ou faut-il la reproduire dans Figma, Canva ou PowerPoint ?
- **Hypothèse** : la marque de l'application (« Boussole ») est une proposition ; Tradinvest peut la renommer.
