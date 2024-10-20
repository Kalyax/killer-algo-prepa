"""
Dernière mise à jour: 2024
Si problème, contactez moi sur Github: @Kalyax
"""

from random import choices

#CRITERE D'ESPACEMENT ENTRE ELEVES D'UNE MEME CLASSE DANS LA BOUCLE
CONST_TAILLE_MIN = 4

def choisir_classes(classes_possibles, taille_classes):
    """
    Entrée:
    - classes_possibles: list: liste des indices des classes possibles de choisir (elles doivent respecter le critère CONST_TAILLE_MIN)
    - taille_classes: list: nombre d'élèves de toutes les classes (celles qui ne sont pas dans classes_possibles y sont quand même)
    Sortie:
    - list: liste aléatoire, chaque classe étant choisie de manière proportionelle à son nombre d'élèves restant
    """
    
    liste_choix = []

    #tant qu'il reste des classes possibles à choisir on continue
    while len(classes_possibles) != 0:
        #on attribue un poid à chaque classe, proportionel à leur nombre d'élement restant, puis on choisit aléatoirement une classe en fonction des poids
        classes_poids = [taille_classes[i] / sum(taille_classes) for i in classes_possibles]
        classe_choisie = choices(classes_possibles, weights=classes_poids)[0]

        #on ajoute cette classe choisie à notre liste et on s'apprête à réiterer le processus en enlvant cette classe des classes possible de choisir
        liste_choix.append(classe_choisie)
        classes_possibles.remove(classe_choisie)

    return liste_choix
        

def creer_boucle(boucle, index_classes, taille_classes):
    """
    Entrée:
    - boucle: list: boucle des classes construite par backtracking, à initialiser en liste vide
    - index_classes: list: liste des numéros de chaque classe
    - taille_classes: list: liste des nombres d'élèves par classe restante, ordonnée selon leur indice dans index_classes

    Sortie:
    - list: boucle finale

    La boucle finale NE respecte PAS FORCEMENT le critère CONST_TAILLE_MIN
    Si le code ne semble pas terminer au bout de plusieurs minutes, le relancer.
    """

    #on fait la liste des classes non vide, celles pour lesquelles on peut encore ajouter des élèves à la boucle
    classes_non_vide = [i for i in index_classes if taille_classes[i] != 0]

    #cas de base: si toutes les classes sont vide, on a fini, on renvoie la boucle
    #ELLE NE RESPECTE PAS FORCEMENT LE CRITERE CONST_TAILLE_MIN, IL FAUT LA TESTER !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    if len(classes_non_vide) == 0:
        return True, boucle

    #on liste les classes verifiant le crtière CONST_TAILLE_MIN si on les ajoutait à la fin de la liste de la boucle
    classes_possibles = [i for i in classes_non_vide if test_segement(boucle, i)]

    #on choisie les classes de manière proportionelle mais aléatoire
    classe_choisie = choisir_classes(classes_possibles, taille_classes)
    
    #on itère sur les classes choisies, pour chacune on essaie récursivement de completer la boucle (backtracking)
    for classe in classe_choisie:
        boucle.append(classe)
        taille_classes[classe] -= 1

        (trouve, new_boucle) = creer_boucle(boucle, index_classes, taille_classes)

        #si on a pu completer la boucle à l'appel de creer_boucle avec cette classe, on remonte la pile des appels
        if trouve:
            return True, new_boucle

        #sinon cette classe ne convient pas et mène à une impasse, on essaie avec la suivante
        boucle.pop(-1)
        taille_classes[classe] += 1
        
    #aucune des classes ne convient, on remonte dans la pile des appels
    return False, boucle
    

#FAUSSE A REFAIRE
def test_segement(boucle, classe_id):
    n = len(boucle)
    for i in range(1, CONST_TAILLE_MIN):
        if i > n:
            continue
        if boucle[-i] == classe_id:
            return False
    return True


