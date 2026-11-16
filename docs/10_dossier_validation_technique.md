# Dossier de validation technique

*Jalon de fin de séance 4 · 2 pages · pré-rempli (conventions et contrôles) ; les sections 3 et 4 sont à compléter après la relecture croisée*

## 1. Conventions retenues

| Domaine | Convention |
|---|---|
| **Données** | Publiques uniquement. Yahoo Finance via `yfinance` 1.8.0. Cours de clôture **ajustés** (`auto_adjust=True`). Tickers : `IWDA.AS`, `XGLE.DE`, `XEON.DE` ; proxy 2008 : `EXSA.DE`. |
| **Gel des données** | Téléchargement jusqu'au **30/10/2026** inclus, enregistré dans `python/donnees/prix.csv`. Toute relecture se fait en mode `--offline` sur ce fichier. |
| **Période** | Du 25/09/2009 (première date commune) au 30/10/2026 : 4 378 jours de bourse. |
| **Alignement des places** | Report du dernier cours, 5 jours au plus. Aucune ligne supprimée. |
| **Portefeuilles** | Poids cibles (Prudent 20/60/20, Équilibré 50/40/10, Dynamique 80/20/0, 100 % actions), rééquilibrés le 1er jour de bourse de chaque mois. Aucun frais ni impôt. |
| **Horizon / niveau** | 21 jours de bourse / 95 %. |
| **Rendements** | Simples, `V(t+21)/V(t) − 1`, fenêtres glissantes (4 357). |
| **Quantile** | `numpy.quantile`, interpolation linéaire. VaR exprimée en perte positive. |
| **Règle de prudence** | VaR affichée = max(VaR sur tout l'historique ; VaR sur les 1 260 derniers jours de bourse, soit 1 240 fenêtres). |
| **Arrondi** | Par excès à 2 chiffres significatifs, appliqué au montant en euros. |
| **Backtest** | Pas de 21 jours, à partir de 1 260 jours d'historique ; mois non chevauchants (148) ; même fonction d'estimation que le chiffre affiché ; tests de Kupiec et de Christoffersen à 5 %. |
| **Code** | Python 3.12, versions figées dans `requirements.txt`. Un seul script (`var_indicateur.py`) ; paramètres en tête de fichier ; noms en français ; aucun chiffre saisi à la main dans la maquette (fichier `donnees_indicateur.js` généré). |
| **Documents** | Markdown, un fichier par livrable, numérotés `01_` à `11_` ; version et date en tête. |

## 2. Contrôles effectués

| # | Contrôle | Méthode | Résultat |
|---|---|---|---|
| C1 | Données complètes | Comptage des valeurs manquantes avant et après alignement | 72 comblées, 0 restante ✅ |
| C2 | Absence d'aberration | Variations journalières > 15 % ; prix > 0 | 0 cas ; prix tous positifs ✅ |
| C3 | Cohérence VaR ≤ ES ≤ pire mois | Automatique (`controles.txt`) | Vérifié pour les 4 portefeuilles ✅ |
| C4 | Fréquence empirique des dépassements dans l'échantillon | Automatique | 5,00 % exactement ✅ |
| C5 | Arrondi jamais inférieur au calcul | Test unitaire sur 500 valeurs + contrôle sur les chiffres affichés | ✅ |
| C6 | Rééquilibrage correct | Test unitaire sur un cas calculé à la main | ✅ |
| C7 | Pas de biais d'anticipation | Test unitaire : modifier les cours après t ne change pas la VaR à t | ✅ |
| C8 | Calcul VaR et ES sur série connue | Test unitaire (−0,50 … +0,49 → VaR 0,4505 ; ES 0,48) | ✅ |
| C9 | Reproductibilité | Deux exécutions `--offline` successives → fichiers identiques | ✅ |
| C10 | Contrôle croisé paramétrique | VaR gaussienne vs historique | Écart < 0,4 point ✅ |
| C11 | Backtest | Kupiec à 5 % | Non rejeté pour les 4 portefeuilles (p ≥ 0,20) ✅ |
| C12 | Indépendance des dépassements | Christoffersen à 5 % | Rejeté pour le Prudent (p = 0,035, grappe en 2022) ⚠️ limite documentée |
| C13 | Cohérence maquette ↔ calcul | Les 4 phrases de la maquette (10 000 €) comparées à `synthese.csv` | 310 / 420 / 560 / 620 € ✅ |
| C14 | Recalcul indépendant | Un membre recalcule la VaR du portefeuille Équilibré dans un tableur à partir de `prix.csv` | **À faire** (L3) |

Commandes de reproduction (depuis le dossier `python/`) :

```
pip install -r requirements.txt
python test_var_indicateur.py
python var_indicateur.py --offline
```

## 3. Remarques de la relecture croisée (projet 5) — *à compléter en séance 4*

| # | Remarque du groupe relecteur | Gravité | Notre réponse |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |

Points sur lesquels nous **sollicitons** l'avis du projet 5 :

1. Le choix d'une **règle de prudence** (max de deux fenêtres) plutôt qu'une VaR conditionnelle (EWMA, GARCH filtré).
2. Les fenêtres chevauchantes pour l'estimation : biais ou seulement perte d'efficacité ?
3. Le taux de dépassement de 6 à 7,4 % (non rejeté, mais au-dessus de 5 %) : faut-il un multiplicateur de sécurité ?
4. La représentativité de la période (pas de 2008 ; test de résistance avec un proxy européen).

## 4. Suites données — *à compléter*

| Remarque | Action | Responsable | Faite le | Effet sur les chiffres affichés |
|---|---|---|---|---|
| | | | | |
