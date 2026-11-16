# Maquette cliquable : écrans, identité et traçabilité

*Livrable du périmètre minimal · maquette : `maquette/index.html`*

## Comment l'ouvrir

- **Sur ordinateur** : double-cliquer sur `maquette/index.html`. Le téléphone s'affiche au centre et les **annotations** à gauche : objectif de l'écran, besoins couverts, choix de conception. Cocher **« Mode test utilisateur »** pour masquer les annotations pendant un test.
- **Sur téléphone** (pour les tests) : héberger le dossier `maquette/` (GitHub Pages, Netlify Drop… gratuits) ou le servir en local (`python -m http.server` dans le dossier). L'application s'affiche alors en plein écran.
- Les chiffres viennent de `maquette/donnees_indicateur.js`, **généré par le script Python** : aucun chiffre n'est saisi à la main.

> **Outil.** Le cahier des charges cite Figma, Canva ou PowerPoint. La maquette est un prototype HTML (aucune programmation de l'application réelle : pas de serveur, pas de compte, pas de données). **À confirmer avec le commanditaire en séance.** S'il exige Figma, les 6 écrans se reproduisent à l'identique à partir de captures d'écran du prototype, avec des liens entre cadres (environ 3 h).

## Identité visuelle : « sobre et rassurante »

| Choix | Justification |
|---|---|
| **Nom : Boussole** | On n'achète pas une boussole pour aller plus vite, mais pour savoir où l'on va. Le nom ne promet aucun gain. |
| **Bleu ardoise** `#24506B` (couleur principale) | Associé à la confiance et au sérieux, sans le « bleu banque » trop institutionnel. |
| **Fond crème** `#F6F3EE` | Plus chaleureux et moins clinique qu'un blanc pur ; fatigue moins à la lecture (profil N). |
| **Terre cuite** `#B4532A` pour les pertes | Visible sans être alarmiste. Le **rouge vif** et le **vert fluo** des applications de trading (code « casino ») sont exclus. |
| **Ocre** `#B8860B` pour les mises en garde | Attire l'attention (« Ce n'est pas un maximum ») sans dramatiser. |
| **Police système** (San Francisco, Roboto, Segoe) | Lisible, familière, gratuite ; bouton « Aa » pour agrandir le texte. |
| **Ton** | Vouvoiement, phrases courtes, aucun superlatif, aucun « opportunité ». |

**Ce que nous nous interdisons (liste anti-incitation)** : classements entre utilisateurs, récompenses liées à un gain, confettis, cours en temps réel qui clignotent, notifications « le marché bouge ! », compte à rebours, bouton « Investir maintenant », mise en avant des meilleurs mois.

## Les 6 écrans

| # | Écran | Ce qu'on y voit | Besoins couverts |
|---|---|---|---|
| 1 | **Accueil** | Les 3 engagements (argent 100 % virtuel, aucun ordre réel, aucune promesse de gain), le parcours en 4 étapes (≈ 15 min), l'avertissement de perte en capital | N1, L3, L4 |
| 2 | **Choisir un portefeuille** | Montant virtuel (1 000 / 5 000 / 10 000 €), 4 portefeuilles avec composition et **même phrase de risque** sur chaque carte, barre de comparaison, repère « Livret A » | L2, N2 |
| 3 | **Indicateur de risque** | La phrase « Dans 1 cas sur 20… », le pictogramme de 20 mois, « Les 19 autres mois… », l'encadré « Ce n'est pas une perte maximale » avec le pire mois en euros | L1, L2, N3 |
| 4 | **Comprendre ce chiffre** | Graphique de 20 barres (20 groupes de périodes réelles, du pire au meilleur), la barre « 1 sur 20 » et sa perte moyenne, puis « ce qu'il dit / ne dit pas / comment il est calculé / le mot des pros (VaR) » | L1, N4, N5 |
| 5 | **Rejouer une période passée** | 2020 (Covid) ou 2022 (hausse des taux), semaine par semaine ; **pause à mi-baisse** avec la question « Que faites-vous ? » ; bilan factuel ; leçon neutre | N3, L3, L4 |
| 6 | **Vérifier ma compréhension** | 3 questions avec correction expliquée, sans note ni classement ; la question 1 est celle du test utilisateur | L1, N5 |
| + | **Règles du jeu** (bouton « i ») | Argent virtuel, pas d'ordre, pas de conseil, avertissements, sources des données, renvoi vers l'AMF et l'ORIAS | N1, L4 |
| + | **Glossaire** (mots soulignés en pointillé) | Action, obligation, monétaire, indice, portefeuille, rééquilibrage, perte en capital, VaR | L1, N4 |

### Traçabilité inverse : chaque besoin est couvert

| Besoin | Écrans |
|---|---|
| L1 Comprendre vite, sans jargon | 3, 4, 6, glossaire |
| L2 Perte possible en € | 2, 3 |
| L3 S'entraîner sans risque | 1, 5 |
| L4 Résister aux promesses et à l'impulsivité | 1, 5, règles du jeu |
| N1 Aucun argent réel en jeu | 1, badge permanent, règles du jeu |
| N2 Comparer, y compris au Livret A | 2 |
| N3 Ce qui arrive dans une crise | 3, 5 |
| N4 Prendre son temps, lisibilité | 4, bouton « Aa », glossaire |
| N5 Préparer un rendez-vous avec un conseiller | 4 (« Le mot des pros »), 6 |

## Choix de conception notables

- **Le risque avant le rendement.** Aucun écran n'affiche de performance moyenne ou annualisée. Les gains apparaissent seulement dans le « rejouer », à égalité avec les pertes.
- **Pas de biais rétrospectif dans « Rejouer ».** La pause se fait quand la baisse atteint 60 % de son maximum de l'année, **pas au point bas** : s'arrêter au plus bas prouverait toujours qu'« il fallait garder ». Les deux épisodes ont des dénouements opposés (2020 : remontée en fin d'année ; 2022 : toujours en perte en décembre, y compris pour le Prudent, −13,6 %).
- **Le même « 20 » partout.** Pictogramme de 20 mois (écran 3), graphique en 20 barres (écran 4), question « sur 24 mois, combien ? » (écran 6).
- **Aucun questionnaire de profil** qui aboutirait à « votre portefeuille idéal » : ce serait un conseil personnalisé (voir page réglementaire).
