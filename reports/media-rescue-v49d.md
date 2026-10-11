# V4.9.d — MEDIA RESCUE · Revue des 166 fiches

**Date :** 11 octobre 2026. **PR :** #5 (`feature/v4.9d-media-rescue-audit`, Draft). **Base :** V4.9.c4 (`main`). **Décision :** aucune fusion ni publication sans validation.

## Méthode — distinguer 3 types de problèmes

1. Reconstruire les **166 fiches réellement affichées dans le navigateur**, en exécutant dans le bon ordre `fruits.js`, `portrait-sources.js`, `portraits-v48.js`, `portraits-v49.js`, `portraits-v49d.js` et `power-art-v48.js`. Cela évite de compter uniquement le fichier JSON brut, qui n'inclut pas les ajouts.
2. Charger chaque URL de portrait et chaque illustration de pouvoir dans **Chrome headless, runner GitHub Actions**, sans referrer, avec délai limité. Si un lien échoue, essayer la redirection par fichier de One Piece Wiki.
3. **Contrôler aussi les dimensions et le contenu visuel** : le CDN de One Piece Wiki renvoie une **fausse image valide de 300 × 171 px** (pictogramme gris générique) lorsque certains noms de fichiers n'existent pas. Elle émet `onload` et trompait les audits antérieurs. Un contact sheet des candidats a été examiné avant intégration.
4. Séparer les sources **absentes**, les **placeholders vérifiés** et les échecs dus éventuellement à des restrictions de réseau ou hotlink. Le runner GitHub ne prouve pas la disponibilité en France ni sur les navigateurs des visiteurs.

### État initial réellement constaté

| Statut | Avant corrections |
|---|---:|
| Fiches du catalogue | 166 |
| Portraits référencés | 162 |
| Illustrations fruits/pouvoirs référencées | 140 |
| Références image totales | 302 |
| Portraits qui affichent l'**image générique 300 × 171** | **26** |
| Portraits sans référence | **4** |
| Illustrations de fruit/pouvoir sans référence | **26** |
| Illustrations décodées sans ce placeholder connu dans Chrome CI | 140 |

**Attention :** le chiffre naïf « 302/302 chargés » était trompeur. Après vérification du contenu graphique du placeholder, le bon constat est **276 références chargées normalement et 26 faux positifs**, dans le contexte de ce runner, avant corrections.

## Corrections implémentées

**21 portraits correctement identifiés** via la page de fichier et les fichiers images du One Piece Wiki, décodés en Chrome et comparés visuellement dans un contact sheet :

- **2 portraits auparavant absents :** Morley (`oshi-oshi-no-mi`) et Urban (`tsutsu-tsutsu-no-mi`).
- **19 anciennes images génériques remplacées :**
  Kuzan, Marshall D. Teach (pour les deux fruits Yami Yami et Gura Gura),
  Sengoku, Catarina Devon, X Drake, Jabra, Wapol, Bellamy,
  Foxy, Blueno, Kalifa, Perona, Kin'emon, Charlotte Brûlée,
  Van Augur, Jesus Burgess, Avalo Pizarro et Vasco Shot.

Le fichier **`data/portraits-v49d.js`** contient les 21 associations vérifiées avec URL originale, nom du fichier, source et provenance. Il **n'écrase la fiche que si l'ancienne URL correspond exactement à la version auditée**, pour protéger les corrections futures. Aucune image n'est copiée ni hébergée dans le dépôt.

Les pages `index.html` et `media-check.html` chargent le sidecar après les précédents fichiers de portraits.

Dans `app.js`, les **faux portraits 300 × 171** du Wiki déclenchent le même repli que les erreurs réseau : tentative de la redirection Wiki, puis placeholder graphique du Dex, plutôt que d'afficher l'image générique comme si c'était un vrai portrait. La détection est limitée aux portraits, et n'assimile jamais automatiquement une capture vidéo 300 × 171 à une erreur.

L'outil **MEDIA CHECK** audite maintenant les **332 emplacements théoriques** (166 × portrait / art), affiche explicitement les références absentes, les défauts reconnus et les échecs de ce navigateur, et exporte un JSON de revue daté et contextualisé.

### Couverture prévue après correction

| Indicateur | V4.9.c4 | V4.9.d |
|---|---:|---:|
| Portraits référencés | 162 | **164** |
| Portraits sans référence | 4 | **2** |
| Anciennes images génériques non réparées | 26 | **7** |
| Portraits véritables vérifiés en CI, hors erreurs réseau futures | 136 | **157** |
| Illustrations référencées | 140 | **140** |
| Illustrations absentes | 26 | **26** |
| URL d'image dans le catalogue effectif | 302 | **304** |

Les **7 dossiers de portraits restant en priorité** : Marco, Miss Merry Christmas, Kanjuro, Kozuki Toki, Gunko, Imu et Momonosuke. Les noms standards essayés ont renvoyé l'image générique Wiki ; il faut localiser un autre fichier précis et revoir le personnage avant intégration.

Les **2 fiches sans portrait** restantes correspondent à l'épée Cerberus et aux consommateurs SMILE collectifs. Elles ne doivent pas recevoir artificiellement une image d'un personnage unique.

Les **26 illustrations absentes** ne sont pas toutes des erreurs : plusieurs fruits physiques n'ont pas d'apparence canon révélée. Prioriser les **scènes du pouvoir clairement identifiées** pour Morley, Bonney, Tama, Vegapunk, Urouge, les nouveaux fruits d'Egghead et autres dossiers documentés, **sans prétendre montrer le fruit physique**. Pas d'art de fan non sourcé ou de faux fruit inventé.

## Reproduction et preuves

