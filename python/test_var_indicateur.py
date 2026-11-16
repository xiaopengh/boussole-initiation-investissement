"""Contrôles unitaires de var_indicateur.py.

Usage : python test_var_indicateur.py   (ou : python -m pytest test_var_indicateur.py)
Aucune connexion réseau n'est nécessaire.
"""

import math

import numpy as np
import pandas as pd

import var_indicateur as vi


def test_arrondi_par_exces():
    assert vi.arrondi_par_exces(30.07) == 31
    assert vi.arrondi_par_exces(556.17) == 560
    assert vi.arrondi_par_exces(19.96) == 20
    assert vi.arrondi_par_exces(20.0) == 20  # pas d'arrondi supplémentaire sur une valeur exacte
    assert vi.arrondi_par_exces(1234) == 1300
    for x in np.random.default_rng(0).uniform(1, 10_000, 500):
        assert vi.arrondi_par_exces(x) >= x  # ne sous-estime jamais


def test_var_historique_sur_serie_connue():
    # 100 rendements de -0,50 à +0,49 : quantile 5 % (interpolation linéaire) = -0,4505
    r = pd.Series(np.arange(-50, 50) / 100)
    assert math.isclose(vi.var_historique(r), 0.4505, abs_tol=1e-12)
    # ES = moyenne des rendements <= -0,4505 : -0,50 … -0,46 → 0,48
    assert math.isclose(vi.es_historique(r), 0.48, abs_tol=1e-12)


def test_portefeuille_mono_actif_egal_au_prix():
    idx = pd.bdate_range("2020-01-01", periods=80)
    rng = np.random.default_rng(1)
    prix = pd.DataFrame({"a": 100 * np.cumprod(1 + rng.normal(0, 0.01, 80)),
                         "b": 50 * np.cumprod(1 + rng.normal(0, 0.01, 80))}, index=idx)
    v = vi.valeur_portefeuille(prix, {"a": 1.0, "b": 0.0})
    assert np.allclose(v.to_numpy(), (prix["a"] / prix["a"].iloc[0]).to_numpy())


def test_reequilibrage_mensuel():
    # Deux actifs : A double le 1er mois puis stagne ; B stagne. 50/50 rééquilibré chaque mois.
    idx = pd.bdate_range("2021-01-01", "2021-03-31")
    a = pd.Series(1.0, index=idx)
    a[idx >= "2021-01-29"] = 2.0  # le doublement a lieu fin janvier
    prix = pd.DataFrame({"a": a, "b": 1.0})
    v = vi.valeur_portefeuille(prix, {"a": 0.5, "b": 0.5})
    assert math.isclose(v.loc["2021-01-29"], 1.5)  # 0,5 × 2 + 0,5 × 1
    assert math.isclose(v.iloc[-1], 1.5)  # ensuite plus rien ne bouge


def test_estimation_sans_regard_vers_le_futur():
    # Modifier les cours APRÈS t ne doit pas changer la VaR estimée à t (pas de biais d'anticipation).
    rng = np.random.default_rng(2)
    v = np.cumprod(1 + rng.normal(0.0003, 0.01, 3000))
    t = 2000
    avant = vi.estimer_var(v[: t + 1])["var"]
    v2 = v.copy()
    v2[t + 1:] *= 0.5
    assert vi.estimer_var(v2[: t + 1])["var"] == avant


def test_regle_de_prudence():
    rng = np.random.default_rng(3)
    calme = rng.normal(0.0003, 0.005, 3000)
    agite = rng.normal(0.0, 0.02, 1300)
    v = np.cumprod(1 + np.concatenate([calme, agite]))
    est = vi.estimer_var(v)
    assert est["var"] == max(est["var_tout"], est["var_recent"])
    assert est["echantillon_nom"] == "5 dernières années"  # la période récente, plus agitée, l'emporte


def test_kupiec():
    lr, p = vi.kupiec(100, 5, 0.05)
    assert math.isclose(lr, 0.0, abs_tol=1e-9) and math.isclose(p, 1.0)
    assert vi.kupiec(148, 15, 0.05)[1] < 0.05  # 10 % de dépassements : rejeté
    assert vi.kupiec(148, 11, 0.05)[1] > 0.05  # 7,4 % : non rejeté


if __name__ == "__main__":
    tests = [f for n, f in sorted(globals().items()) if n.startswith("test_")]
    for f in tests:
        f()
        print(f"OK  {f.__name__}")
    print(f"{len(tests)} contrôles réussis")
