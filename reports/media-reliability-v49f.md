# DemonFruitzDex V4.9.f — MEDIA RELIABILITY

**Branche :** `feature/v4.9f-media-reliability` · **PR #7 Draft** · **Publication : interdite sans autorisation explicite**.

## Périmètre effectivement audité

Le catalogue est reconstruit avec les mêmes fichiers et le même ordre que `index.html` ; aucune ancienne métrique n'est copiée pour gonfler les résultats.

| Références | Quantité |
|---|---:|
| Fruits | 166 |
| Portraits enregistrés | **164** |
| Illustrations enregistrées | **152** |
| URL tierces testées | **316** |
| Emplacements sans média | **16** : 2 portraits + 14 illustrations |
| Associations YouTube (inchangées) | **50** |

Les 16 emplacements sans image sont un manque éditorial, **pas** une URL cassée ; aucun visuel inventé n'a été introduit.

## Vérification inter-navigateurs sur les runners GitHub

Le workflow `.github/workflows/media-reliability-v49f.yml` lance trois navigateurs indépendants depuis **l'origine HTTP locale du Dex** et teste les mêmes 316 images avec un élément `Image`, sans referrer, avec repli borné uniquement si le lien direct échoue. Les rapports JSON donnent le moteur et sa version, chaque paire fruit/média, chaque tentative et le résultat précis.

| Moteur | Références testées | Directement décodées | Repli sollicité |
|---|---:|---:|---:|
| Chromium (Linux CI) | 316 | **316** | 0 |
| Firefox (Linux CI) | 316 | **316** | 0 |
| WebKit (Linux CI) | 316 | **316** | 0 |

Ces observations se rapportent aux **runners GitHub Actions** : elles **ne prouvent pas** que les mêmes URL passent sur Chrome/Windows depuis la France. Les précédentes sessions Windows ont signalé des échecs de lecture Wikia ; aucun accès automatisé à cet environnement n'a été effectué pendant cette PR. Aucun certificat CORS ni origine de blocage réseau n'est déduit de `Image.onload` : l'affichage HTML d'une image tierce ne requiert normalement pas de CORS.

## Corrections apportées

1. **`data/media-reliability-v49f.js`** centralise la construction sûre d'une redirection `Special:Redirect/file` à partir du nom de fichier déjà fourni par le Dex, le chargement asynchrone borné, les statuts détaillés et l'identification conservatrice de la **fausse miniature One Piece Wiki 300×171 px**, déjà vérifiée visuellement dans l'audit précédent. Pas d'URL fabriquée pour les enregistrements sans fichier.
2. **`app.js`** reconnaît désormais cette fausse miniature sur les **portraits comme sur les illustrations**, uniquement si l'URL vient du Wiki One Piece. Un JPG de 300×171 provenant d'un autre hébergeur n'est pas rejeté. L'image est retentée via la redirection connue ou supprimée proprement au profit du fallback stylisé. On n'expose pas une image générique du Wiki comme s'il s'agissait d'une illustration canonique.
3. **MEDIA CHECK V2** inspecte les **332 emplacements** (dont 16 volontairement vides), distingue image décodée directement, image obtenue via redirection, réponse générique du Wiki, timeout, échec navigateur et URL absente. Il permet de filtrer les cas problématiques, de tester seulement les 12 nouveautés V4.9.e, et d'exporter toutes les tentatives avec navigateur, horodatage et URLs. Il n'envoie pas ces observations à un serveur.
4. L'audit GitHub Actions valide aussi **la panne simulée d'un CDN externe** : les images ne doivent pas casser le catalogue et MEDIA CHECK V2 doit terminer son travail, conserver le résultat, le filtrage et l'export de ses 12 références ciblées.
5. Les anciens tests **V4.9.d, V4.9.e et Media Integrity** restent actifs ; les assertions qui imposaient le code JavaScript en ligne ou le vieux titre `V4.9.c4` ont été mises à jour pour accepter l'externalisation et les éditions plus récentes.

## Ce que les résultats permettent — et ne permettent pas — d'affirmer

