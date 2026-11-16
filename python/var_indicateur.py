"""
Indicateur de risque grand public fondé sur la VaR historique
==============================================================

Projet 1 — Application d'initiation à l'investissement (bonus Python).

Phrase affichée à l'utilisateur :
    « Dans 1 cas sur 20, vous pourriez perdre plus de X € en un mois. »

Conventions (voir docs/04_specification_indicateur_risque.md) :
    - VaR historique, niveau de confiance 95 % (1 cas sur 20) ;
    - horizon 21 jours de bourse (≈ 1 mois calendaire) ;
    - RÈGLE DE PRUDENCE : on calcule la VaR sur tout l'historique disponible ET sur les
      5 dernières années (1 260 jours de bourse), et l'on affiche la plus élevée des deux ;
    - rendements sur 21 jours glissants (fenêtres chevauchantes) ;
    - portefeuilles rééquilibrés le premier jour de bourse de chaque mois ;
    - prix ajustés des dividendes et opérations sur titres (yfinance, auto_adjust=True) ;
    - montant affiché arrondi PAR EXCÈS à deux chiffres significatifs.

Usage :
    python var_indicateur.py            # télécharge les cours puis calcule
    python var_indicateur.py --offline  # réutilise donnees/prix.csv (reproductible)

Sorties (dossier resultats/) :
    synthese.csv, backtest.csv, sensibilite.csv, stress_2008.csv,
    controles.txt, indicateur.json, *.png
    + ../maquette/donnees_indicateur.js (données utilisées par la maquette)
"""

from __future__ import annotations

import argparse
import json
import math
import pathlib

import numpy as np
import pandas as pd
from scipy import stats

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

# ---------------------------------------------------------------------------
# Paramètres (une seule source de vérité)
# ---------------------------------------------------------------------------
RACINE = pathlib.Path(__file__).resolve().parent
DONNEES = RACINE / "donnees"
RESULTATS = RACINE / "resultats"
MAQUETTE_JS = RACINE.parent / "maquette" / "donnees_indicateur.js"

DATE_DEBUT_TELECHARGEMENT = "2007-01-01"
DATE_FIN = "2026-10-31"  # dernier mois complet : gel des données pour la reproductibilité

NIVEAU_CONFIANCE = 0.95  # « 1 cas sur 20 »
HORIZON_JOURS = 21  # ≈ 1 mois de bourse
FENETRE_RECENTE = 1260  # 5 ans de bourse : 2e échantillon de la règle de prudence
MINIMUM_BACKTEST = 1260  # 5 ans d'historique avant la première date testée
MONTANTS_AFFICHES = [1_000, 10_000]  # en euros virtuels

ACTIFS = {
    "actions_monde": ("IWDA.AS", "Actions monde — iShares Core MSCI World UCITS ETF (EUR)"),
    "obligations_euro": ("XGLE.DE", "Obligations d'États zone euro — Xtrackers II Eurozone Government Bond UCITS ETF (EUR)"),
    "monetaire": ("XEON.DE", "Monétaire euro — Xtrackers II EUR Overnight Rate Swap UCITS ETF (EUR)"),
}
# Proxy actions pour le test de résistance 2008 (IWDA.AS n'existe qu'à partir de sept. 2009)
PROXY_ACTIONS_2008 = ("EXSA.DE", "Actions Europe — iShares STOXX Europe 600 UCITS ETF (DE) (EUR)")

PORTEFEUILLES = {
    "prudent": {"nom": "Prudent", "poids": {"actions_monde": 0.20, "obligations_euro": 0.60, "monetaire": 0.20}},
    "equilibre": {"nom": "Équilibré", "poids": {"actions_monde": 0.50, "obligations_euro": 0.40, "monetaire": 0.10}},
    "dynamique": {"nom": "Dynamique", "poids": {"actions_monde": 0.80, "obligations_euro": 0.20, "monetaire": 0.00}},
    "actions": {"nom": "100 % actions", "poids": {"actions_monde": 1.00, "obligations_euro": 0.00, "monetaire": 0.00}},
}


