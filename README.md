# Algorithme du jeu Killer
Algorithme générant une boucle pour le jeu du Killer

## Utilisation
Vous devez remplire le fichier `config.csv` avec les classes et nom de chaque participants.
Le fichier se présente sous forme de tableau à deux colonnes `Classe` et `Joueur`. 
Chaque retour à la ligne represente une ligne du tableau et on sépare la classe et le nom du joueur sur une même ligne par une virgule.

Vous pouvez ensuite lancer l'algorithme, lequel devrait créer un fichier `boucle.csv` où se trouvera la boucle (sous forme de tableau encore une fois).

## Tests
Le fichier `util.py` permet de générer un fichier `config.csv` avec des noms aléatoires. Il y a besoin de la librarie suivante:
```
pip install names_generator
```
