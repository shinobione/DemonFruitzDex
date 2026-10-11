# DemonFruitzDex — V4.9.a : audit croisé avant intégration

**Date :** 11 octobre 2026. **Statut :** audit documentaire + suppression des liens d'épisodes complets sur la branche de revue. Aucun nouveau fruit ou visuel publié à cette étape.

## Périmètre actuel et vérification

- Catalogue : **166** fiches distinctes dans `data/fruits.json`. Ce nombre comprend des copies artificielles, pouvoirs non nommés et cas particuliers ; ce n'est pas le nombre canon de fruits naturels.
- Illustrations liées (fruit **ou pouvoir**) : **140/166** après application des extensions chargées dans la page (`data/portrait-sources.js`, `data/power-art-v48.js`). Il reste **26** fiches sans référence.
- Portraits liés : **162/166** après application des extensions de V4.7 à V4.9 ; il reste **4** fiches sans portrait : **Épée Cerberus, Morley, groupe des SMILE, Urban**.
- Vidéothèque avant V4.9.a : **37** associations à des vidéos YouTube sur **25** fruits. Les **44** autres fruits historiquement signalés comme ayant une scène avaient uniquement un lien d'épisode complet, pas un clip sélectionné.
- **81** liens d'épisodes complets retirés de `data/clips.json` et de son export `data/clips.js`. Les clips courts publiés sur YouTube par Crunchyroll, Toei, ADN ou Netflix (adaptation live-action distincte) restent catalogués.
- **Aucune lecture réelle ni autorisation d'iframe vérifiée** sur les 37 associations. L'existence d'une URL YouTube ne prouve ni l'accès sans compte, ni l'autorisation d'intégration.

## Sources croisées : statut

| Source | Apport envisagé | Contrôle et prudence | Décision V4.9.a |
|---|---|---|---|
| Deux planches Paramecia / Zoan / Logia transmises par l'utilisateur | Référentiel graphique permettant une recherche par catégorie et silhouette ; candidats pour les 26 visuels manquants | Définition des fichiers transmis env. 1750 × 2048 px ; zoom et recadrage possibles, sans créer d'informations. Auteur, licence, détails de chaque fruit à contrôler ; ne pas présumer le caractère canon | **Recherche uniquement**, aucune image ajoutée |
| Threads `@trafalgar_sukuna_jana`, publication `DBgy7TTIBN5` | Source indiquée avec les planches | Réponse de la plateforme indisponible à la consultation automatisée ; auteur et source primaire à confirmer | **À vérifier** |
| Homebrewery `24DkobVl8IGZ` | Idées descriptives et analogies D&D des pouvoirs | Adaptation de jeu de rôle ; ne pas confondre adaptations, fruits originaux des fans et canon | **Référence secondaire, jamais preuve canonique** |
| Vidéo naviguant sur une galerie Imgur `a/devil-fruits-NPrno` | Captures visuelles de personnages, transformations et apparitions | Accès direct non vérifié ; droits des images et correspondance à chaque pouvoir à auditer | **Candidats à sourcer** |
| Vidéo naviguant sur un document Scribd `978922460` | Images de fruits grand format et explications en français | Aperçu d'un ouvrage ; droits d'auteur et éventuelles interprétations graphiques | **Consultation seule**, aucun recadrage hébergé |
| Références One Piece Wiki / galeries d'images déjà associées à V4.9 | 162 portraits / 140 visuels avec URL | Présence d'une URL ≠ affichage réel, provenance canon et réutilisation autorisée | **Source à auditer avec MEDIA CHECK** |
| Recherche directe YouTube sur chaque fiche | Retrouver des scènes courtes montrant précisément la capacité | Curatelle manuelle : lien `watch?v=`, fruit/porteur concordant, scène effective, catégorie anime/live-action, chaîne d'origine, intégration HTML autorisée, disponibilité locale | **Priorité d'enrichissement V4.9.b** |

## Avertissement sur les illustrations non canoniques

Les planches et encyclopédies de fans peuvent représenter des fruits dont l'apparence physique officielle est inconnue. Ne jamais remplacer un visuel manquant par une représentation inventée sans **badge FAN ART / INTERPRÉTATION** et provenance explicite. Un dessin de la transformation du porteur doit être catégorisé **POUVOIR**, pas **FRUIT PHYSIQUE**.

