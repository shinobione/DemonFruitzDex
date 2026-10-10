# V4.5 — clips Crunchyroll et contrôle des sources

Audit **documentaire** : les clips nouveaux sont retrouvés dans les publications de la chaîne officielle Crunchyroll. La lecture en France, le fonctionnement de l'iframe et la disponibilité future ne sont **pas** testés.

| Fruit | Extrait éditeur | Épisode | Source |
|---|---|---|---|
| Hito Hito / Nika | Luffy transforme Saturn et Kizaru en pizza | 1142 | https://www.youtube.com/watch?v=5L_Ek_CcREc |
| Hito Hito / Nika | Gear 5 attaque Saturn | 1141 | https://www.youtube.com/watch?v=MK2DHUoD8pE |
| Ope Ope | Law et Kid contre Big Mom | 1067 | https://www.youtube.com/watch?v=R_tBf1ByqYo |
| Jiki Jiki | La même scène, pour la contribution de Kid | 1067 | https://www.youtube.com/watch?v=R_tBf1ByqYo |
| Magu Magu | Akainu contre Barbe Blanche, partie 1 | 484 | https://www.youtube.com/watch?v=IL2yBUx2Lpc |

**Attention :** la vidéo Akainu / Barbe Blanche était déjà utilisée sur la fiche Gura Gura. Elle est maintenant aussi associée au Magu Magu, sans dupliquer la vidéo.

## Bilan

- **166** fiches dont **69** documentées ; **97** sans scène retenue.
- **34 associations YouTube**, représentant **29 vidéos distinctes**, réparties sur **25 fruits**.
- **84 associations d'épisodes** sur Crunchyroll.
- **5 nouvelles associations** avec métadonnées de provenance explicites ; les anciennes associations n'ont pas toutes ce niveau de contrôle.
- **4 miniatures** mises en avant sur l'accueil, menant vers les fiches avec playlist.
- Les 40 références historiques identifiées par le rapport V4.4 restent à revoir.

## Vérifications reproductibles

```sh
python scripts/validate_clips.py
python scripts/check_v45.py
node --check app.js
node --check data/clips.js
```

Ces contrôles détectent les incohérences internes et les doublons **sans** prétendre valider la lecture vidéo ou l'autorisation d'intégration. Aucun extrait de l'anime n'est téléchargé, réencodé ou redistribué par le dépôt.
