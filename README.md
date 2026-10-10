# 🍎 DemonFruitzDex — SHINO EDITION V4

Encyclopédie fan-made et interactive des Fruits du Démon de **One Piece**, en français.

**Site :** https://shinobione.github.io/DemonFruitzDex/

## Édition V4

- **166 fiches** dans l'édition actuelle (fruits naturels + cas non nommés + copies artificielles). Ce total **n'est pas un décompte canon officiel de fruits naturels distincts**.
- **Français en nom principal**, suivi du nom original japonais **romanisé** (pas en kanji/kana). Les traductions françaises sont **descriptives** et peuvent différer des localisations officielles.
- **133 références** d'images des fruits/pouvoirs tirées des noms de fichiers de la galerie *One Piece Wiki* ; ces références peuvent ne pas toutes être valides ou chargeables.
- **121 fiches associées** à une URL de portrait d'utilisateur potentielle. Les images distantes sont non garanties : un avatar de secours reste visible si le média ne charge pas.
- **Six clips MP4 originaux** pour les principaux effets : feu, foudre, ténèbres, glace, gravité et élasticité. Les clips sont silencieux, en boucle et stockés dans `assets/powers/`.
- Pour les autres fruits : **moteur Canvas d'animations procédurales**, conçu pour rendre une sensation visuelle du pouvoir ; ce ne sont **pas des extraits de l'anime**.
- Recherche en français/japonais romanisé, filtres familles/éveil/tier/images, tri, affichage progressif.
- **Favoris** stockés localement dans le navigateur et **comparateur de deux fruits**.
- Fiches en modal avec animation, lecteur pause/reprise, utilisateur illustré, sources, navigation et lien direct `?fruit=...`.
- Adapté mobile et desktop, respecte `prefers-reduced-motion`.

## Lancer

En ligne, publier `main` avec GitHub Pages, source `/(root)`.

Localement : `python -m http.server 8000`, puis `http://localhost:8000/`. Le site ne nécessite pas de build ou npm. Une fois téléchargé comme dossier complet, les liens relatifs et clips doivent rester ensemble.

## Architecture

```
index.html                 Interface et sémantique
styles.css                 Responsive + direction artistique
app.js                     Recherche, favoris, duel, animations Canvas
data/fruits.json           Source éditoriale des fiches
data/fruits.js             Export pour fonctionnement local sans fetch()
assets/icon.svg           Icône SVG originale
assets/powers/*.mp4       Vidéos originales générées procéduralement
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

**Les six vidéos sont produites par un générateur original de motifs/particules.** Le projet **n'héberge aucune séquence copiée de l'anime, aucun GIF extrait, aucune musique ni séquence Toei**. Ne pas ajouter d'extraits officiels sans autorisation adaptée. Tous les personnages et designs de *One Piece* appartiennent à leurs ayants droit (Eiichiro Oda / Shueisha / Toei).

Les classements `S+` → `C` sont subjectifs ; certaines classifications récentes du manga demandent une vérification fine (notamment les formes des Doyens et des Chevaliers Divins). Ne pas utiliser la base comme référence canon certifiée sans citer les chapitres/SBS.

## Pistes V4.1

1. Valider chaque URL de portrait/fruit et indiquer si l'illustration a été chargée.
2. Ajouter de vrais extraits officiels **uniquement si la redistribution est autorisée**.
3. Créer un workflow CI de validation des données et des noms uniques.
4. Crédits par illustration et chapitres source.
5. Importer les futurs chapitres avec une séparation canon / théorie / info à vérifier.


## V4.1 — les pouvoirs en action (10 octobre 2026)

- Les animations abstraites ne sont plus utilisées dans les fiches. À la place, **16 fiches** proposent une scène d’anime publiée par les chaînes Crunchyroll, Crunchyroll FR, Crunchyroll Dubs ou Toei Animation sur YouTube. La vidéo n’est chargée qu’au clic, avec un lien alternatif direct vers la chaîne.
- Plusieurs autres fruits renvoient à un épisode Crunchyroll précisément référencé ; aucune vidéo non vérifiée n’est présentée comme étant la démonstration d’un pouvoir.
- Le portrait de l’utilisateur est agrandi sur les cartes et occupe un grand panneau dans la fiche ouverte. Le fruit reste visible dans un encart distinct. Les images proviennent de liens externes du One Piece Wiki et certains portraits peuvent ne pas charger.
- Métadonnées éditables dans `data/clips.json`, export navigateur dans `data/clips.js`.
- Aucun extrait de l’anime n’est téléchargé, coupé, réencodé ni redistribué par ce dépôt. Les lecteurs intégrés suivent les restrictions et droits du fournisseur. Les anciens MP4 originaux dans `assets/powers/` sont obsolètes et ne sont plus chargés.
