# DemonFruitzDex — audit médias V4.9

**Statut :** édition publiée dans `main` le 11 octobre 2026. Les images ajoutées aujourd'hui n'ont **pas encore passé un Media Check utilisateur**. Ne pas les compter comme « chargées » tant qu'un rapport réel ne le confirme pas.

## Inventaire

| Métrique | V4.8 | V4.9 | Évolution |
|---|---:|---:|---:|
| Fiches | 166 | 166 | 0 |
| Portraits avec URL | 154 | 162 | +8 |
| Portraits sans URL | 12 | 4 | -8 |
| Illustrations de fruits ou pouvoirs avec URL | 140 | 140 | 0 |
| Fruits sans illustration propre | 26 | 26 | 0 |
| Cartes sans illustration propre montrant un portrait utilisateur | 0 | 24 | +24 |
| Associations YouTube | 36 | 37 | +1 |
| Vidéos YouTube distinctes | 31 | 32 | +1 |

**Attention :** les cartes affichant l'utilisateur ne prétendent PAS montrer l'apparence du fruit. Il s'agit d'un repli visuel clairement étiqueté. Pour le Green Blood, les SMILE, les fruits non révélés et les capacités non représentées, aucune apparence canonique ne doit être inventée.

## Huit portraits ajoutés

| Personnage | Fruit | Nom de fichier source | Confiance documentaire |
|---|---|---|---|
| Pierre | Uma Uma no Mi | `Pierre Portrait.png` | Mention d'une galerie du personnage |
| Smiley | Sara Sara no Mi (Axolotl) | `Smiley Portrait.png` | Index galerie images Punk Hazard |
| Very Good | Beri Beri no Mi | `Very Good Portrait.png` | Mention dans sa page encyclopédique |
| Giolla | Ato Ato no Mi | `Giolla Portrait.png` | Fichier indexé dans la saison 17 |
| Machvise | Ton Ton no Mi | `Machvise Portrait.png` | Intitulé de galerie, orthographe à contrôler |
| Buffalo | Guru Guru no Mi | `Buffalo Portrait.png` | Fichier référencé dans le catalogue canon |
| Charlotte Newshi | Gocha Gocha no Mi | `Charlotte Newshi Portrait.png` | Fichier existant mais signalé de faible qualité |
| Kelly Funk | Jake Jake no Mi | `Kelly Funk Portrait.png` | Fichier indexé dans la saison 17 |

Chaque référence est dans [data/portraits-v49.js](../data/portraits-v49.js), avec une URL de source `portrait_evidence`. Le chemin CDN suit la convention d'adressage MediaWiki, mais **doit encore être testé depuis un vrai navigateur**.

## Vidéo ajoutée

Smoker / Moku Moku no Mi : [Luffy vs. Captain Smoker](https://www.youtube.com/watch?v=4frfkxIubLc), publication de **Still Watching Netflix**. Cette scène est issue du **live-action**, pas de l'animé ; elle est marquée `contentKind: live-action` dans la playlist et étiquetée à l'écran.

## Quatre portraits encore absents

- Épée Cerbère : les références et la nature canonique de cette entrée doivent être examinées avant de sélectionner une image.
- Morley : rechercher un portrait de référence à l'orthographe exacte.
- SMILE (collectif) : aucun porteur unique, ne pas inventer de portrait individuel.
- Urban : rechercher et contrôler le fichier de portrait du vice-amiral, sans le confondre avec Urbain.

## Validation à faire

1. Lancer [Media Check](../media-check.html) sur **30 images**, qui place les huit nouvelles références en tête.
2. Exporter le JSON et vérifier les huit URL nouvelles.
3. Ne conserver que les sources affichées réellement ou utiliser leur fichier alternatif après vérification.
4. Auditer ensuite la **pertinence visuelle** des portraits ; un fichier qui charge n'est pas forcément le bon personnage.
5. Chercher des clips **de l'animé** pour les 97 fruits n'ayant aucune scène sélectionnée. Le clip Netflix est seulement un bonus explicitement identifié.

Les 294 images de la V4.8 ont été vérifiées précédemment par Media Check, mais cela ne vaut **pas** pour les huit nouvelles.
