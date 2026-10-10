# 🍎 DemonFruitzDex — SHINO EDITION V4.2 · ANIME ARCHIVE

Encyclopédie fan-made et interactive des Fruits du Démon de **One Piece**, en français.

**Site :** https://shinobione.github.io/DemonFruitzDex/

## Édition V4.2

- **166 fiches** dans l'édition actuelle (fruits naturels + cas non nommés + copies artificielles). Ce total **n'est pas un décompte canon officiel de fruits naturels distincts**.
- **Français en nom principal**, suivi du nom original japonais **romanisé** (pas en kanji/kana). Les traductions françaises sont **descriptives** et peuvent différer des localisations officielles.
- **133 références** d'images des fruits/pouvoirs tirées des noms de fichiers de la galerie *One Piece Wiki* ; ces références peuvent ne pas toutes être valides ou chargeables.
- **121 fiches associées** à une URL de portrait d'utilisateur potentielle. Les images distantes sont non garanties : un avatar de secours reste visible si le média ne charge pas.
- **18 fiches avec des références à des clips vidéo sur YouTube** (à vérifier au chargement selon la région). L’extrait est **intégré à la demande** via le lecteur officiel ; **aucune séquence protégée n’est hébergée par le dépôt**.
- **Plus de 40 fruits disposent maintenant d’au moins une scène documentée**, dont des extraits YouTube ou des pages d’épisodes Crunchyroll. **Plus de 50 références d’épisodes** sont indexées (plusieurs pour certains fruits). Quand aucun extrait n’est vérifié, le site le dit : aucun faux extrait, aucune vidéo d’un autre fruit.
- Les six anciennes vidéos abstraites de V4 restent dans `assets/powers/` pour l’historique, mais ne sont plus utilisées dans le Dex.
- Recherche en français/japonais romanisé, filtres familles/éveil/tier/images, tri, affichage progressif.
- **Favoris** stockés localement dans le navigateur et **comparateur de deux fruits**.
- Fiches en modal immersive, **portrait utilisateur grand format**, fruit séparé, extrait animé officiel sur clic, sources, navigation et lien direct `?fruit=...`.
- Adapté mobile et desktop, respecte `prefers-reduced-motion`.

## Lancer

En ligne, publier `main` avec GitHub Pages, source `/(root)`.

Localement : `python -m http.server 8000`, puis `http://localhost:8000/`. Le site ne nécessite pas de build ou npm. Une fois téléchargé comme dossier complet, les liens relatifs et clips doivent rester ensemble.

## Architecture

```
index.html                 Interface et sémantique
styles.css                 Responsive + direction artistique
app.js                     Recherche, favoris, duel, lecteur officiel
data/fruits.json           Source éditoriale des fiches
data/fruits.js             Export pour fonctionnement local sans fetch()
data/clips.json             Sélection des vidéos officielles vérifiées
data/clips.js               Export navigateur de la sélection
assets/icon.svg           Icône SVG originale
assets/powers/*.mp4       Anciennes vidéos originales (V4, désormais inutilisées)
scripts/build_data.py     Enrichissement initial de la V3 (nécessite les fichiers source de la phase de migration)
scripts/export_data.py    Export JSON vers JS
scripts/render_loops.py   Générateur des animations MP4 originales
```

Éditer `data/fruits.json`, puis exécuter `python scripts/export_data.py`.

## Illustrations, sources et limites

- [One Piece Wiki — galerie Fruits du Démon](https://onepiece.fandom.com/wiki/Category:Devil_Fruit_Infobox_Images)
- [One Piece Wiki — portraits](https://onepiece.fandom.com/wiki/Category:Character_Anime_Infobox_Images)
- [One Piece Wiki — images d'utilisation des pouvoirs](https://onepiece.fandom.com/wiki/Category:Devil_Fruit_Usage_Images)

Les illustrations externes sont **liées à leur source**, non copiées dans le repo. Certains liens sont proposés à partir d'un nom de fichier présumé et doivent encore être vérifiés **un par un** : une image cassée peut déclencher l'avatar de secours, et un fichier tiers peut changer sans préavis.

**Les extraits d’anime sont visionnés directement chez Crunchyroll sur YouTube, par lecteur intégré**, sous réserve des restrictions de lecture, de géoblocage et d’intégration. Ce dépôt **ne copie ni n’héberge les images animées/audio de Toei** ; aucune autorisation de redistribution de ces séquences n’est revendiquée. Tous les personnages et designs de *One Piece* appartiennent à leurs ayants droit (Eiichiro Oda / Shueisha / Toei).

Les classements `S+` → `C` sont subjectifs ; certaines classifications récentes du manga demandent une vérification fine (notamment les formes des Doyens et des Chevaliers Divins). Ne pas utiliser la base comme référence canon certifiée sans citer les chapitres/SBS.

## Pistes V4.3

1. Valider chaque URL de portrait/fruit et indiquer si l'illustration a été chargée.
2. Ajouter de vrais extraits officiels **uniquement si la redistribution est autorisée**.
3. Créer un workflow CI de validation des données et des noms uniques.
4. Crédits par illustration et chapitres source.
5. Importer les futurs chapitres avec une séparation canon / théorie / info à vérifier.

## Vidéothèque de l’anime — V4.2

- Sources officielles prioritaires : chaînes **Crunchyroll**, **Crunchyroll FR**, **Toei Animation** sur YouTube, pages d’épisodes **Crunchyroll** et un clip vidéo publié par le compte Facebook officiel One Piece.
- **Plusieurs clips par fruit**, avec sélecteur de miniatures et arrêt du lecteur précédent lorsque l’on change de clip ou de fiche.
- **Filtres « Extraits / épisodes officiels »** pour limiter le catalogue aux fiches qui possèdent une scène associée.
- Pour les épisodes seuls, **un lien externe explicite vers le diffuseur** remplace le lecteur vidéo. Un épisode complet n’est **pas** un extrait court : les deux types sont distingués dans l’interface.
- **Aucun extrait de l’anime n’est téléchargé, réencodé, ni commité dans ce dépôt.** Les anciens MP4 abstraits ne sont pas lus dans les fiches.
- Les associations figurent dans `data/clips.json`, dont `data/clips.js` est l’export local chargé par le navigateur. Chaque fiche a une date de revue ; les restrictions géographiques / d’intégration des plateformes ne sont pas garanties.
- Une occurrence d’utilisateur dans une scène **ne suffit pas** : le pouvoir doit y être visible ou le descriptif de l’épisode doit l’attester. Certaines scènes de combat montrent plusieurs utilisateurs, et les fiches correspondantes sont créditées séparément.
- **Attention** : une partie des clips YouTube préexistants a été conservée sans contrôle individuel de lecture sur le réseau. La validation de l'existence des références ne prouve pas l'autorisation d'intégration.

### Vérification de la vidéothèque

```bash
python scripts/validate_clips.py
```

Ce validateur vérifie la structure, l’unicité des liens par fiche, les IDs YouTube et la référence des fruits. Il **ne** vérifie **pas** le caractère visionnable des vidéos dans chaque pays ; cette vérification est manuelle et dépend du diffuseur.