# ---------------------------------------------------------------------------
# Données
# ---------------------------------------------------------------------------
def telecharger_prix() -> pd.DataFrame:
    import yfinance as yf

    tickers = [t for t, _ in ACTIFS.values()] + [PROXY_ACTIONS_2008[0]]
    brut = yf.download(
        tickers,
        start=DATE_DEBUT_TELECHARGEMENT,
        end=(pd.Timestamp(DATE_FIN) + pd.Timedelta(days=1)).strftime("%Y-%m-%d"),
        auto_adjust=True,
        progress=False,
    )["Close"]
    brut.index = pd.to_datetime(brut.index).tz_localize(None)
    brut = brut.loc[:DATE_FIN]
    DONNEES.mkdir(parents=True, exist_ok=True)
    brut.to_csv(DONNEES / "prix.csv", float_format="%.6f")
    return brut


def charger_prix(offline: bool) -> pd.DataFrame:
    if offline:
        prix = pd.read_csv(DONNEES / "prix.csv", index_col=0, parse_dates=True)
    else:
        prix = telecharger_prix()
    return prix.sort_index()


def nettoyer(prix: pd.DataFrame, colonnes: list[str], controles: list[str], etiquette: str) -> pd.DataFrame:
    """Aligne des cotations de places différentes (Amsterdam / Francfort).

    Un jour férié sur une seule place laisse un trou : on reporte le dernier cours connu
    (au plus 5 jours). On commence à la première date où tous les actifs cotent.
    """
    p = prix[colonnes].copy()
    debut = max(p[c].first_valid_index() for c in colonnes)
    p = p.loc[debut:]
    trous = int(p.isna().sum().sum())
    p = p.ffill(limit=5)
    reste = int(p.isna().sum().sum())
    p = p.dropna()
    r = p.pct_change().dropna()
    extremes = r[(r.abs() > 0.15).any(axis=1)]
    controles.append(f"[{etiquette}] période {p.index[0].date()} → {p.index[-1].date()}, {len(p)} jours de bourse")
    controles.append(f"[{etiquette}] valeurs manquantes comblées par report (≤ 5 j) : {trous} ; non comblées (lignes supprimées) : {reste}")
    controles.append(f"[{etiquette}] variations journalières > 15 % en valeur absolue : {len(extremes)}"
                     + ("" if extremes.empty else f" → {', '.join(str(d.date()) for d in extremes.index)}"))
    controles.append(f"[{etiquette}] prix strictement positifs : {bool((p > 0).all().all())}")
    return p


# ---------------------------------------------------------------------------
# Calculs
# ---------------------------------------------------------------------------
def valeur_portefeuille(prix: pd.DataFrame, poids: dict[str, float]) -> pd.Series:
    """Valeur (base 1) d'un portefeuille rééquilibré au 1er jour de bourse de chaque mois."""
    rend = prix.pct_change().dropna()
    w = np.array([poids.get(c, 0.0) for c in prix.columns])
    assert abs(w.sum() - 1) < 1e-12, "les poids doivent sommer à 100 %"
    valeurs = pd.Series(index=rend.index, dtype=float)
    v = 1.0
    for _, bloc in rend.groupby(rend.index.to_period("M")):
        lignes = (1 + bloc).cumprod().to_numpy() * (w * v)  # chaque ligne évolue librement dans le mois
        total = lignes.sum(axis=1)
        valeurs.loc[bloc.index] = total
        v = total[-1]  # rééquilibrage au début du mois suivant
    return pd.concat([pd.Series([1.0], index=[prix.index[0]]), valeurs])


def rendements_horizon(valeur: pd.Series, h: int = HORIZON_JOURS) -> pd.Series:
    return (valeur / valeur.shift(h) - 1).dropna()


def var_historique(r: pd.Series, niveau: float = NIVEAU_CONFIANCE) -> float:
    """VaR en perte positive : -quantile(1 - niveau) des rendements (interpolation linéaire)."""
    return float(-np.quantile(r.to_numpy(), 1 - niveau))