- **Oui :** les 316 URL **ont décodé** dans les trois moteurs de CI sur Linux ; elles ne sont pas globalement indisponibles.
- **Oui :** les images manquantes sont **16 emplacements non référencés**, non 16 liens cassés.
- **Oui :** la détection du placeholder Wiki et les tentatives de fallback sont codées dans le Dex et dans l'outil de contrôle local.
- **Non :** impossible de garantir leur lecture sur la machine Windows du propriétaire ou sur Safari iOS physique à partir de WebKit Linux.
- **Non :** le chargement d'une image ne certifie ni le personnage représenté ni les droits d'usage. Les images restent chargées depuis leurs hébergeurs externes et ne sont **jamais** téléchargées/réhébergées dans le dépôt.
- **Non :** le correctif ne peut pas contourner à coup sûr un blocage réseau général du CDN ; dans ce cas, un fallback graphique lisible apparaît et un export de diagnostic utilisateur pourra préciser les cas à traiter.

## Validation réelle du propriétaire — Chrome Windows (11 octobre 2026)

Un export utilisateur de **MEDIA CHECK V4.9.d**, réalisé depuis `https://shinobione.github.io` dans **Chrome 154 sous Windows 10**, a été fourni après les validations CI. L'export contenait **332 résultats sur 332 emplacements** et ses résultats ont été agrégés localement sans réhéberger le JSON brut.

| Mesure | Résultat Chrome Windows |
|---|---:|
| Portraits chargés directement | **164/164** |
| Illustrations chargées directement | **152/152** |
| Images décodées avec dimensions non nulles | **316/316** |
| Images Wikia chargées directement | **304/304** |
| Autres hébergeurs chargés directement | **12/12** |
| Redirections `Special:Redirect` utilisées | **0** |
| Échecs / délais / fausses vignettes connues 300×171 | **0** |
| Emplacements sans URL (non-établis, pas cassés) | **16** : 2 portraits et 14 illustrations |

**Traçabilité :** SHA-256 du JSON fourni : `d3705897f3f436398a61059ef992df727f56ac56f93030849911326b69b446a9`. Date déclarée dans l'export : `2026-10-11T20:55:42.354Z`. Schéma : `demonfruitzdex.media-browser-review.v49d`. Aucune adresse privée ni contenu personnel n'est recopié dans le dépôt.

**Interprétation :** cette mesure confirme que toutes les URL référencées ont **décodé dans le navigateur réel du propriétaire à cet instant**, sans recours au fallback. Les anciens problèmes Wikia ne sont pas actuellement reproduits par cet essai ; leur cause historique (cache, temporaire ou autre) reste **inconnue**. L'audit V4.9.d ne vérifie pas à lui seul le rendu final de chaque carte ni un blocage intermittent ultérieur. Les protections V4.9.f restent utiles en cas de futures erreurs et pour diagnostiquer celles-ci.

Le JSON utilisateur étant émis par l'ancienne page **V4.9.d**, il ne teste pas l'interface **MEDIA CHECK V2 de cette PR** sur Windows ; cette vérification restera possible après publication.

---

## Pour reproduire l'audit dans les CI

```bash
node scripts/inventory_media_v49f.js
node scripts/check_v49f.js
python -m pip install playwright
python -m playwright install --with-deps chromium firefox webkit
python scripts/audit_media_multibrowser_v49f.py --engine chromium
python scripts/audit_media_multibrowser_v49f.py --engine firefox
python scripts/audit_media_multibrowser_v49f.py --engine webkit
python scripts/smoke_media_ui_v49f.py --engine chromium
```

GitHub Actions conserve **un artefact par moteur** avec l'inventaire et les 316 observations, ainsi que deux captures de fonctionnement et d'échec simulé dans `reports/screenshots/v49f/`.

## Étape de validation après la PR

Ouvrir **MEDIA CHECK V2** sur Windows/Chrome et, séparément, Safari iOS réel si disponible, déclencher « Auditer les 332 emplacements », filtrer les échecs et exporter le JSON. Il permettra de distinguer les vrais liens hors service des restrictions réseau sans mettre en danger la base canonique. Le Dex public reste inchangé tant que la PR #7 n'est pas approuvée.

**Statut :** PR Draft / pas de fusion / pas de publication.
