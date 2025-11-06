def read_boucle_csv():
    """
    Lis le fichier config.txt et renvoie une liste des classes ainsi qu'une liste
    de liste des couples (Joueur,Cible) pour chaque classe.
    Il faut noter que les indices des classes dans la liste nom_classes
    correspondent à la d'indice de la même classe dans couples_classes.

    Sortie:
    - nom_classes : liste de classe
    - couples_classes : liste de liste où chaque liste correspond aux couples (Joueur,Cible) de chaque classe
    """
    f = open("boucle.txt", "r")
    cartes = f.read().split("\n")

    nom_classes = []
    couples_classes = []

    for i in range(1,len(cartes)-1):
        j1, j2 = cartes[i].split(",")
        nom1, classe1 = j1.split("|")
        nom2, _ = j2.split("|")

        if classe1 in nom_classes:
            i_classe = nom_classes.index(classe1)
            couples_classes[i_classe].append((nom1, nom2))
        else:
            couples_classes.append([(nom1, nom2)])
            nom_classes.append(classe1)

    f.close()

    return (nom_classes, couples_classes)

def write_cards (tex, nom_classes, couples_classes):
    """
    Ecrit le document LaTeX dans le fichier tex donné
    """
    #On sépare les cartes de chaque classe
    for i in range(len(nom_classes)):
        tex.write("\\LARGE " + nom_classes[i] + " \n")
        for j in range(0, 20):
            tex.write("\\videcarte \n")

        #On traite les cartes par paquet de 10 pour alterner les feuilles de Joueur et de leur cible au verso
        for j in range(0, len(couples_classes[i]), 10):
            batch = couples_classes[i][j:j+10]
            #On rajoute des cartes vides au cas où le paquet n'est pas complet
            while len(batch) != 10:
                batch.append((None, None))

            #Ecriture des cartes des Joueurs
            for nom_owner, _ in batch:
                if(nom_owner == None):
                    tex.write("\\videcarte \n")
                else:
                    tex.write(f"\\ownercarte{{{nom_owner}}}\n")

            #Ecriture des cartes des cibles
            #Il faut inverser les deux colonnes car c'est le verso de l'autre carte
            part_one = batch[0:5]
            part_two = batch[5:10]

            tex.write("\\oddsidemargin=20pt \n")

            #On ecrit d'abord la 2ème colonne
            for _, nom_target in part_two:
                if(nom_target == None):
                    tex.write("\\videcarte \n")
                else:
                    tex.write(f"\\ciblecarte{{{nom_target}}}\n")

            #Puis la 1ère
            for _, nom_target in part_one:
                if(nom_target == None):
                    tex.write("\\videcarte \n")
                else:
                    tex.write(f"\\ciblecarte{{{nom_target}}}\n")

            tex.write("\\oddsidemargin=0pt \n")


tex = open("cartes.tex", "w")

#On écrit l'entête nécessaire au fichier LaTeX
tex.write("""\\documentclass[a4paper,10pt]{letter}
\\usepackage[zw32010,crossmark]{ticket}
\\usepackage{graphicx}

\\renewcommand{\\ticketdefault}{}

\\newcommand{\\ciblecarte}[1]{\\ticket{
    \\put(31, 36){\\includegraphics[width=25mm,angle=0,origin=bl]{logo.png}}
    \\put(34, 25){\\scshape \\LARGE Cible:}
    \\put(38 ,15){\\makebox[10mm]{\\centering{\\scshape \\large #1}}}
}}

\\newcommand{\\ownercarte}[1]{\\ticket{%
    \\put(31, 36){\\includegraphics[width=25mm,angle=0,origin=bl]{logo.png}}
    \\put(38 ,23){\\makebox[10mm]{\\centering{\\scshape \\LARGE #1}}}
    \\put(15 ,8){\\scshape \\small Vous devez avoir la carte en main}
    \\put(29 ,4.5){\\scshape \\small pour faire un kill}
}}
          
\\newcommand{\\videcarte}[0]{\\ticket{}}

\\newcounter{numcards}

\\begin{document} \n""")

nom_classes, couples_classes = read_boucle_csv()

#On écrit les cartes
write_cards(tex, nom_classes, couples_classes)

tex.write("""\\end{document}""")
tex.close()

print("Fichier LaTeX des cartes construit dans cartes.tex")