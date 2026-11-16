# Deux profils d'utilisateurs

*Livrable du périmètre minimal · version 1 · à valider avec le commanditaire*

Le public prioritaire est celui fixé par le commanditaire : **des particuliers débutants qui n'ont jamais investi**. Nous retenons deux profils contrastés. Ils partagent la même ignorance du risque, mais pas pour les mêmes raisons : la première sous-estime le risque, la seconde le surestime au point de rester bloquée. Une application qui aide les deux doit montrer le risque **en euros, de façon juste**, sans faire peur ni rassurer à tort.

> Ces profils sont des hypothèses construites à partir de tendances publiques sur les nouveaux investisseurs particuliers. Ils doivent être confrontés aux 3 utilisateurs test (voir `06_protocole_test_utilisateurs.md`) et corrigés si besoin.

---

## Profil L — Léa, 24 ans, « la curieuse pressée »

| | |
|---|---|
| **Situation** | Chargée de communication en CDI depuis un an, à Lille. Vit en colocation. |
| **Épargne** | 4 000 € sur un Livret A, alimenté de 150 € par mois. |
| **Rapport à l'investissement** | N'a jamais investi. Voit passer sur TikTok et Instagram des vidéos sur les ETF, la crypto, « l'argent qui travaille ». Deux amis disent avoir « fait +30 % ». |
| **Usage numérique** | Tout sur smartphone, sessions courtes (trajets, pauses). Abandonne une appli au bout de 2 écrans confus. |
| **Phrase type** | « Tout le monde dit qu'il faut investir jeune, mais je ne sais même pas ce que je risque. » |

**Besoins**

| Code | Besoin |
|---|---|
| **L1** | Comprendre vite, sans jargon, sur mobile (sessions de 5 minutes). |
| **L2** | Savoir concrètement combien elle pourrait perdre, **en euros**, avec ses propres montants. |
| **L3** | S'entraîner sans risquer son argent réel. |
| **L4** | Faire la différence entre une information fiable et une promesse de réseau social ; résister à l'impulsivité. |

**Craintes**

- Se faire arnaquer (faux site, « coach » en trading, promesse de rendement garanti).
- Passer à côté (« FOMO ») et regretter de ne pas avoir commencé plus tôt.
- Se sentir jugée ou ridicule parce qu'elle ne connaît pas les termes.

**Risque de comportement à corriger** : chercher le gain rapide, sous-estimer la possibilité de baisses fortes et durables.

---

## Profil N — Nadia, 51 ans, « la prudente qui veut protéger »

| | |
|---|---|
| **Situation** | Gestionnaire administrative dans une mairie, à Nantes. Deux enfants (19 et 16 ans). Départ à la retraite envisagé dans une douzaine d'années. |
| **Épargne** | 25 000 € sur Livret A et LDDS, plus 20 000 € reçus récemment en héritage. |
| **Rapport à l'investissement** | N'a jamais investi. Son conseiller bancaire lui a parlé d'« unités de compte » dans une assurance vie ; elle n'a pas compris et n'a pas osé demander. S'inquiète de l'inflation qui « grignote » son épargne. |
| **Usage numérique** | Ordinateur et tablette, préfère lire à son rythme. Aime pouvoir relire. Texte petit = abandon. |
| **Phrase type** | « Je ne veux pas jouer au casino avec l'argent de ma retraite. Mais je voudrais au moins comprendre ce qu'on me propose. » |

**Besoins**

| Code | Besoin |
|---|---|
| **N1** | Être certaine qu'aucun argent réel n'est en jeu, ni aucun engagement (pas de carte bancaire, pas de vente). |
| **N2** | Comparer des niveaux de risque entre eux, **et avec ce qu'elle connaît** (le Livret A). |
| **N3** | Savoir ce qui peut arriver dans une mauvaise période : ampleur et durée d'une crise. |
| **N4** | Prendre son temps, relire, avoir des explications claires et lisibles (taille du texte). |
| **N5** | Arriver préparée à un rendez-vous avec son conseiller : savoir quelles questions poser. |

**Craintes**

- Perdre l'argent qui doit servir à sa retraite ou aux études de ses enfants.
- Être poussée à acheter un produit, ou que l'application soit une publicité déguisée.
- Ne pas comprendre et devoir faire confiance aveuglément.

**Risque de comportement à corriger** : rester bloquée par une peur diffuse, ou à l'inverse vendre en panique à la première baisse si elle investit un jour.

---

## Ce que les deux profils impliquent pour la conception

| Constat | Conséquence pour l'application |
|---|---|
| L'une sous-estime, l'autre surestime le risque | Montrer un chiffre **juste** (ni alarmiste ni rassurant), puis le pire cas observé. |
| Ni l'une ni l'autre ne parle « finance » | Phrase en euros, pictogramme, glossaire au toucher ; le mot « VaR » n'apparaît que dans une rubrique « Le mot des pros ». |
| Léa est impulsive, Nadia est inquiète | Aucune incitation (pas de classement, pas de confettis sur les gains, pas de notification de marché) ; ton calme. |
| Usages différents (mobile rapide / lecture posée) | Parcours court en 4 étapes, mais tout est relisible ; bouton « Aa » pour agrandir le texte. |
| Les deux craignent l'arnaque ou la vente déguisée | Les 3 engagements (argent virtuel, aucun ordre, aucune promesse) dès l'accueil ; « Règles du jeu » toujours accessibles. |

La correspondance écran par écran figure dans `05_maquette_ecrans.md` (critère d'acceptation : « chaque écran répond à un besoin identifié dans les profils »).
