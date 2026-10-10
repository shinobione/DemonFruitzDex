# DemonFruitzDex — SHINO-DEX Ultimate 🍎

Encyclopédie interactive et illustrée des Fruits du Démon de **One Piece**, en français.

## Version actuelle

- **166 fiches** de l'édition actuelle (fruits naturels, quelques pouvoirs sans nom et technologies artificielles). Ce nombre **n'est pas** le nombre officiel de fruits distincts : les catégories se recouvrent et des copies artificielles sont incluses.
- **133 références visuelles externes** vers des fichiers de la galerie du One Piece Wiki ; elles ne sont ni téléchargées ni redistribuées dans ce dépôt.
- **39 fiches** répertorient un visuel du fruit physique (selon les informations de cette édition) ; les autres visuels éventuels montrent **le pouvoir**, pas le fruit.
- Recherche, filtres type/tier/éveil/illustration, tri, cartes et fiches détaillées.
- Mode sombre et responsive. Aucun build ni dépendance nécessaire.

## Démarrage

Ouvrir `index.html` dans un navigateur récent.

## Publication GitHub Pages

Aller dans **Settings → Pages → Build and deployment → Deploy from a branch**. Sélectionner **main** / **/(root)** puis enregistrer.

La page sera généralement accessible à :
https://shinobione.github.io/DemonFruitzDex/

> L'URL publique ne sera fonctionnelle que lorsque GitHub Pages sera activé et aura fini de publier.

## Images et sources

Illustrations issues de liens distants vers :
https://onepiece.fandom.com/wiki/Category:Devil_Fruit_Infobox_Images

Les illustrations et personnages de One Piece restent la propriété de leurs titulaires respectifs. Le projet n'est ni officiel ni affilié à Shueisha, Eiichiro Oda ou Toei Animation. Les images externes peuvent disparaître, être bloquées par les règles de hotlinking, ou ne pas avoir le même statut de licence que les textes collaboratifs du wiki. Consulte les pages fichiers originales pour les crédits et droits.

Les cartes affichent un **visuel alternatif non officiel** si la ressource distante ne charge pas. Un badge distingue :
- `FRUIT PHYSIQUE` : design du fruit identifié dans cette édition ;
- `POUVOIR ILLUSTRÉ` : image associée à l'utilisation / transformation ;
- `VISUEL NON DOCUMENTÉ` : aucun fichier retenu.

## Qualité et limites

L'ensemble des 166 fiches a fait l'objet d'un contrôle automatique basique de l'interface (JavaScript, rendu, recherche et modale). **Les 133 liens d'image n'ont pas encore pu être testés individuellement sur le réseau public** et certaines entrées très récentes du manga devront être revérifiées avant de déclarer le catalogue exhaustif ou 100 % canonique. Les tiers S+ à C sont une **appréciation éditoriale non officielle**.

## Roadmap proposée

1. Réviser chaque fiche récente (canon, nom et orthographe) avec référence au chapitre/SBS.
2. Auditer automatiquement les URLs d'images et substituer les liens rompus par des sources stables et autorisées.
3. Séparer le contenu dans des fichiers JSON versionnés pour faciliter les mises à jour.
4. Ajouter personnages, plusieurs images par fruit, chapitre de première apparition et frise chronologique.
5. Ajouter la comparaison de deux fruits, des favoris et une interface de contribution.

