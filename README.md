# 🍎 DemonFruitzDex — SHINO EDITION V4.3 · ANIME ARCHIVE

Encyclopédie fan-made et interactive des Fruits du Démon de **One Piece**, en français.

**Site :** https://shinobione.github.io/DemonFruitzDex/

## Édition V4.3

- **166 fiches** dans l'édition actuelle (fruits naturels + cas non nommés + copies artificielles). Ce total **n'est pas un décompte canon officiel de fruits naturels distincts**.
- **Français en nom principal**, suivi du nom original japonais **romanisé** (pas en kanji/kana). Les traductions françaises sont **descriptives** et peuvent différer des localisations officielles.
- **133 références** d'images des fruits/pouvoirs tirées des noms de fichiers de la galerie *One Piece Wiki* ; ces références peuvent ne pas toutes être valides ou chargeables.
- **121 fiches associées** à une URL de portrait d'utilisateur potentielle. Les images distantes sont non garanties : un avatar de secours reste visible si le média ne charge pas.
- **22 fiches disposant d’au moins une référence YouTube** (à vérifier au chargement selon la région). L’extrait est **intégré à la demande** via le lecteur officiel ; **aucune séquence protégée n’est hébergée par le dépôt**.
- **56 fruits disposent maintenant d’au moins une scène documentée**, dont des extraits YouTube ou des pages d’épisodes Crunchyroll. **70 références d’épisodes** sont indexées (plusieurs pour certains fruits). Quand aucun extrait n’est vérifié, le site le dit : aucun faux extrait, aucune vidéo d’un autre fruit.
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

## Pistes suivantes

1. Valider chaque URL de portrait/fruit et indiquer si l'illustration a été chargée.
2. Ajouter de vrais extraits officiels **uniquement si la redistribution est autorisée**.
3. Créer un workflow CI de validation des données et des noms uniques.
4. Crédits par illustration et chapitres source.
5. Importer les futurs chapitres avec une séparation canon / théorie / info à vérifier.

## Vidéothèque de l’anime — V4.3

- Sources officielles prioritaires : chaînes **Crunchyroll**, **Crunchyroll FR**, **Toei Animation** sur YouTube, pages d’épisodes **Crunchyroll** et un clip vidéo publié par le compte Facebook officiel One Piece.
- **Plusieurs clips par fruit**, avec sélecteur de miniatures et arrêt du lecteur précédent lorsque l’on change de clip ou de fiche.
- **Filtres « Scène documentée » et « Extrait YouTube uniquement »** pour limiter le catalogue aux fiches qui possèdent une scène associée.
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

## Extension du 10 octobre 2026 — V4.3

- **56 fruits documentés sur 166** contre 40 précédemment : +16 fruits.
- **26 associations à des vidéos YouTube** (certaines couvrent plusieurs fruits), et **70 liens vers des épisodes**.
- 16 nouveaux fruits référencés avec des scènes de Ryokugyu, Bonney, Queen, Hawkins, Perona, Bartolomeo, Cracker, Tama, Ulti, Page One, Toki, Absalom, Sasaki, Who's-Who, Monet et Momonosuke (fruit artificiel).
- Les clips ajoutés sont publiés par les chaînes **Crunchyroll**, **Crunchyroll FR** ou **Toei Animation**. La vidéo Toei de Bonney est **une bande-annonce de l'épisode 1152** et l'interface la signale comme telle.
- Deux filtres distincts : **scène documentée** (épisode ou clip) et **extrait YouTube uniquement**. Nouveau tri **Extraits d'abord**.
- Pour les fruits sans scène retenue, lien de **recherche YouTube** explicitement non vérifié, et non une fausse source officielle.
- Le dossier `data/clips.json` stocke un lien exact vers la source du diffuseur pour les nouvelles entrées (`sourceEvidence`, `reviewedOn`) : cela facilite la maintenance et évite la fabrication de liens.
- **Aucune redistribution de vidéos de l'anime** ; les liens renvoient vers leurs éditeurs. Les restrictions de visionnage en France et d'intégration restent à confirmer depuis un navigateur utilisateur.

### Points restant à auditer

Le validateur vérifie la **structure**, les IDs, les doublons et les domaines, pas la lecture réelle ou les droits des vidéos. Toutes les anciennes références n'ont pas encore fait l'objet du contrôle documentaire que reçoivent les nouvelles entrées.

## Mise à jour V4.4 — extrait documentaire et contrôle qualité

