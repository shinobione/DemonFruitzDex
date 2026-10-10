# DemonFruitzDex V4.8 — Audit portraits et illustrations

**Date :** 10 octobre 2026. **Portée :** références documentaires, intégrité JavaScript, déploiement des fichiers sur `main`. Cette étape **ne garantit pas la réponse HTTP ni l'affichage de chaque image distante**.

## État

| Indicateur | V4.7 | V4.8 | Delta |
|---|---:|---:|---:|
| Fiches du catalogue | 166 | 166 | 0 |
| Portraits avec URL enregistrée | 134 | 154 | +20 |
| Portraits sans URL | 32 | 12 | -20 |
| Illustrations de fruit / pouvoir avec URL | 136 | 140 | +4 |
| Illustrations sans URL | 30 | 26 | -4 |
| Associations de clips YouTube | 36 | 36 | 0 |

**Ce sont des comptes de références**, pas de fichiers lisibles ou téléchargés.

## Lot de portraits V4.8

Références `data/portraits-v48.js`, obtenues à partir des noms de fichiers indexés dans des catégories Wiki :

- **Borsalino/Kizaru** : `Borsalino PW Portrait.png` — jeu *Pirate Warriors*, et non portrait canon de l'anime.
- **Kabu** : `Kabu Portrait.png`.
- **Famille Charlotte** : Perospero, Mont-d'Or, Smoothie, Daifuku, Oven, Streusen, Galette, Opera.
- **Séraphins** : S-Hawk, S-Bear, S-Shark.
- **Impel Down** : Minotaurus, Minokoala, Minorhinoceros, Minozebra.
- **Marines, plus jeunes** : Sharinguru, Shu.
- **Tama** : `Tama at Age 4.png`, image de personnage plus jeune.

Sources catalogues : [Portraits](https://onepiece.fandom.com/wiki/Category:Character_Portraits), [personnages dans le passé](https://onepiece.fandom.com/wiki/Category:Character_Past_Portraits), [Wano – épisode saison 20](https://onepiece.fandom.com/wiki/Category:Season_20_Episode_Images), [Impel Down – saison 13](https://onepiece.fandom.com/wiki/Category:Season_13_Episode_Images). Les autres catégories pertinentes sont identifiées dans le manifeste.

## Illustrations des capacités des Séraphins

Ce sont des images de **pouvoirs utilisés** et **non** des fruits physiques :

- S-Hawk : `Artificial Supa Supa no Mi.png` — lames, source page Supa Supa no Mi.
- S-Shark : `Sui Sui no Mi Water Depiction.png` — nage dans une surface, source galerie saison 21.
- S-Bear : `S-Bear Uses Ursus Shock.png` — Nikyu Nikyu, source galerie saison 21.
- S-Snake : `S-Snake Petrifies CP0 Agents.png` — Mero Mero, source galerie saison 21.

Voir `data/power-art-v48.js`.

## 12 portraits encore sans référence

Épée Cerberus, Pierre, Smiley, Very Good, Giolla, Machvise, Morley, groupe des consommateurs de SMILE (pas de porteur unique), Buffalo, Charlotte Newshi, Kelly Funk, Urban.

## Images non canoniques, source et tests

La plupart des fruits physiques encore sans illustration n'ont pas d'apparence officielle connue. Le Dex ne doit pas transformer une représentation de pouvoir en fruit « canon ».

Les anciens liens `static.wikia.nocookie.net` peuvent être invalides, refusés en hotlink, ou indisponibles régionalement. Le navigateur tente maintenant :

1. URL de fichier direct provenant de la convention MediaWiki.
2. `Special:Redirect/file/<nom du fichier>`.
3. Affichage d'un pictogramme et d'un message *image externe indisponible* en cas d'échec.

Le nouvel outil **[Media Check](../media-check.html)** teste jusqu'à 30 références récentes ou la totalité de la liste, puis télécharge un rapport JSON depuis ton navigateur. Aucun droit de réhébergement implicite n'est accordé sur les images sous droits.

**À faire :** lancer Media Check en France, corriger les URL qui échouent, ensuite seulement chercher les 12 portraits et 26 représentations manquants restants.
