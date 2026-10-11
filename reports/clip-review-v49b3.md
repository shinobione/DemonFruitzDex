# DemonFruitzDex V4.9.b3 — 50 clips / 36 fruits et parcours de curation

**Date :** 11 octobre 2026. **Statut :** PR Draft ; la lecture effective en France n'a pas été vérifiée. La CI ne valide que structure, JavaScript et liens.

## Évolution du lot

| Étape | Associations YouTube | Fruits concernés |
|---|---:|---:|
| Base V4.9.a | 37 | 25 |
| V4.9.b2 | 45 | 31 |
| V4.9.b3 | **50** | **36** |

**5 références vidéo nouvelles** sont associées à des fiches précédemment sans scène sélectionnée :

| Fruit et porteur | ID vidéo | Chaîne | Format | Évidence documentaire |
|---|---|---|---|---|
| [Noro Noro / Foxy](https://www.youtube.com/watch?v=1hh_5xUZ5Mw) | `1hh_5xUZ5Mw` | Rensuka Ren | Compilation | Titre / description YouTube identifiant Foxy, Noro Noro et ralentissement |
| [Doa Doa / Blueno](https://www.youtube.com/watch?v=HnsL-5GHUrc) | `HnsL-5GHUrc` | Rensuka Ren | Compilation | Titre / description YouTube identifiant Blueno, portes du Doa Doa |
| [Yuki Yuki / Monet](https://www.youtube.com/watch?v=oLRxJVxoWWo) | `oLRxJVxoWWo` | Rensuka Ren | Compilation | Titre / description YouTube identifiant Monet et neige |
| [Ito Ito / Doflamingo](https://www.youtube.com/watch?v=ow1Hpfnlri4) | `ow1Hpfnlri4` | Koi 鯉 | Compilation | Métadonnées du montage Doflamingo et description mentionnant Ito Ito / Birdcage |
| [Pero Pero / Perospero](https://www.youtube.com/watch?v=5r92RNbFpz4) | `5r92RNbFpz4` | Koi 鯉 | Compilation | Titre / description YouTube identifiant Perospero ; pouvoirs de bonbon à confirmer dans la scène |

**Important :** sources communautaires ; *métadonnées identifiées* ≠ vidéo lisible, iframe permise, scène du pouvoir contrôlée, ni autorisation de redistribution. Aucun extrait n'est téléchargé ou hébergé dans le dépôt. Les **liens vers les épisodes complets Crunchyroll restent absents**.

## Étape 2 — boucle de qualité dans la fiche

Les résultats humains de `CLIP CHECK` sont stockés uniquement sur l'appareil dans `localStorage` (`demonfruitzdex.clip-review.v49b`). Quand ce même navigateur revient sur une fiche :

- `embed-ok` : la fiche signale une validation **locale**, jamais globale ;
- `youtube-only`, `login-required`, `unavailable`, `wrong-power`, `other` : affiche un avertissement local et suspend la lecture intégrée **pour cette vidéo sur ce navigateur** ; le lien de revue et l'accès à YouTube sont conservés ;
- si plusieurs vidéos existent, la fiche choisit par défaut un clip localement accepté, sinon un clip non signalé, sinon le premier candidat avec avertissement ;
- les liens de partage précisant `?clip=...` restent prioritaires ;
- le message d'ouverture d'iframe ne prétend plus qu'une lecture vidéo a eu lieu.

Ce mécanisme ne modifie pas le catalogue GitHub ni l'expérience des autres visiteurs.

## Étape 3 — importer un audit CLIP CHECK

`clip-check.html` accepte de réimporter un rapport précédemment exporté :

- schéma explicite `demonfruitzdex.clip-review.v1`, taille du JSON **≤ 1 Mo**, maximum 500 entrées ;
- association uniquement aux couples fruit + ID vidéo **déjà présents** dans le Dex ;
- seuls les verdicts connus et datés sont retenus (aucun `pending` promu en vérifié) ;
- si un verdict local plus récent existe, il est conservé ;
- les résultats restent sur le navigateur et doivent être exportés volontairement.

## Étape 4 — suggérer directement depuis une fiche

Sous les recherches YouTube et Google Vidéos : **« J’ai trouvé une vidéo de ce pouvoir »** ouvre `clip-check.html?fruit=<id>&suggest=1`, avec le fruit préselectionné.

- accepte une URL YouTube `watch`, `youtu.be`, `shorts`, `live` ou `embed` en **HTTPS** ;
- rejette les faux domaines / ID incorrects / doublons déjà sélectionnés ;
- conserve localement l'ID, le fruit et une note de scène facultative ;
- exporte un fichier au schéma `demonfruitzdex.clip-proposals.v1` ;
- ces propositions portent `status:unverified-user-proposal`, **jamais intégrées automatiquement**, et nécessitent vérification éditoriale (contenu, titre, droits d'embed, absence d'abonnement, région).

Cette voie accélère la récupération des clips trouvés par les visiteurs sans présenter les résultats de recherche comme validés.

## Étape 5 — QA et promotion

`scripts/check_v49b3.py` teste : comptage de 50 associations, 36 fruits, cohérence JSON/JS via autres validateurs, absence de liens d'épisodes complets, UI de revue, import borné, propositions locales et parser d'URL YouTube (cas bons/malformés), plus syntaxe JS inline dans Node.

**Avant fusion :** exécuter CLIP CHECK en France sur les 13 nouvelles associations de V4.9.b, tester le lecteur et l'URL YouTube directe sans compte, relever les minutages et remplacer les références problématiques. Aucun résultat « playback verified » ne peut être généré par les tests statiques.

Les **130** fiches sans vidéo ont toujours une recherche YouTube et une voie de proposition. Le backlog reste à enrichir.
