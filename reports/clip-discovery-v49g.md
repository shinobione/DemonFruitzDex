# V4.9.g — POWER IN ACTION 2.0 : CLIP FINDER

**PR #8** — `feature/v4.9g-power-in-action-curation`, empilée sur la PR #7 (`feature/v4.9f-media-reliability`). **Brouillon, non fusionnée, non publiée.**

## État exact du catalogue

| Mesure | Valeur |
|---|---:|
| Fruits | **166** |
| Associations YouTube sélectionnées | **50** |
| Fruits comportant au moins un extrait | **36** |
| Fruits sans extrait sélectionné | **130** |
| Nouveaux liens vidéo sans vérification ajoutés par cette PR | **0** |

La couverture correspond au fichier `data/clips.js`, interprété comme dans `app.js` (vidéo principale et tableau `moreVideos`). Les 50 associations sont **référencées** ; leur lecture effective peut varier selon pays, compte, géoblocage ou autorisation d'intégration. Les anciens verdicts « non testé » restent non testés.

## Travail réalisé

- `clip-finder.html` et `scripts/clip-finder-v49g.js` : interface ancienne archive/parchemin, affichage de la couverture, navigation dans les 166 fiches, filtres « sans extrait / avec extrait », priorité A/B/C et recherche du fruit, du porteur ou de son ID.
- Chaque ligne propose un lien de **recherche YouTube** avec la bonne paire fruit/utilisateur. **Une page de résultats YouTube n'est pas un extrait vérifié.** Aucun ID n'est automatiquement importé et aucun lien vers des épisodes entiers Crunchyroll n'est créé.
- Lien vers `clip-check.html?fruit=ID&suggest=1` : fiche présélectionnée et module existant de proposition manuelle, avec stockage local de candidatures et export pour revue humaine. CLIP FINDER voit le nombre de propositions stockées localement sur ce navigateur, sans les transmettre au serveur.
- Export JSON `demonfruitzdex.clip-discovery.v49g` de la sélection filtrée : ID, fruit, utilisateur, priorité, recherche suggérée, nombre de vidéos déjà référencées et nombre de propositions locales. Cet export **n'est pas un catalogue de vidéos approuvées**.
- Intégration dans le pied de page de `index.html` et libellés V4.9.g cohérents.

### Priorité A (recherche éditoriale, pas validation vidéo)

Premières pistes : **Mera Mera / Ace-Sabo, Bara Bara / Buggy, Zushi Zushi / Fujitora, Mero Mero / Hancock, Okuchi no Makami / Yamato, Susu Susu / Karasu, Numa Numa / Caribou, Baku Baku / Wapol, Daibutsu / Sengoku, Hobi Hobi / Sugar**, ainsi que Baby 5, Shiki, Capone Bege, Kalifa, Jozu, Bellamy et d'autres entrées explicitement marquées A dans le script. Les catégories B/C n'impliquent pas un jugement de puissance. Les fruits fictifs/non confirmés gardent une priorité prudente.

## Pourquoi aucun clip nouveau n'est automatiquement intégré

Les recherches publiques ne permettaient pas d'établir simultanément : **identité du diffuseur**, **scène montrant exactement le pouvoir**, **URL YouTube publique**, **format extrait plutôt qu'épisode entier**, et **lecture sans compte / embed possible**. Ajouter des IDs au hasard aurait dégradé la qualité du Dex. La méthode reste *evidence-first* : CLIP CHECK + propositions exportées et revue humaine avant ajout à `data/clips.json` / `data/clips.js`.

## Vérifications

- `node scripts/check_v49g.js` : 166 fruits, 50 associations, 36 couverts, 130 sans extrait ; intégrité des liens et absence d'épisode Crunchyroll.
- `python scripts/test_clip_finder_v49g.py` : Chromium réel (desktop 1440px, mobile 390px), 130 lignes sans extrait, 36 déjà couvertes, recherche ID de Mera Mera, filtres priorité, export de 130 éléments, navigation vers CLIP CHECK avec fruit pré-sélectionné, pas de débordement horizontal sur mobile.
- Artefact attendu : `DemonFruitzDex-V49g-clip-finder`, deux captures `reports/screenshots/v49g/clip-finder-desktop.jpg` et `clip-finder-mobile.jpg`.
- Les CI antérieures de fiabilité média, de l'illustration et d'intégrité du Dex doivent rester vertes ; une V4.9.g fusionnée ne doit pas effacer V4.9.f.

## Suite réelle de V4.9.g

1. Récupérer un premier lot de **liens YouTube exacts** via les recherches de CLIP FINDER, ou l'export de propositions.
2. Vérifier un par un les **10 meilleurs candidats** dans CLIP CHECK (diffuseur, pouvoir dans la scène, replay sans compte, embedding). Les restrictions sont conservées comme telles.
3. Ajouter seulement les extraits confirmés, avec `sourceEvidence`, (verificationStatus), et éventuellement des timecodes **constatés**, jamais supposés. Relancer la CI et mettre à jour la couverture.