- **69 fruits avec au moins une référence** sur 166, contre 56 dans la version précédente.
- **29 associations YouTube** correspondant à 26 vidéos distinctes ; **84 associations à des épisodes** correspondant à 75 épisodes distincts.
- Nouveaux fruits documentés notamment : Baku Baku (Wapol), Doru Doru (Mr. 3), Mane Mane (Bon Clay), Supa Supa (Mr. 1), Toge Toge (Miss Doublefinger), Mogu Mogu (Miss Merry Christmas), Noro Noro (Foxy), Doa Doa (Blueno), Awa Awa (Kalifa), Bane Bane (Bellamy), Inu Inu Loup (Jabra), Zo Zo Mammouth (Jack) et Tama Tama (Baron Tamago).
- **Trois clips YouTube publiés par Crunchyroll** : Bon Clay imite les Mugiwara ; Zoro contre Mr. 1 parties 1 et 2. Le fruit de Chopper reçoit aussi un épisode de référence.
- Les nouvelles pages d’épisode sont identifiées dans le catalogue officiel **Crunchyroll**, mais le minutage exact des pouvoirs n'a pas été contrôlé.
- Générer un audit documentaire : `python scripts/audit_sources.py`. Résultats dans [reports/media-audit.md](reports/media-audit.md) et [reports/media-audit.json](reports/media-audit.json).
- Le contrôle structurel reste : `python scripts/validate_clips.py`. Il ne certifie ni le fonctionnement du lecteur intégré, ni l'absence de blocage régional.
- Il reste **97 fiches sans extrait ou épisode retenu** et **40 fiches historiques** dont la provenance à la racine nécessite un contrôle éditorial complémentaire.


## Mise à jour V4.5 — clips courts vérifiés au niveau des métadonnées