- `node scripts/inventory_media_v49d.js` produit l'inventaire complet fruit par fruit : `reports/media-inventory-v49d.json`.
- `python scripts/audit_media_browser_v49d.py` teste **les 304 images** avec Chrome et produit les observations détaillées : `reports/media-browser-audit-v49d.json`.
- `python scripts/probe_media_candidates_v49d.py` produit la liste des candidats et une **planche contact** permettant de repérer les fausses images avant tout changement.
- `python scripts/check_v49d.py` garantit les comptes attendus, les 166 fiches, l'intégralité des références et la validité du rapport.
- Les fichiers JSON générés et les contacts sheets sont conservés comme **artifacts de la CI**, sans publier des fichiers d'images sous copyright dans le dépôt.
- La CI classique de DemonFruitzDex conserve les validations du catalogue, les clips et le thème parchemin V4.9.c4.

### Risques résiduels

1. Les CDN externes peuvent varier selon région/navigateur, blocage anti-hotlink, réseau ou délai ; un `onload` ou une réussite GitHub Actions ne certifient pas tous les visiteurs.
2. Le fait qu'une image montre le bon personnage ne suffit pas à accorder une licence de redistribution. Les images restent référencées à leur source tierce.
3. L'absence de représentation canon est conservée telle quelle. Aucun faux fruit physique ne doit être ajouté pour gonfler la couverture.
4. La lecture YouTube et la disponibilité des vidéos n'entrent pas dans cette mission.
5. La PR reste **Draft**. Aucune fusion/publication automatique.

**Prochaine étape éditoriale :** examen manuel du nouveau contact sheet et du rapport d'audit, recherche ciblée des sept portraits restants, puis vérification sur Chrome en France et Safari iOS avant promotion.

---

## V4.9.d2 — deuxième vague : les sept portraits restants

La section précédente documente l'état **avant** cette deuxième vague (les 21 premiers remplacements). Après examen du contact sheet V4.9.d2 en Chrome, les **7 derniers placeholders Wiki ont trouvé un autre fichier réel**. Les images ont été vérifiées visuellement, puis intégrées au même sidecar avec garde `previous_portrait`.

| Fruit / porteur | Nouveau fichier | Choix éditorial |
|---|---|---|
| Phoenix / Marco | `Marco PW Portrait.png` | Portrait officiel de jeu One Piece Pirate Warriors ; clairement distingué d'une image anime |
| Mogu Mogu / Miss Merry Christmas | `Drophy Portrait.png` | Nom véritable du personnage ; portrait anime |
| Fude Fude / Kanjuro | `Kurozumi Kanjuro Portrait.png` | Nom complet du personnage ; portrait anime |
| Toki Toki / Kozuki Toki | `Kouzuki Toki Portrait.png` | Romanisation `Kouzuki` utilisée dans les fichiers Wiki |
| Aro Aro / Gunko | `Manmayer Gunko Portrait.png` | Nom complet ; portrait anime |
| Pouvoir d'Imu | `Imu Anime Concept Art.png` | **Silhouette de l'anime** pour limiter les révélations manga ; fichier explicitement typé silhouette |
| Dragon artificiel / Momonosuke | `Kouzuki Momonosuke Anime Infobox.png` | **Apparence adulte** correspondant à l'histoire actuelle, plutôt que portrait enfant |

Ces fichiers ont été décodés dans le navigateur Chrome CI, et le contenu de la planche contact a été revu avant sélection. Aucun fichier Wiki n'est téléchargé ou réhébergé : seuls les liens et provenances sont ajoutés.

### Nouvel objectif de couverture

- **28** corrections de portraits au total depuis V4.9.c4 : 26 URL Wiki placeholders remplacées, **2 portraits auparavant absents** ajoutés.
- **164 portraits renseignés sur 166 fiches** (les 2 absences restantes sont un objet animé et un groupe SMILE collectif).
- **0 placeholder connu** parmi les 164 portraits, sous réserve de confirmation du nouveau test intégral Chrome GitHub Actions.
- **140 illustrations de pouvoir / fruit enregistrées** ; les **26 manques** restent des tâches de recherche et ne sont PAS comblés avec des dessins inventés.
- Les **50 associations vidéo** ne changent pas.

Le nouveau `scripts/check_actual_media_v49d2.py` charge **la vraie page `index.html`**, toutes ses sidecars et les 7 portraits depuis Chrome, contrôle `164/166` et refuse les miniatures Wiki 300×171, puis génère la capture `reports/media-actual-page-v49d2.jpg`.

### Prochaine vague — 26 illustrations manquantes

Le script `scripts/triage_missing_visuals_v49d2.py` produit un fichier structuré **`reports/media-illustration-backlog-v49d2.json`** classant les 26 dossiers en priorités A/B/C avec statut `not-researched-or-not-verified`. Il sépare :

- les capacités nommées pour lesquelles une scène d'action vérifiable est une priorité (Bonney, Morley, Tama, Vegapunk, etc.) ;
- les formes Zoan / mythiques à illustrer **comme transformations**, non comme apparence du fruit physique ;
- les fruits sans nom et formes dont la documentation canon est insuffisante : ne pas inventer de fruit ni attribuer une illustration trompeuse.

Le texte de la fiche sans image a été clarifié : **« illustration absente » n'implique pas « apparence du fruit canon inconnue »**.

### Limites du contrôle

- Les succès proviennent de Chrome dans GitHub Actions et ne certifient pas l'accès depuis chaque pays / navigateur.
- Une image décodée, même visuellement conforme, ne signifie pas que la réutilisation ou le réhébergement sont autorisés.
- Le fichier de portrait Marco vient d'un jeu ; Imu est représenté en silhouette ; ces distinctions doivent rester documentées.
- Toujours **PR Draft, pas de fusion ni publication** sans validation explicite.
