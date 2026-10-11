DemonFruitzDex — V4.9.b3 · PR Preview (11 octobre 2026)
=======================================================

Ceci est un paquet de revue provenant de la PR GitHub #2.
Il n'est pas la version publique de DemonFruitzDex.

DÉMARRAGE SUR WINDOWS
1. Décompressez TOUT le ZIP de l'artifact dans un dossier.
2. Ouvrez PowerShell DANS ce dossier.
3. Exécutez: py -m http.server 8000
   (ou: python -m http.server 8000)
4. Ouvrez http://localhost:8000/
5. Ouvrez http://localhost:8000/clip-check.html pour vérifier les 50
   associations YouTube (montages communautaires inclus).

CE QU'IL FAUT TESTER
- Dans une fiche de fruit, essayer « Lire l'extrait » puis « Ouvrir sur YouTube ».
- Depuis la fiche, cliquer « Tester / signaler cet extrait ».
- En navigation privée et sans compte YouTube, noter si le clip montre
  réellement le pouvoir du fruit, et si l'iframe fonctionne en France.
- Si l'iframe est bloquée, enregistrer « YouTube seulement ».
- Revenir sur la fiche dans le même navigateur : le signalement local doit
  suspendre la lecture de ce clip, sans masquer les autres clips ni le lien source.
- Essayer « J'ai trouvé une vidéo de ce pouvoir » et exporter la proposition.
- Exporter puis réimporter un audit CLIP CHECK ; les résultats plus récents
  dans ce navigateur ne doivent pas être écrasés.

IMPORTANT
Les résultats du navigateur sont personnels (localStorage) : aucun statut
de vidéo ne change dans GitHub sans revue explicite et nouveau commit.
Les titres et métadonnées ne prouvent ni l'absence de compte ni
l'autorisation d'intégration. Aucun épisode complet Crunchyroll n'est lié.

AUCUN NOUVEAU VISUEL OU EXTRAIT PROTÉGÉ N'EST RÉHÉBERGÉ DANS LE DÉPÔT.