Une planche semblable intitulée « Complete Chart of all Known Devil Fruits (Revised) » a été publiée sur Reddit en mars 2025 avec une **déclaration de l'auteur sur ses libertés artistiques et ses noms provisoires** : <https://www.reddit.com/r/OnePiece/comments/1jkrt1t/>. Cette similitude ne suffit pas à établir que les deux fichiers transmis sont ce document ; la comparaison de l'original source est nécessaire.

## File de recherche prioritaire — portraits et visuels

**Portraits :** Épée Cerberus (qualification canon), Morley, SMILE (cas collectif non représentable par un personnage unique), Urban.

**Visuels de fruit/pouvoir :** Onyudo (Onimaru), Kirin (Killingham), Ratatoskr (Ragnir), cinq transformations associées aux Doyens, Cerbère, Lassoo, Morgans, Bonney, Morley, Tama, Vegapunk, Vasco Shot, Urouge, Laffitte, Blamenco, Sharinguru, Charlotte Opera, Biblo, les quatre gardiens d'Impel Down.

Chacun doit recevoir l'un des statuts **APPARENCE CANONIQUE**, **VISUEL DU POUVOIR**, **FAN ART CRÉDITÉ**, **NON VÉRIFIÉ / REFUSÉ** avant ajout. Aucun résultat fiable ne doit être fabriqué à partir d'un nom présumé de fichier wiki.

## Règles produit V4.9.a

1. **Aucun lien d'épisode complet Crunchyroll** exposé ni dans les données clients. Enlever les rubans « ÉPISODE » et les faux compteurs de scènes.
2. **Conserver les extraits courts YouTube**, y compris ceux publiés sur des chaînes Crunchyroll **sur YouTube** ; la plateforme d'hébergement reste YouTube.
3. Le filtre de scènes correspond désormais aux seules **fiches avec au moins un clip YouTube sélectionné**, pas aux pages d'épisodes.
4. Pour les autres fiches : recherche YouTube et Google Vidéos disponible, sans lecture ni vidéo inventée.
5. Avant intégration de nouvelles vidéos, auditer l'ID, le détenteur, le pouvoir effectivement montré, l'auteur, la durée, l'intégration et le territoire. Dans le doute, lien de recherche plutôt que clip trompeur.

## Suite

V4.9.b = lots de clips vidéo candidats vérifiés ; V4.9.c = enrichissement des illustrations, seulement après concordance source/canon et droits. L'audit documentaire ne valide pas une vidéo ou une image à lui seul.

## Premiers candidats YouTube identifiés — aucun ajout automatique

Ces liens montrent pourquoi une recherche manuelle dans YouTube est utile. Leur fiche doit être contrôlée avant intégration. Les pages YouTube sont trouvables publiquement, mais le test iframe, la disponibilité en France, le minutage et les droits de la chaîne n'ont pas été certifiés.

| Fruit | Clip / lien | Source | Stade |
|---|---|---|---|
| **Bari Bari no Mi** (Bartolomeo) | [Bartolomeo — First Appearance](https://www.youtube.com/watch?v=2VwupgivJmI) | OACBVideos, vidéo de fan ; la description évoque explicitement la barrière face au King's Punch | **CANDIDAT DIRECT**, lecture/iframe et autorisation à vérifier |
| **Bari Bari no Mi** (Bartolomeo) | [Bartolomeo — Bari Bari no Mi](https://www.youtube.com/watch?v=pXvhvzbH1-Q) | MarcoDaporta, vidéo de fan | **CANDIDAT DIRECT**, passage exact et lecture à vérifier |
| **Baku Baku no Mi** (Wapol) | [Wapol's Munch-Munch Fruit — discussion](https://www.youtube.com/watch?v=1osMD-1SwGE) | Tekking101, analyse/commentaire de 2020 | **NE PAS intégrer comme extrait de pouvoir** : description d'une discussion, pas une scène d'anime attestée |

**Règle :** Une recherche YouTube pointe sur des résultats dynamiques ; pour intégrer un clip, l'éditeur doit sélectionner et enregistrer l'ID YouTube précis dans `data/clips.json` avec statut, fruit, porteur, séquence montrée, provenance et date de revue. Le site ne peut pas deviner de manière fiable le premier résultat de recherche à ouvrir comme un clip vérifié.