def es_historique(r: pd.Series, niveau: float = NIVEAU_CONFIANCE) -> float:
    """Expected Shortfall : perte moyenne au-delà de la VaR."""
    seuil = -var_historique(r, niveau)
    return float(-r[r <= seuil].mean())


def var_normale(valeur: pd.Series, niveau: float = NIVEAU_CONFIANCE, h: int = HORIZON_JOURS) -> float:
    """Contrôle croisé : VaR paramétrique gaussienne (moyenne et écart-type journaliers, règle de la racine du temps)."""
    rj = valeur.pct_change().dropna()
    return float(-(rj.mean() * h + rj.std(ddof=1) * math.sqrt(h) * stats.norm.ppf(1 - niveau)))


def kupiec(n: int, x: int, p: float) -> tuple[float, float]:
    """Test de couverture inconditionnelle de Kupiec (proportion of failures)."""
    if n == 0:
        return float("nan"), float("nan")
    phat = x / n
    ll0 = (n - x) * math.log(1 - p) + x * math.log(p)
    ll1 = 0.0
    if 0 < x < n:
        ll1 = (n - x) * math.log(1 - phat) + x * math.log(phat)
    lr = -2 * (ll0 - ll1)
    return lr, float(1 - stats.chi2.cdf(lr, df=1))


def christoffersen(seq: list[bool]) -> tuple[float, float]:
    """Test d'indépendance des dépassements de Christoffersen (les dépassements arrivent-ils en grappes ?)."""
    n00 = n01 = n10 = n11 = 0
    for a, b in zip(seq[:-1], seq[1:]):
        if not a and not b:
            n00 += 1
        elif not a and b:
            n01 += 1
        elif a and not b:
            n10 += 1
        else:
            n11 += 1
    pi0 = n01 / (n00 + n01) if n00 + n01 else 0.0
    pi1 = n11 / (n10 + n11) if n10 + n11 else 0.0
    pi = (n01 + n11) / max(n00 + n01 + n10 + n11, 1)

    def ll(k0, k1, q):  # log-vraisemblance de k0 « non » et k1 « oui » avec probabilité q
        return (k0 * math.log(1 - q) if k0 else 0.0) + (k1 * math.log(q) if k1 else 0.0)

    lr = -2 * (ll(n00 + n10, n01 + n11, pi) - ll(n00, n01, pi0) - ll(n10, n11, pi1))
    return lr, float(1 - stats.chi2.cdf(lr, df=1))


def estimer_var(v: np.ndarray, methode: str = "prudence", h: int = HORIZON_JOURS) -> dict:
    """Estime la VaR à partir des valeurs v[0..t] du portefeuille (rien après t).

    methode :
      - "prudence"  (méthode AFFICHÉE) : max(VaR tout l'historique, VaR 5 dernières années) ;
      - "historique" : tout l'historique disponible ;
      - "recent"     : 5 dernières années seulement.
    """
    tout = v[h:] / v[:-h] - 1  # rendements sur h jours, fenêtres chevauchantes
    recent = tout[-(FENETRE_RECENTE - h + 1):]  # fenêtres entièrement contenues dans les 5 dernières années
    var_tout = float(-np.quantile(tout, 1 - NIVEAU_CONFIANCE))
    var_recent = float(-np.quantile(recent, 1 - NIVEAU_CONFIANCE))
    if methode == "historique":
        var, ech = var_tout, tout
    elif methode == "recent":
        var, ech = var_recent, recent
    else:
        var, ech = (var_recent, recent) if var_recent >= var_tout else (var_tout, tout)
    return {"var": var, "var_tout": var_tout, "var_recent": var_recent, "echantillon": ech,
            "echantillon_nom": "5 dernières années" if ech is recent else "tout l'historique"}


