# Modèles : compte rendu, retour d'expérience, plan de soutenance

## A. Modèle de compte rendu (½ page, déposé dans l'espace partagé sous 48 h)

```
COMPTE RENDU — Projet 1 Boussole — Réunion du [jj/mm/aaaa]
Type : séance n° __ / réunion commanditaire / réunion d'équipe
Présents : ______________________      Absents : ______________________
Rédacteur : [RC]                         Diffusion : équipe, commanditaire

1. Décisions prises
   - D1 : ...
   - D2 : ...

2. Décisions attendues du commanditaire (avec date limite)
   - ... avant le [jj/mm]

3. Actions
   | # | Action | Responsable | Échéance | Statut |
   |---|--------|-------------|----------|--------|
   | A1 |       |             |          |        |

4. Risques nouveaux ou modifiés (→ registre)
   - ...

Prochaine réunion : [date, lieu, ordre du jour]
```

## B. Plan du retour d'expérience (2 pages, séance 5)

Le critère d'évaluation est la **lucidité sur ce qui a marché ou non** : citer des faits, des chiffres, des dates.

1. **Ce que nous avions prévu** (rappel de la note de cadrage, du planning, des charges) ; **ce qui s'est réellement passé** (écarts de délai et de charge, en heures).
2. **Ce qui a marché**, avec preuves (ex. : tests ___/3, backtest non rejeté, CR envoyés en ___ h en moyenne).
3. **Ce qui n'a pas marché**, et pourquoi (cause racine, pas seulement le symptôme).
4. **Risques** : lesquels sont survenus ? La parade a-t-elle fonctionné ? Exemple déjà connu : le backtest a montré une sous-estimation du risque du portefeuille Prudent → adoption de la règle de prudence.
5. **Relation avec le commanditaire** : délais de validation, malentendus, ce que nous referions autrement.
6. **Rotation des rôles** : apports et difficultés de la passation en séance 3.
7. **Trois leçons** que chaque membre réutilisera dans un futur projet.

## C. Plan de soutenance (12 minutes + 8 minutes de questions)

| Min | Partie | Contenu | Support |
|---|---|---|---|
| 0-1 | Le problème | Débutants qui investissent sans mesurer la perte possible ; demande de Tradinvest | 1 diapositive |
| 1-2,5 | Nos utilisateurs | Léa et Nadia : besoins et craintes opposés | 1 diapositive |
| 2,5-4 | Ce que nous avons le droit de faire | Tableau « peut / ne peut pas » ; validation du commanditaire | 1 diapositive |
| 4-7 | **L'indicateur** | La phrase, les choix (95 %, 1 mois, historique), la règle de prudence née du backtest, les limites | 2 diapositives |
| 7-9,5 | **Démonstration** | Maquette en direct : accueil → fiche Dynamique → Comprendre → Rejouer 2022 | Maquette |
| 9,5-11 | **Preuve** | Résultats des 3 tests (___/3) et corrections apportées | 1 diapositive |
| 11-12 | Et après | Feuille de route V1 / V2 / V3 ; ce que nous avons appris | 1 diapositive |

Questions techniques probables (projet 5) : pourquoi historique et pas paramétrique ? Pourquoi des fenêtres chevauchantes ? Que vaut le backtest ? Pourquoi 95 % et pas 99 % ? Que se passe-t-il en 2008 ? Comment gérez-vous un changement de régime ? → réponses dans `04_specification_indicateur_risque.md` §3 et §7.
