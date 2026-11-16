# Projet 1 — Boussole : application d'initiation à l'investissement (version 1)

Conception d'une application **pédagogique en argent virtuel** qui apprend aux particuliers débutants à comprendre le risque avant d'investir. Commanditaire : directeur produit de la fintech Tradinvest.

*Projet étudiant de master (cas pédagogique). Ce dépôt ne contient ni conseil en investissement ni offre commerciale ; les chiffres sont calculés sur des performances passées, qui ne préjugent pas des performances futures.*

## Démarrage rapide

```bash
git clone https://github.com/xiaopengh/boussole-initiation-investissement.git
cd boussole-initiation-investissement
```

**Voir la maquette** : aucune installation. Ouvrir `maquette/index.html` dans un navigateur (double-clic).

**Relancer le calcul** : Python 3.12 ou plus récent.

```bash
cd python
python3 -m venv .venv
source .venv/bin/activate          # Windows : .venv\Scripts\activate
pip install -r requirements.txt
python test_var_indicateur.py      # 7 contrôles unitaires
python var_indicateur.py --offline # recalcule à partir des cours gelés, sans réseau
```

Le mode `--offline` reproduit exactement les chiffres du dépôt. Sans cette option, le script retélécharge les cours depuis Yahoo Finance : les cours ajustés pouvant être révisés, les chiffres peuvent alors légèrement changer.

> **Indicateur affiché :** « Dans 1 cas sur 20, vous pourriez perdre plus de X € en un mois. »
> VaR historique 95 % à 1 mois, règle de prudence, calculée sur des cours réels de 2009 à 2026.

## Correspondance avec le cahier des charges

| Exigence | Livrable | État |
|---|---|---|
| Deux profils d'utilisateurs | [docs/02_profils_utilisateurs.md](docs/02_profils_utilisateurs.md) | v1 |
| Page réglementaire | [docs/03_page_reglementaire.md](docs/03_page_reglementaire.md) | v1, **à valider par le commanditaire** |
| Maquette cliquable 5-6 écrans | [maquette/index.html](maquette/index.html) + [docs/05_maquette_ecrans.md](docs/05_maquette_ecrans.md) | v1 (6 écrans), **outil à confirmer** |
| Spécification de l'indicateur VaR | [docs/04_specification_indicateur_risque.md](docs/04_specification_indicateur_risque.md) | v1 |
| Test auprès de 3 utilisateurs + corrections | [docs/06_protocole_test_utilisateurs.md](docs/06_protocole_test_utilisateurs.md) | Protocole prêt, **tests à réaliser** |
| *Bonus* : calcul Python sur 3-4 portefeuilles | [python/var_indicateur.py](python/var_indicateur.py) | Fait (4 portefeuilles, backtest) |
| *Bonus* : feuille de route en 3 versions | [docs/07_feuille_de_route.md](docs/07_feuille_de_route.md) | v1 |
| Note de cadrage (S1) | [docs/01_note_de_cadrage.md](docs/01_note_de_cadrage.md) | v1, noms à compléter |
| Planning, RACI (S2) | [docs/08_planning_et_raci.md](docs/08_planning_et_raci.md) | v1, dates à compléter |
| Registre des risques (S2+) | [docs/09_registre_des_risques.md](docs/09_registre_des_risques.md) | v1 |
| Dossier de validation technique (S4) | [docs/10_dossier_validation_technique.md](docs/10_dossier_validation_technique.md) | Conventions et contrôles remplis ; relecture croisée à compléter |
| Comptes rendus, retour d'expérience, soutenance | [docs/11_modeles_compte_rendu_rex_soutenance.md](docs/11_modeles_compte_rendu_rex_soutenance.md) | Modèles |

Les versions Word (.docx) de chaque document sont dans `docs/word/`.

## Résultats clés (données arrêtées au 30/10/2026)

| Portefeuille | Actions / Oblig. / Monét. | X pour 10 000 € | Pire mois observé |
|---|---|---|---|
| Prudent | 20 / 60 / 20 | 310 € | −950 € (mars 2020) |
| Équilibré | 50 / 40 / 10 | 420 € | −1 821 € |
| Dynamique | 80 / 20 / 0 | 560 € | −2 705 € |
| 100 % actions | 100 / 0 / 0 | 620 € | −3 248 € |

Backtest (148 mois hors échantillon) : 6,1 à 7,4 % de dépassements, test de Kupiec non rejeté pour les 4 portefeuilles. Sans la règle de prudence, le portefeuille Prudent serait rejeté (10,1 %).

## Organisation du dépôt

| Dossier | Contenu |
|---|---|
| `docs/` | Les 11 documents en Markdown ; `docs/word/` : les mêmes en Word (.docx) |
| `maquette/` | Maquette cliquable (`index.html`) et ses données (`donnees_indicateur.js`, générées par le script) |
| `python/` | Calcul de l'indicateur (`var_indicateur.py`), contrôles unitaires, cours gelés (`donnees/prix.csv`), résultats (`resultats/`) |

**Maquette** : sur ordinateur, les annotations (besoins couverts) s'affichent à gauche ; cocher « Mode test utilisateur » pour les masquer. Pour la tester sur un téléphone, servir le dossier sur le réseau local (`python3 -m http.server 8000` dans `maquette/`) ou l'héberger (GitHub Pages).

**Calcul** : les sorties vont dans `python/resultats/` (CSV, PNG, `controles.txt`) et régénèrent `maquette/donnees_indicateur.js`, ce qui met à jour les chiffres de la maquette.

**Données** : cours publics issus de Yahoo Finance via la bibliothèque `yfinance`, figés au 30/10/2026 pour la reproductibilité. Ils sont fournis à des fins pédagogiques uniquement.

## Ce qui reste à faire par l'équipe

1. Compléter les noms, rôles et dates (note de cadrage, planning).
2. **Vérifier les références réglementaires** citées dans la page réglementaire, puis la faire valider.
3. Confirmer avec le commanditaire si la maquette HTML convient ; sinon la reproduire dans Figma.
4. **Faire passer les 3 tests utilisateurs**, remplir les grilles et appliquer les corrections.
5. Recalcul indépendant au tableur (contrôle C14), puis relecture croisée avec le projet 5.