def backtest(valeur: pd.Series, methode: str = "prudence", h: int = HORIZON_JOURS,
             minimum: int = MINIMUM_BACKTEST) -> dict:
    """Backtest hors échantillon sur des mois NON chevauchants.

    À chaque date t (pas de h jours), la VaR est estimée avec la MÊME fonction que le chiffre
    affiché, en n'utilisant que les cours connus à t, puis comparée au rendement réalisé
    entre t et t + h.
    """
    v = valeur.to_numpy()
    dates = valeur.index
    lignes, seq = [], []
    for t in range(minimum, len(v) - h, h):
        var_t = estimer_var(v[: t + 1], methode)["var"]
        realise = v[t + h] / v[t] - 1
        dep = bool(realise < -var_t)
        seq.append(dep)
        lignes.append((dates[t].date(), var_t, realise, dep))
    n, x = len(seq), sum(seq)
    lr, pval = kupiec(n, x, 1 - NIVEAU_CONFIANCE)
    lr_i, pval_i = christoffersen(seq)
    return {
        "n_mois_testes": n,
        "depassements": x,
        "taux_depassement": x / n if n else float("nan"),
        "kupiec_LR": lr,
        "kupiec_pvalue": pval,
        "christoffersen_pvalue": pval_i,
        "detail": lignes,
    }


def arrondi_par_exces(x: float, chiffres: int = 2) -> int:
    """Arrondi par excès à `chiffres` chiffres significatifs (on ne sous-estime jamais la perte affichée)."""
    if x <= 0:
        return 0
    exposant = int(math.floor(math.log10(x))) - chiffres + 1
    q = x / 10 ** exposant
    k = round(q) if math.isclose(q, round(q), abs_tol=1e-9) else math.ceil(q)  # 20,0 reste 20 (bruit flottant)
    return k * 10 ** exposant if exposant >= 0 else round(k * 10.0 ** exposant, -exposant)


def phrase(var_pct: float, montant: float) -> str:
    x = f"{arrondi_par_exces(var_pct * montant):,}".replace(",", " ")  # espace fine insécable à la française
    return f"Dans 1 cas sur 20, vous pourriez perdre plus de {x} € en un mois."