- 69 fruits avec scène sur 166, dont 25 avec un clip YouTube.
- 34 associations YouTube / 29 vidéos distinctes, et 84 références d'épisodes.
- Cinq nouvelles associations : Gear 5 à Egghead (deux séquences), Law et Kid contre Big Mom (deux fiches), Akainu contre Barbe Blanche.
- Quatre scènes mises en avant sur l'accueil, en ouvrant la fiche du fruit correspondant.
- Métadonnée `verificationStatus: publisher-metadata-verified` sur les nouvelles associations : **provenance du diffuseur identifiée**, lecture/iframe/géoblocage non testés.
- Correctif de l'étiquette « Clip vidéo » pour les fiches dont les vidéos figurent uniquement dans `moreVideos`.
- Nouveau contrôle `python scripts/check_v45.py` ; détails dans [l'audit V4.5](reports/clip-review-v45.md).
- Aucun extrait d'anime n'est réhébergé.


## V4.6 — audit des sources historiques

Cette étape privilégie la **fiabilité** plutôt que de rajouter des extraits non contrôlés.

- 40 fiches historiques ont subi des contrôles automatiques de structure et de cohérence ; **39 nécessitent encore une revue éditoriale**, une attribution a été corrigée.
- Le clip `I752TYMkM7Y` (*Luffy and Law Combo*) est retiré de la fiche **Doflamingo / Ito Ito** : il n'illustrait pas suffisamment le pouvoir de ses fils. Les épisodes 727 et 731 restent disponibles.
- Les doublons des épisodes **796 (Big Mom), 1121 (Kuzan) et 913 (Kaido)** ont été éliminés sur la base de l'identifiant Crunchyroll (indépendamment du préfixe de langue).
- Les fiches concernées arborent **« À REVOIR »**, une explication et une réserve sur les liens d'épisodes ; nouveau filtre **« Sources à contrôler »**.
- Bilan : **69 fruits documentés**, **33 associations YouTube** représentant **28 vidéos distinctes**, **81 liens d'épisodes** représentant **71 épisodes distincts**.
- Quatre vidéos historiques ont des métadonnées identifiées indépendamment (Gear 5 contre Kaido, Barbe Blanche contre Akainu, Kid et Law contre Big Mom, Robin et Demonio Fleur). Cela **ne constitue pas un contrôle de lecture**.
- Audit détaillé : [reports/media-audit-v46.md](reports/media-audit-v46.md), [version JSON](reports/media-audit-v46.json).
- Qualité reproductible : `python scripts/check_v46.py` (en plus des validateurs précédents).

**Limite :** le navigateur de l'utilisateur peut rencontrer des blocages d'intégration ou de territoire ; aucune compatibilité de lecture en France n'a été certifiée.

## V4.7 — Sources vidéo et portraits

- Recherche YouTube et Google Vidéos désormais disponible dans les 166 fiches, y compris celles qui proposent déjà un épisode Crunchyroll.
- Trois extraits ADN sur YouTube ajoutés : Luffy Gear 5 (aLG9XoxJE7g), Gear 5 à Elbaph (SJtADPK0fKQ), Robin Demonio Fleur (IRXco8fXxBE).
- Treize portraits ou images de personnages supplémentaires attribués à des fichiers présents dans des catégories One Piece Wiki. Voir `data/portrait-sources.js`.
- 134 fiches avec URL de portrait, 32 sans. 136 fiches avec visuel de fruit ou de pouvoir référencé, 30 sans. Trois nouvelles images de pouvoir : Numa Numa, Wapu Wapu (GIF) et forme Zoan loup de Jabra.
- 36 associations YouTube dans la sélection éditoriale, sur 69 fruits disposant de scènes référencées.
- Les vidéos restent chez leurs diffuseurs. Disponibilité par pays, intégration et affichage des images distantes non certifiés.


## V4.8 — Portraits sourcés et fiabilité des visuels

Cette édition ajoute **20 nouvelles références de portraits** provenant de noms de fichiers réellement listés dans les galeries du One Piece Wiki : Kizaru, Kabu, plusieurs membres de la famille Charlotte, les trois Séraphins S-Hawk/S-Bear/S-Shark, les quatre gardiens Zoan d'Impel Down, Sharinguru, Shu et Tama. Fichier : [data/portraits-v48.js](data/portraits-v48.js).

Elle ajoute également **4 illustrations de pouvoirs des Séraphins**, clairement étiquetées comme telles (aucune n'est l'apparence d'un « fruit Green Blood ») : [data/power-art-v48.js](data/power-art-v48.js).

**Bilan de présence de références (et NON de chargement effectif) :** 154 / 166 portraits, 140 / 166 illustrations de fruit/pouvoir ; il reste 12 portraits et 26 illustrations à documenter.

Les images distantes sont fragiles : le site tente maintenant une seconde URL de redirection MediaWiki quand un lien direct échoue, puis affiche un indicateur d'indisponibilité au lieu de masquer le défaut. Un fichier référencé n'est pas nécessairement visible en France ou dans tous les navigateurs.

**Nouveau : [MEDIA CHECK](media-check.html)** — outil intégré qui teste le chargement réel depuis ton navigateur (30 images ou toutes les images), puis permet d'exporter les échecs au format JSON. L'outil ne télécharge pas les images dans le dépôt.

Contrôles :
```bash
python scripts/check_v48.py
node --check app.js
node --check data/portraits-v48.js
node --check data/power-art-v48.js
```
Rapport détaillé : [reports/media-audit-v48.md](reports/media-audit-v48.md).


## V4.9 — portraits d'utilisateurs et vraie provenance vidéo

- **162 / 166 portraits avec une URL**, contre 154 auparavant : huit nouveaux fichiers sourcés via les galeries du One Piece Wiki. Voir [data/portraits-v49.js](data/portraits-v49.js).
- **140 / 166 images de fruits et pouvoirs avec une URL**, inchangé. Pour **24 des 26 cartes** sans illustration propre, le site affiche désormais **le portrait de l'utilisateur en grand**, accompagné de « PORTEUR · FRUIT NON REPRÉSENTÉ » : jamais présenté comme une photo du fruit.
- **37 associations YouTube** (32 vidéos distinctes). L'extrait **Smoker contre Luffy** est publié par *Still Watching Netflix*. Il est **explicitement classé live-action**, pas anime, afin de ne pas brouiller la vidéothèque.
- **Media Check** utilise aussi les huit nouvelles références et les teste en priorité lors du test de 30 images. Le précédent résultat **294/294** concerne uniquement la V4.8 : **il ne valide pas les nouvelles images V4.9**.
- Les quatre portraits encore sans référence sont l'épée Cerbère (identité/canon à clarifier), Morley, les utilisateurs collectifs des SMILE (pas de portrait unique) et Urban.
- Les anciens contrôles QA reconnaissent désormais les versions d'assets postérieures et le type de vidéo live-action distinct.
- Validation : `python scripts/check_v49.py` et [rapport d'audit V4.9](reports/media-audit-v49.md).

## V4.9.a — audit des sources, vidéos courtes uniquement

- Audit croisé du catalogue **166 fiches** avec les planches et ressources fournies, documenté dans [l'audit V4.9.a](reports/cross-source-audit-v49a.md) et dans [l'inventaire de 166 lignes](reports/catalogue-media-gap-v49a.json). Les correspondances spécifiques aux sources graphiques externes **restent à valider** : ne pas en déduire qu'une image de fruit de fan est canonique.
- Les **81 liens d'épisodes complets Crunchyroll** sont supprimés des données publiées et de l'interface. Les **37 associations YouTube** existantes (sur **25 fruits**) sont conservées, y compris les extraits hébergés sur YouTube par la chaîne Crunchyroll. Le site n'impose pas de compte Crunchyroll pour explorer les clips.
- Le filtre « Extrait court sélectionné » ne comptabilise plus les **44 fiches uniquement documentées par des épisodes complets**. Les boutons de recherche YouTube / Google Vidéos restent accessibles depuis **toutes** les fiches. Les résultats de recherche ne sont pas considérés comme clips intégrables tant qu'ils ne sont pas vérifiés et attribués à la bonne fiche.
- Sources visuelles : **162 portraits** et **140 illustrations de fruit ou pouvoir** avec URL référencée, **4 + 26** manquants. Le chargement dans le navigateur, les droits et le statut canon restent distincts et à contrôler.
- Régression automatisable : `python scripts/check_v49a.py`. Les vérifications de structure **ne remplacent pas** la lecture réelle des vidéos ni le contrôle des images en France.

## V4.9.b — scènes de pouvoirs YouTube

- **5 associations vidéo supplémentaires** pour quatre fruits : Bari Bari (deux clips), Horo Horo, Kage Kage et Doku Doku. Total **42 associations vidéo** sur **29 fiches**.
- Les deux vidéos Bartolomeo montrent une scène de barrière face à King Punch selon leurs métadonnées ; les trois autres sont des **montages d'attaques de l'anime**, pas des épisodes complets.
- Les chaînes sont **communautaires**, non les diffuseurs officiels. Titres et descriptions documentés, mais **aucune vérification de lecture iframe, région ou nécessité de compte YouTube** n'a encore été menée. Ces limites figurent dans les fiches.
- Pas de copie ni d'hébergement de séquences protégées : lecteur intégré sur clic et lien vers la vidéo source.
- Les **liens d'épisodes complets Crunchyroll restent absents**. [Rapport V4.9.b](reports/clip-review-v49b.md), contrôle : `python scripts/check_v49b.py`.

### V4.9.b2 — Kuma et CLIP CHECK

- **2 clips YouTube supplémentaires** du *Nikyu Nikyu no Mi* (Kuma / Ursus Shock) : `ofJ3DkkOo7Y` et `PvODesQjMgU`. Indexés d'après titres et métadonnées publiques, **lecture/iframe non testées**.
- Total actuel : **44 associations YouTube couvrant 30 fruits** (7 nouvelles associations depuis V4.9.a).
- **[CLIP CHECK](clip-check.html)** : revue humaine des extraits, test d'intégration sur clic, lien YouTube direct, signalement des problèmes, navigation privée, notes/timecodes, sauvegarde locale et export JSON. Le Dex propose le lien de vérification depuis la fiche du fruit.
- Les tests de structure `scripts/check_v49b.py` et `scripts/check_v49b2.py` sont exécutés en GitHub Actions. Aucun verdict d'accessibilité en France n'est inventé.

### V4.9.b2 — extension finale du lot

- **Caesar Clown / Gasu Gasu no Mi** : [montage « All Attacks and Abilities » par Rensuka Ren](https://www.youtube.com/watch?v=NKgXWO2RK-A), indexé à partir des métadonnées publiques. **Lecture effective, durée et autorisation d'intégration à contrôler.**
- **Bilan actuel : 45 associations YouTube pour 31 fiches** (+8 vidéos, +6 fruits depuis V4.9.a). Les autres fiches gardent leur recherche externe.
- Le contrôle utilisateur passe par **[CLIP CHECK](clip-check.html)** ; le verdict n'est jamais déduit de la simple existence de la miniature.

## V4.9.b3 — 50 clips / 36 fruits, audit et proposition en un clic

- **+5 montages d'attaques documentés via YouTube** : Foxy, Blueno, Monet, Doflamingo, Perospero. **50 associations sur 36 fiches**, 130 fiches sans clip sélectionné.
- Les métadonnées concordent avec les personnages / fruits, mais la lecture et l'intégration sans compte en France ne sont **pas** certifiées. Voir [audit V4.9.b3](reports/clip-review-v49b3.md).
- Un verdict CLIP CHECK enregistré sur ce navigateur est visible sur la fiche : un clip localement signalé indisponible/mauvais pouvoir ne peut plus démarrer dans l'iframe locale. Lien YouTube et revue disponibles. Ceci ne remplace pas une revue éditoriale globale.
- Import d'un audit JSON CLIP CHECK antérieur (validation du schéma, des couples fruit/ID, date et taille ≤1 Mo). Les observations personnelles ne sont ni partagées ni envoyées automatiquement.
- Depuis chaque fiche, bouton **« J'ai trouvé une vidéo de ce pouvoir »** : soumission locale avec normalisation de l'URL YouTube et export d'un dossier de candidats non vérifiés, sans modification du catalogue public.
- Gate `python scripts/check_v49b3.py` ajouté à la CI. **PR Draft** tant qu'aucune vérification de lecture réelle n'est effectuée.
