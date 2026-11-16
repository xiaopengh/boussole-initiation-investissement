# Feuille de route de lancement en trois versions

*Livrable bonus · proposition à discuter avec le commanditaire*

Principe : chaque version **apprend quelque chose de plus** à l'utilisateur. Aucune version n'ajoute d'incitation à investir. On ne passe à la version suivante que si les **critères de passage** sont atteints.

| | **V1 « Comprendre »** | **V2 « S'entraîner »** | **V3 « Se préparer à investir »** |
|---|---|---|---|
| **Objectif** | Comprendre ce que l'on peut perdre avant d'investir | Tester ses propres choix de répartition en argent virtuel | Passer de l'apprentissage à une décision réelle éclairée, prise ailleurs |
| **Contenu** | Les 6 écrans de la maquette : 4 portefeuilles types, indicateur « 1 cas sur 20 », écran Comprendre, Rejouer 2020 et 2022, quiz, règles du jeu, glossaire | Portefeuille virtuel **composable** (curseurs actions / obligations / monétaire, une dizaine d'indices larges) avec l'indicateur **recalculé en direct** ; épisodes supplémentaires (2008, 2011, 2015, 2018) ; effet des **frais** et de l'**inflation** ; comparaison Livret A ; parcours de leçons courtes | Lire un **vrai DIC** (indicateur officiel de 1 à 7) ; auto-évaluation « quelle perte puis-je supporter ? » (sans recommandation de produit) ; checklist avant d'investir (vérifier l'agrément AMF / ORIAS, frais, horizon) ; mode classe / enseignant |
| **Ce qui reste exclu** | Argent réel, ordres, conseil, crypto, produits à effet de levier | idem ; pas de classement entre utilisateurs | idem ; toute **passerelle** vers une offre réelle exige une revue juridique et conformité (changement possible de statut réglementaire) |
| **Données** | 4 portefeuilles figés, recalcul mensuel | Calcul côté serveur pour les combinaisons libres, mêmes conventions | Bibliothèque de DIC publics |
| **Mesure de succès** | ≥ 80 % de bonnes réponses à la question 1 du quiz ; ≥ 60 % des utilisateurs terminent le parcours ; score « envie d'investir tout de suite » ≤ 2/5 | Les utilisateurs qui modifient leur répartition consultent l'écran Comprendre avant de valider ; baisse des choix « 100 % actions » chez ceux qui déclarent ne pas supporter de perte | ≥ 70 % des utilisateurs savent situer un produit réel sur l'échelle 1-7 du DIC ; questions posées au conseiller (enquête déclarative) |
| **Critère de passage** | Tests utilisateurs ≥ 2/3, page réglementaire validée, backtest non rejeté | V1 stable 3 mois, pas de signalement de contenu trompeur | Avis juridique favorable, accord du RCCI de Tradinvest |
| **Durée indicative** | 3 mois de développement après validation de la maquette | +4 mois | +6 mois |

## Ce qui pourrait remettre en cause la feuille de route

- Si les tests montrent que la phrase VaR reste mal comprise, la V1 doit **d'abord** corriger la formulation (variantes prêtes dans `06_protocole_test_utilisateurs.md`) avant tout ajout de fonctionnalité.
- Si le commanditaire souhaite relier l'application à ses offres réelles, la V3 change de nature : c'est de la **communication promotionnelle**, soumise à toutes les règles MiFID, et non plus un outil pédagogique.
