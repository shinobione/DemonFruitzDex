# V4.9.b — enrichissement des extraits YouTube de pouvoirs

**Date :** 11 octobre 2026. **Branche :** `feature/v4.9b-youtube-power-clips`, empilée sur `audit/v4.9a-cross-source-no-full-episodes`. **État :** métadonnées indexées et mises dans le lecteur YouTube, **lecture réelle et iframe non certifiées**.

## Bilan

- V4.9.a : **37 associations vidéo / 25 fruits**.
- V4.9.b : **42 associations vidéo / 29 fruits** ; +5 références vidéo, +4 fruits dotés d'au moins un clip.
- Toujours **166 fiches**, **162** portraits référencés et **140** représentations de fruit/pouvoir référencées.
- **0 lien vers un épisode complet Crunchyroll** dans les données clients.
- Le bouton direct « Ouvrir sur YouTube » demeure dans la fiche, notamment si le lecteur embarqué est refusé.

## Candidats intégrés à la playlist

| Fruit | Utilisateur | YouTube | Chaîne | Ce qui est documenté | Statut |
|---|---|---|---|---|---|
| Bari Bari | Bartolomeo | [AdM7PV5kako](https://www.youtube.com/watch?v=AdM7PV5kako) | Portgas D. Ace | « King Punch and Power of Barrier Barrier Fruit », 31 mars 2014 ; défense puis victoire de Bartolomeo dans la description | Métadonnées concordantes ; diffusion non testée |
| Bari Bari | Bartolomeo | [Zupy-QIf-8U](https://www.youtube.com/watch?v=Zupy-QIf-8U) | BULLBOOJI | « Barrier vs King Punch - Barto vs Elizabelo », 31 janv. 2026 | Métadonnées concordantes ; diffusion non testée |
| Horo Horo | Perona | [p5KF8XZlqEk](https://www.youtube.com/watch?v=p5KF8XZlqEk) | Rensuka Ren | « Perona / Horo Horo no Mi / All Attacks and Abilities », 8 oct. 2022 ; fantômes décrits dans la vidéo | **Montage** ; lecture non testée |
| Kage Kage | Gecko Moria | [fSgU4NEqa4s](https://www.youtube.com/watch?v=fSgU4NEqa4s) | Rensuka Ren | « Gecko Moria / Kage Kage no Mi / All Attacks and Abilities », 26 mai 2024 ; contrôle des ombres décrit | **Montage** ; lecture non testée |
| Doku Doku | Magellan | [592XWC7Abkc](https://www.youtube.com/watch?v=592XWC7Abkc) | Koi 鯉 | « Magellan / All Attacks », 9 mai 2025 ; hydre et poisons décrits | **Montage** ; lecture non testée |

### Contrôles effectués

1. Les **5 identifiants** ont une structure YouTube de 11 caractères et pointent vers des fiches de fruits existantes.
2. Métadonnées de chaque vidéo (titre / chaîne / descriptif lorsque disponible) **visibles sur l'index public YouTube** ; les pouvoirs invoqués correspondent aux fruits, via les pages One Piece Wiki correspondantes.
3. Deux liens distincts de la même scène de Bartolomeo (épisode 638), affichés dans le sélecteur de playlist sans duplication d'ID.
4. Source = `youtube.com/watch?v=...` ; **pas d'hébergement/republication des vidéos**.
5. Provenance de chaîne **communautaire**, non officielle. La mention « METADONNEES RECENSÉES / LECTURE INTÉGRATION NON TESTÉES » figure sur chaque sélection.
6. Les anciennes vidéos restent inchangées.

### Ce qui reste à vérifier AVANT validation finale

- **Lire les 5 vidéos** sur le navigateur du visiteur, en France, hors session YouTube, puis tester le lecteur YouTube `youtube-nocookie.com/embed/` pour chaque ID. Une URL trouvable ne garantit pas l'autorisation d'intégration ou l'absence de compte.
- Mesurer **durée réelle**, minutage d'entrée en action du pouvoir et présence d'éventuels commentaires / inserts.
- Déterminer si les **montages** respectent la cible éditoriale « extraits de l'anime » malgré leur longueur éventuelle ; le titre ne certifie pas le montage effectif.
- Vérifier les conditions de réutilisation des vidéos tierces. L'embed YouTube et un lien vers l'auteur ne confèrent **pas de licence de téléchargement**.
- Ne pas exposer d'éléments vidéo marqués `verified playback` ou `embed verified` sans test en navigateur.

### Sélection écartée

- [Wapol — Munch-Munch Fruit discussion](https://www.youtube.com/watch?v=1osMD-1SwGE) : vidéo explicative (pas une scène d'anime), exclue de la playlist des scènes.
- [Doflamingo — Birdcage original song](https://www.youtube.com/watch?v=Yv-yRdiwz1o) : chanson originale, non pertinente comme extrait de pouvoir.
- [Moria — Kage Kage Explained](https://www.youtube.com/watch?v=rkUziqU-b5w) : analyse commentée plutôt que séquence d'action.
- [Buggy vs Mihawk fan-animation](https://www.youtube.com/watch?v=7P7kxOZXm7g) : animation de fans, non conforme à la séquence de l'anime demandée.

### Suite proposée

V4.9.b.2 : vérifier en conditions réelles ce lot de 5 vidéos, remplacer les vidéos géobloquées/non intégrables, puis rechercher les pouvoirs manquants chez les 137 fiches sans clip sélectionné. Les archives de l'anime ne doivent pas être hébergées dans le dépôt.


## Lot complémentaire V4.9.b2 — Kuma

| Fruit | ID | Chaîne | Scène annoncée | Statut |
|---|---|---|---|---|
| Nikyu Nikyu no Mi | [ofJ3DkkOo7Y](https://www.youtube.com/watch?v=ofJ3DkkOo7Y) | DapperDarius | « Kuma Creates His Ursus Shock » | Métadonnées indexées, lecture non testée |
| Nikyu Nikyu no Mi | [PvODesQjMgU](https://www.youtube.com/watch?v=PvODesQjMgU) | Yonko Level | « Kuma Ursus Shock vs Strawhat Pirates at Thriller Bark » | Métadonnées indexées, lecture non testée |

**Nouveau total : 44 associations YouTube sur 30 fruits** ; 136 fiches sans clip (166 - 30), en attendant les validations. La CI vérifie la concordance JSON/JS et les références, pas la possibilité de lecture ou l'intégration.

### CLIP CHECK

Le dépôt propose maintenant `clip-check.html`. Les vidéos sont chargées dans un iframe YouTube sur demande. Le réviseur ouvre aussi la page YouTube directe, idéalement en fenêtre privée et déconnecté. Il choisit un verdict explicite (iframe OK / YouTube seulement / connexion requise / indisponible / mauvais pouvoir / à revoir), ajoute éventuellement le minutage et exporte un rapport JSON. Les résultats sont stockés localement dans le navigateur et **ne changent pas automatiquement le statut public des vidéos**. L'iframe chargée ne signifie jamais « lecture certifiée ».

**Contrôles hors ligne :** `python scripts/check_v49b2.py`, plus tests précédents. **Validation d'usage réelle : à effectuer sur navigateur en France.**