# ---------------------------------------------------------------------------
# Programme principal
# ---------------------------------------------------------------------------
def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--offline", action="store_true", help="réutiliser donnees/prix.csv sans téléchargement")
    args = ap.parse_args()

    RESULTATS.mkdir(parents=True, exist_ok=True)
    controles: list[str] = []
    prix_brut = charger_prix(args.offline)

    colonnes = [t for t, _ in ACTIFS.values()]
    prix = nettoyer(prix_brut, colonnes, controles, "principal")
    prix = prix.rename(columns={t: k for k, (t, _) in ACTIFS.items()})

    synthese, sensib, bt_rows, stress_rows = [], [], [], []
    export = {
        "parametres": {
            "niveau_confiance": NIVEAU_CONFIANCE,
            "horizon_jours_bourse": HORIZON_JOURS,
            "periode": [str(prix.index[0].date()), str(prix.index[-1].date())],
            "methode": "VaR historique 95 % sur rendements 21 jours glissants, rééquilibrage mensuel ; "
                       "règle de prudence = max(tout l'historique, 5 dernières années)",
            "actifs": {k: {"ticker": t, "libelle": lib} for k, (t, lib) in ACTIFS.items()},
        },
        "portefeuilles": {},
    }

    fig_h, axes_h = plt.subplots(2, 2, figsize=(11, 7), sharex=True)
    for ax, (cle, pf) in zip(axes_h.ravel(), PORTEFEUILLES.items()):
        val = valeur_portefeuille(prix, pf["poids"])
        r21 = rendements_horizon(val)
        est = estimer_var(val.to_numpy())
        var95 = est["var"]  # chiffre affiché (règle de prudence)
        ech = pd.Series(est["echantillon"])  # échantillon qui détermine le chiffre affiché
        es95 = es_historique(r21)  # ES sur tout l'historique
        es95_ech = es_historique(ech)
        pire = float(r21.min())
        date_pire = r21.idxmin()
        debut_pire = val.index[val.index.get_loc(date_pire) - HORIZON_JOURS]
        meilleur = float(r21.max())
        part_negatifs = float((r21 < 0).mean())
        vnorm = var_normale(val)
        bt = backtest(val)  # méthode affichée (règle de prudence)
        bt_hist = backtest(val, "historique")  # variante : tout l'historique seul
        bt_rec = backtest(val, "recent")  # variante : 5 ans glissants seuls
        annees = (val.index[-1] - val.index[0]).days / 365.25
        perf_annualisee = float(val.iloc[-1] ** (1 / annees) - 1)
        vol_annualisee = float(val.pct_change().dropna().std() * math.sqrt(252))
        # pire baisse depuis un plus haut (drawdown)
        dd = float((val / val.cummax() - 1).min())

        controles.append(f"[{cle}] VaR historique({est['var_tout']:.4%}) ≤ ES({es95:.4%}) ≤ pire({-pire:.4%}) : "
                         f"{est['var_tout'] <= es95 <= -pire}")
        controles.append(f"[{cle}] VaR affichée = max(historique {est['var_tout']:.4%}, 5 ans {est['var_recent']:.4%}) = "
                         f"{var95:.4%} ({est['echantillon_nom']})")
        controles.append(f"[{cle}] fréquence des pertes > VaR affichée dans son échantillon : {(ech < -var95).mean():.4%} (attendu ≈ 5 %)")
        controles.append(f"[{cle}] arrondi par excès : X(1 000 €) = {arrondi_par_exces(var95 * 1000)} ≥ {var95 * 1000:.2f} : "
                         f"{arrondi_par_exces(var95 * 1000) >= var95 * 1000}")

        synthese.append({
            "portefeuille": pf["nom"],
            "actions_%": pf["poids"]["actions_monde"] * 100,
            "obligations_%": pf["poids"]["obligations_euro"] * 100,
            "monetaire_%": pf["poids"]["monetaire"] * 100,
            "VaR95_affichee_%": round(var95 * 100, 2),
            "echantillon_retenu": est["echantillon_nom"],
            "VaR95_historique_%": round(est["var_tout"] * 100, 2),
            "VaR95_5ans_%": round(est["var_recent"] * 100, 2),
            "VaR95_normale_%": round(vnorm * 100, 2),
            "ES95_historique_%": round(es95 * 100, 2),
            "ES95_echantillon_retenu_%": round(es95_ech * 100, 2),
            "pire_mois_%": round(-pire * 100, 2),
            "pire_mois_periode": f"{debut_pire.date()} → {date_pire.date()}",
            "meilleur_mois_%": round(meilleur * 100, 2),
            "part_mois_negatifs_%": round(part_negatifs * 100, 1),
            "volatilite_annuelle_%": round(vol_annualisee * 100, 2),
            "perte_max_depuis_plus_haut_%": round(-dd * 100, 2),
            "perf_annualisee_passee_%": round(perf_annualisee * 100, 2),
            **{f"X_affiche_{m}€": arrondi_par_exces(var95 * m) for m in MONTANTS_AFFICHES},
            "backtest_mois": bt["n_mois_testes"],
            "backtest_depassements": bt["depassements"],
            "backtest_taux_%": round(bt["taux_depassement"] * 100, 2),
            "kupiec_pvalue": round(bt["kupiec_pvalue"], 3),
            "christoffersen_pvalue": round(bt["christoffersen_pvalue"], 3),
            "variante_historique_seul_taux_%": round(bt_hist["taux_depassement"] * 100, 2),
            "variante_historique_seul_kupiec_p": round(bt_hist["kupiec_pvalue"], 3),
            "variante_5ans_seuls_taux_%": round(bt_rec["taux_depassement"] * 100, 2),
            "variante_5ans_seuls_kupiec_p": round(bt_rec["kupiec_pvalue"], 3),
        })
        for d, v_t, real, dep in bt["detail"]:
            bt_rows.append({"portefeuille": pf["nom"], "date": d, "VaR_estimee_%": round(v_t * 100, 3),
                            "rendement_realise_%": round(real * 100, 3), "depassement": dep})

        # Sensibilité à la période d'estimation
        for libelle, rr in [("tout l'historique", r21),
                            ("10 dernières années", r21.iloc[-(2 * FENETRE_RECENTE - HORIZON_JOURS + 1):]),
                            ("5 dernières années", r21.iloc[-(FENETRE_RECENTE - HORIZON_JOURS + 1):]),
                            ("3 dernières années", r21.iloc[-(756 - HORIZON_JOURS + 1):])]:
            sensib.append({"portefeuille": pf["nom"], "periode": libelle, "VaR95_%": round(var_historique(rr) * 100, 2),
                           "ES95_%": round(es_historique(rr) * 100, 2), "n_obs": len(rr)})

        # Données pour la maquette
        # 20 groupes de même taille (vingtiles) dans l'échantillon retenu : la barre 1 = « le 1 cas sur 20 »
        tri = np.sort(ech.to_numpy())
        vingtiles = [float(g.mean()) for g in np.array_split(tri, 20)]
        rejouer = {}
        for nom_ep, (d0, d1) in {"covid_2020": ("2020-01-02", "2020-12-31"), "taux_2022": ("2022-01-03", "2022-12-30")}.items():
            seg = val.loc[d0:d1]
            seg = seg / seg.iloc[0] * 10_000
            hebdo = seg.groupby(seg.index.to_period("W-FRI")).tail(1)  # dernier jour de bourse réel de chaque semaine
            rejouer[nom_ep] = {"dates": [str(d.date()) for d in hebdo.index], "valeurs": [round(float(x), 0) for x in hebdo]}
        export["portefeuilles"][cle] = {
            "nom": pf["nom"],
            "poids": pf["poids"],
            "var95": round(var95, 5),
            "var95_historique": round(est["var_tout"], 5),
            "var95_5ans": round(est["var_recent"], 5),
            "echantillon_retenu": est["echantillon_nom"],
            "n_fenetres_echantillon": int(len(ech)),
            "vingtiles": [round(x, 5) for x in vingtiles],
            "es95": round(es95, 5),
            "pire_mois": round(-pire, 5),
            "pire_mois_periode": [str(debut_pire.date()), str(date_pire.date())],
            "part_mois_negatifs": round(part_negatifs, 4),
            "n_fenetres": int(len(r21)),
            "backtest_taux": round(bt["taux_depassement"], 4),
            "rejouer": rejouer,
        }

        # Graphique : distribution des rendements sur 1 mois
        ax.hist(r21 * 100, bins=np.arange(-35, 25.5, 0.5), color="#9fb3c8", edgecolor="white", linewidth=0.3)
        ax.axvline(-est["var_tout"] * 100, color="#7a8793", lw=1.5, ls=":", label=f"VaR 95 % historique = −{est['var_tout']:.1%}")
        ax.axvline(-var95 * 100, color="#b4532a", lw=2, label=f"VaR 95 % affichée = −{var95:.1%}")
        ax.axvline(-es95 * 100, color="#5b2a86", lw=1.5, ls="--", label=f"ES 95 % historique = −{es95:.1%}")
        ax.set_title(f"{pf['nom']}")
        ax.legend(fontsize=8, frameon=False)
        ax.set_ylabel("nombre de fenêtres")
    for ax in axes_h[-1]:
        ax.set_xlabel("rendement sur 21 jours de bourse (%)")
    fig_h.suptitle(f"Distribution des rendements sur 1 mois — {prix.index[0].date()} → {prix.index[-1].date()}")
    fig_h.tight_layout()
    fig_h.savefig(RESULTATS / "distributions_1mois.png", dpi=150)
    plt.close(fig_h)

    # Test de résistance 2008 (hors période principale, avec proxy actions européennes)
    prix08 = nettoyer(prix_brut, [PROXY_ACTIONS_2008[0], ACTIFS["obligations_euro"][0], ACTIFS["monetaire"][0]],
                      controles, "stress 2008")
    prix08 = prix08.loc[:"2009-09-24"].rename(columns={PROXY_ACTIONS_2008[0]: "actions_monde",
                                                       ACTIFS["obligations_euro"][0]: "obligations_euro",
                                                       ACTIFS["monetaire"][0]: "monetaire"})
    for cle, pf in PORTEFEUILLES.items():
        r08 = rendements_horizon(valeur_portefeuille(prix08, pf["poids"]))
        stress_rows.append({"portefeuille": pf["nom"], "pire_mois_2008_2009_%": round(-r08.min() * 100, 2),
                            "fin_de_fenetre": str(r08.idxmin().date()),
                            "perte_pour_1000€": round(-r08.min() * 1000), "perte_pour_10000€": round(-r08.min() * 10000)})

    df = pd.DataFrame(synthese)
    df.to_csv(RESULTATS / "synthese.csv", index=False)
    pd.DataFrame(bt_rows).to_csv(RESULTATS / "backtest.csv", index=False)
    pd.DataFrame(sensib).to_csv(RESULTATS / "sensibilite.csv", index=False)
    pd.DataFrame(stress_rows).to_csv(RESULTATS / "stress_2008.csv", index=False)

    # Graphique comparatif simple (même vocabulaire que l'application)
    fig, ax = plt.subplots(figsize=(8, 4))
    x = np.arange(len(df))
    ax.bar(x - 0.2, df["X_affiche_1000€"], width=0.4, color="#2f5d7c", label="1 cas sur 20 : perte supérieure à…")
    ax.bar(x + 0.2, df["pire_mois_%"] * 10, width=0.4, color="#c9a227", label="pire mois observé")
    ax.set_xticks(x, df["portefeuille"])
    ax.set_ylabel("€ pour 1 000 € investis")
    ax.set_title("Perte possible en un mois pour 1 000 € investis")
    ax.legend(frameon=False)
    for i, (a, b) in enumerate(zip(df["X_affiche_1000€"], df["pire_mois_%"] * 10)):
        ax.text(i - 0.2, a + 3, f"{a:.0f} €", ha="center", fontsize=8)
        ax.text(i + 0.2, b + 3, f"{b:.0f} €", ha="center", fontsize=8)
    fig.tight_layout()
    fig.savefig(RESULTATS / "comparaison_portefeuilles.png", dpi=150)
    plt.close(fig)

    (RESULTATS / "indicateur.json").write_text(json.dumps(export, ensure_ascii=False, indent=1), encoding="utf-8")
    MAQUETTE_JS.parent.mkdir(parents=True, exist_ok=True)
    MAQUETTE_JS.write_text(
        "// Fichier généré par python/var_indicateur.py — ne pas modifier à la main.\n"
        f"window.INDICATEUR = {json.dumps(export, ensure_ascii=False)};\n",
        encoding="utf-8",
    )
    (RESULTATS / "controles.txt").write_text("\n".join(controles) + "\n", encoding="utf-8")

    pd.set_option("display.width", 200)
    print(df[["portefeuille", "VaR95_affichee_%", "echantillon_retenu", "VaR95_historique_%", "VaR95_5ans_%", "VaR95_normale_%",
              "ES95_historique_%", "ES95_echantillon_retenu_%", "pire_mois_%", "pire_mois_periode",
              "X_affiche_1000€", "X_affiche_10000€"]].to_string(index=False))
    print()
    print(df[["portefeuille", "backtest_mois", "backtest_depassements", "backtest_taux_%", "kupiec_pvalue",
              "christoffersen_pvalue", "variante_historique_seul_taux_%", "variante_historique_seul_kupiec_p",
              "variante_5ans_seuls_taux_%", "variante_5ans_seuls_kupiec_p"]].to_string(index=False))
    print()
    print(pd.DataFrame(sensib).to_string(index=False))
    print()
    print(pd.DataFrame(stress_rows).to_string(index=False))
    print()
    print("\n".join(controles))
    print()
    for cle, pf in PORTEFEUILLES.items():
        v95 = export["portefeuilles"][cle]["var95"]
        print(f"{pf['nom']:>14} | 1 000 € : {phrase(v95, 1_000)} | 10 000 € : {phrase(v95, 10_000)}")


if __name__ == "__main__":
    main()