def test_boucle(boucle, taille_classes):
    """
    Entrée:
    - boucle: list: boucle à tester
    - taille_classes: list: liste des nombres d'élèves par classe restante
    Sortie:
    - bool: la boucle est-elle valide?

    On teste si toutes les classes sont bien vide et si la boucle respecte le critère CONST_TAILLE_MIN
    """
    #On teste si toutes les classes sont vide
    for classe in taille_classes:
        if classe != 0:
            print("ERREUR: Toutes les classes ne sont pas vide")
            return False

    #On teste si la boucle vérifie le critère CONST_TAILLE_MIN
    for i in range(len(boucle)):
        for k in range(1,CONST_TAILLE_MIN) :
            if boucle[i] == boucle[i-k]:
                print("ERREUR: La boucle ne vérifie pas le critère CONST_TAILLE_MIN")
                return False
    return True

def read_config_csv():
    """
    Sortie:
    - index_classes: list: liste des indice de chaque classe (exemple s'il y a 3 classes: [0, 1, 2])
    - nom_classes: list: liste des noms de chaque classe, à l'indice i, il y a le nom de la classe d'indice i (indice au sens de index_classes) 
                         (exemple s'il y a 3 classes: ["HK", "MP2I", "PC"])
    - taille_classes: list: liste du nombre d'élèves par classe, le nombre d'élèves dans la classe i est à l'indice i: (exemple s'il y a 3 classes: [48, 24, 32])
    - nom_joueur_classes: list of lists: liste de listes des noms de chaque élèves par classes (idem pour les indices)

    Lis le fichier config.csv où se trouvent les noms de tous les participants ainsi que leur classe et renvoie les données dans 4 variables
    """
    index_classes = []
    nom_classes = []
    taille_classes = []
    nom_joueur_classes = []

    f = open("config.csv", "r")
    joueurs = f.read().split("\n")

    for i in range(1,len(joueurs)-1):
        classe, nom = joueurs[i].split(",")
        #si la classe existe déjà dans nom_classes
        if classe in nom_classes:
            i_classe = nom_classes.index(classe)
            taille_classes[i_classe] += 1
            nom_joueur_classes[i_classe].append(nom)
        #sinon il faut la créer, on l'initialise avec l'élève sur lequel on itère
        else:
            index_classes.append(len(index_classes))
            nom_classes.append(classe)
            taille_classes.append(1)
            nom_joueur_classes.append([nom])
    
    return index_classes, nom_classes, taille_classes, nom_joueur_classes


def build_boucle_csv(boucle, index_classes, nom_classes, nom_joueur_classes):
    """
    Entrée:
    - Idem aux autres fonctions...

    Construit le fichier boucle.csv, qui correspond à la boucle et où chaque élève a une cible assignée.
    """

    #format du tableau csv
    texte = "Joueur,Cible\n"

    compteur_classes = [0 for i in index_classes]

    #on itère sur chaque element de la boucle, on rajoute une ligne au fichier à chaque fois de la forme "joueur,cible"
    for i in range(len(boucle)-1):
        id_classe_joueur = boucle[i]
        id_classe_cible = boucle[i+1]
        joueur = nom_joueur_classes[id_classe_joueur][compteur_classes[id_classe_joueur]]
        cible = nom_joueur_classes[id_classe_cible][compteur_classes[id_classe_cible]]
        compteur_classes[id_classe_joueur] += 1
        texte += joueur + "," + cible + "\n"

    #on complète la boucle, on donne au dernier élève le premier élève comme cible
    id_classe_joueur = boucle[len(boucle)-1]
    id_classe_cible = boucle[0]
    joueur = nom_joueur_classes[id_classe_joueur][compteur_classes[id_classe_joueur]]
    cible = nom_joueur_classes[id_classe_cible][0]
    texte += joueur + "," + cible
    
    f = open("boucle.csv", "w")
    f.write(texte)
    f.close()


#on lit le fichier config.csv et on recupère les variables
index_classes, nom_classes, taille_classes, nom_joueur_classes = read_config_csv ()

#on crée la boucle
trouve, boucle = creer_boucle([], index_classes, taille_classes)

#si trouve est faux, il y a eu une erreur
if not trouve:
    print("ERREUR: La boucle n'a pas pu être formée")
else:
    #on teste la validité de la boucle, se réferer à la fonction test_boucle pour voir ce qu'elle teste
    test_boucle(boucle, taille_classes)

    #on construit le fichier boucle.csv
    build_boucle_csv(boucle, index_classes, nom_classes, nom_joueur_classes)
    print("Boucle construite dans boucle.csv")