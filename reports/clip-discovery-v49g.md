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
