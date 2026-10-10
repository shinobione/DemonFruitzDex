# Source Discovery V4.7 — portraits, pouvoirs et vidéos hors abonnement

## Audit factuel

- 166 fiches, dont 69 possédant au moins une référence sélectionnée.
- 36 associations YouTube (les mêmes vidéos peuvent correspondre à plusieurs fruits).
- 121 portraits initialement référencés, 13 nouveaux fichiers identifiés : 134 références de portraits, 32 en attente.
- 133 illustrations principales initialement référencées, 3 nouvelles représentations de pouvoir : 136 références, 30 en attente.
- Les références sont externes. La bonne résolution des URL et l'affichage ne sont **pas garantis** par ce contrôle.
- Les 30 absences de visuel ne représentent pas nécessairement 30 images officielles existantes : plusieurs fruits physiques ne sont jamais représentés canoniquement.

## Sources de vidéos à privilégier

Les extraits diffusés sur YouTube peuvent souvent se regarder sans être abonné à Crunchyroll.

1. **ADN / Animation Digital Network** — Luffy Gear 5 : https://www.youtube.com/watch?v=aLG9XoxJE7g
2. **ADN** — Luffy à Elbaph : https://www.youtube.com/watch?v=SJtADPK0fKQ
3. **ADN** — Robin Demonio Fleur : https://www.youtube.com/watch?v=IRXco8fXxBE
4. **Toei Animation** — Robin Demonio Fleur : https://www.youtube.com/watch?v=dqAOqwOdIVE

D'autres éditeurs peuvent proposer des vidéos selon les régions : Crunchyroll sur **YouTube**, Toei Animation, Netflix et leurs chaînes officielles. Aucun abonnement Crunchyroll n'est nécessaire pour afficher une page de recherche YouTube.

**Recherche toujours disponible :** depuis toute fiche, deux liens ouvrent une recherche YouTube (tous les producteurs) et Google Vidéos (multi-plateformes). Les résultats de recherche **ne sont pas** des extraits vérifiés. Les épisodes Crunchyroll sont secondaires et facultatifs.

## Nouvelles images utilisateurs

Aramaki, Sakazuki, Lassoo, Bian, Bunbuku, Galdino, Inazuma, Belo Betty, Shinobu, Bluegrass, S-Snake, Blamenco, Biblo.

Références des fichiers dans [data/portrait-sources.js](../data/portrait-sources.js). Certaines viennent d'illustrations de jeux ou de périodes particulières : elles sont identifiées comme telles.

## Nouvelles illustrations de pouvoirs

- Numa Numa no Mi — `Numa Numa no Mi Infobox.png`
- Wapu Wapu no Mi — `Wapu Wapu no Mi.gif` (GIF animé)
- Inu Inu no Mi, modèle Loup — `Full-Beast Form of Jabra's fruit.png`

Ces trois fichiers sont des **représentations du pouvoir** et non des photographies du fruit physique.

## Droits, contrôle et prochain lot

- Aucun extrait d'anime ni portrait sous droits n'est redistribué comme fichier dans le dépôt.
- Liens wiki et miniatures YouTube restent externes ; provenance indiquée dans les fiches.
- La lecture en France, le géoblocage et l'intégration iframe restent à valider sur un vrai navigateur.
- Priorité suivante : vérifier les 32 portraits non référencés et les 30 visuels encore absents, puis curer des clips YouTube **spécifiques au pouvoir** pour les 97 fruits sans scène sélectionnée.
- Contrôle statique : `python scripts/check_v47.py`.

Sources de catégories :
- https://onepiece.fandom.com/wiki/Category:Character_Portraits
- https://onepiece.fandom.com/wiki/Category:Devil_Fruit_Infobox_Images
