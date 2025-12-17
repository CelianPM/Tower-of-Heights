# Tower-of-Heights
Projet NSI 
-----------------------------------------------------------
# Description :
Un jour, une mystèrieuse tour est apparue au milieu de Nice. Depuis cette tour, de nombreux monstres apparaissent et attaquent de nombreux civils, causant de nombreuses pertes. Certains individus choisis par la tour ont obtenus le pouvoir de combatre ces monstres. Jeune aventurié, auras-tu le courage de grimper la tour? 
# Idée :
Jeu de plateforme où il faut grimper une tour tout en éliminant les monstres et en gagnant en puissance.

Utilisation d'un système de niveau :

<img width="180" height="281" alt="image" src="https://github.com/user-attachments/assets/0aee1386-a089-4619-a909-e7719ea86987" />
<img width="664" height="374" alt="image" src="https://github.com/user-attachments/assets/2da63a81-9bc4-437f-a4f5-a5a1f32608cb" />


# Controles :
fleches droite-gauche = déplacement du personnage

touche space = saut

touche D = attaque dague

touche F = attaque magique

touche C = menu des attribus

# Cahier des Charges


- jeu de plateforme
- un seul joueur dont le personnage évoluera au cours du jeu
- choix entre 4 personnages possibles au début du jeu
- les capacités sont la force (dégâts bruts), l'agilité (vitesse de déplacement et d'attaque), l'inteligence (dégats magique), et la vitalité (la vie quoi)
- le personnage à le choix entre un attaque physique (corps à corps) et magique (à distance) en accord avec les capacités du perssonnage
- le level up dépend du nombre de points d'expérience, et à chaque level up le joueur se voit attribué des points d'abilité
- les points d'expérience augmente grâce au nombre d'ennemis tués et leurs niveaux (si plus fort, alors plus de points)
- à un cetain nombre de oints d'expérience, le pesonnage level up
- à chaque level up, le personnage gagne des points d'abilité, qui sont utilisés à améliorer ses capacités
- le système de vie dépend de la vitalité du personnage
- les ennemis peuvent attaquer et se déplacer en fonction du joueur
- les ennemis auront un emplacement prédéfini
- pas de système de timer
- pas de système de niveaux, mais il y aura des checkpoints
- pas de système de score, et donc de high score
- pour le système de contrôles, voir "Controles"
- jeu 2D pixélisé style "Celeste" créer avec les bibliothèques random et pygame
- utilisation de pygame
- le personnage se déplace de droite à gauche mais le décor se déplace de haut en bas
- les attaques seront animé
- les enemies seront animé et leur mort aussi
- le jeu se terminera lorsque le personnage aura atteint le haut de la tour