**PR Draft : ne pas fusionner ni publier sans confirmation explicite.**

## V4.9.g2 — première recherche ciblée de vidéos officielles (11 octobre 2026)

Après revue des cinq cibles initiales **Mera Mera / Ace-Sabo, Bara Bara / Buggy, Zushi Zushi / Fujitora, Mero Mero / Hancock, Okuchi no Makami / Yamato**, trois **extraits publiés par le compte YouTube vérifié de Crunchyroll** ont été localisés et associés à une fiche par métadonnées éditeur. **Le contenu exact des vidéos et leur lecture intégrée n'ont pas été visionnés/confirmés dans un navigateur humain.** En conséquence, ils sont stockés dans `data/clip-candidates-v49g.js`, **séparément de `data/clips.js` / `data/clips.json`**, pour revue manuelle.

| Fruit | Vidéo de l'éditeur sur YouTube | Contexte recoupé | Statut |
|---|---|---|---|
| Mera Mera — Ace/Sabo | [Ace vs Blackbeard (Part 1 of 2)](https://www.youtube.com/watch?v=bAShh8lXaUI), Crunchyroll, ép. 325 | Affrontement feu / ténèbres, mais déterminer si l'extrait précis montre les flammes d'Ace | **CANDIDAT : lecture et pouvoir à valider** |
| Mero Mero — Boa Hancock | [Koby vs Blackbeard vs Hancock](https://www.youtube.com/watch?v=h3GtlifE8CQ), Crunchyroll, ép. 1087 | L'épisode représente la pétrification de nombreux adversaires par `Slave Arrow` ; [résumé détaillé](https://onepiece.fandom.com/wiki/Episode_1087). Contrôler que cette portion figure dans le clip. | **CANDIDAT : lecture et pouvoir à valider** |
| Okuchi no Makami — Yamato | [Yamato vs Kaido](https://www.youtube.com/watch?v=yJPxk-jO3Xc), Crunchyroll, ép. 1049 | L'[épisode officiel One Piece.com](https://one-piece.com/anime/o6367/index.html) identifie les attaques de Yamato, Kagamiyama et Himorogiri, sous forme de loup divin. Contrôler ce qui est visible dans le clip. | **CANDIDAT : lecture et pouvoir à valider** |

**Recherches tenues en attente :** aucun extrait YouTube d'un diffuseur officiel montrant clairement **Bara Bara / Buggy** ou **Zushi Zushi / Fujitora** n'a pu être identifié avec une preuve suffisante. Des scènes complètes en accès Crunchyroll et des vidéos de fans existent, mais ce ne sont pas des extraits publisher-validés répondant aux contraintes. De même, une vidéo alternative de Yamato `Z8OX4kFWjqI` (épisode 1038) a été **retenue hors sélection**, car l'utilisation du Zoan n'y est pas établie. Ne pas transformer une page d'épisode complet avec abonnement en lien vidéo du site.

### Comment les revoir dans le Dex (PR seulement)

Le `CLIP FINDER` affiche les trois fiches avec « candidat(s) officiel(s) » et un bouton **« Tester le candidat »**, qui ouvre `CLIP CHECK` sur la paire exacte fruit / ID YouTube. Le filtre `candidates` y isole les trois extraits. Un réviseur peut ouvrir l'iframe YouTube *sur clic*, confirmer le pouvoir précis et la lecture sans compte, enregistrer un verdict et exporter un rapport incluant `candidate:true`. Le verdict est stocké **uniquement dans le navigateur** ; même si le test est positif, la vidéo **n'entre pas automatiquement** dans le catalogue publié.

Les tests automatisés Chrome vérifient le routage vers la bonne vidéo, les filtres, le statut de candidature, l'export du verdict et **50 associations publiées distinctes de 3 candidates**. Ils **ne jouent pas le film** et ne prétendent pas avoir vérifié sa disponibilité en France.

### Seuil de promotion vers `data/clips.json` et `data/clips.js`

La promotion d'un candidat exigera : 
1. `embed-ok` ou `youtube-only` observé depuis le pays visé, avec précision d'accès sans compte et capture / note de durée ;
2. pouvoir du bon fruit visible dans l'extrait, avec **timecode constaté** (pas inventé) ;
3. vidéo courte de l'éditeur, pas d'épisode entier, pas de source piratée ;
4. attribution correcte, identification canonique du fruit, pas de mélange Haki/pouvoir sans justification ;
5. aucune vidéo ni image de tiers réhébergée dans le dépôt.

**Comptes du Dex à ce stade : toujours 166 fruits, 50 associations publiées, 36 fruits couverts, 130 fiches sans clip sélectionné ; 3 candidats distincts à vérifier. PR #8 Draft, PR #7 Draft, aucune fusion.**
