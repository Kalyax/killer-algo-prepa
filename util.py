#############################################
#SCRIPT POUR CREER UN FICHIER CONFIG DE TEST#
#############################################

#pip install names_generator
from names_generator import generate_name

f = open("config.csv", "w")

index_classes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
nom_classes = ["MPSI", "PCSI", "MP2I", "ECG1", "ECG2", "HK", "KH", "MP", "MPI", "PC", "PSI"]
taille_classes = [45, 48, 24, 15, 25, 37, 45, 28, 23, 34, 46]

texte = "Classe,Joueur\n"
for classe in index_classes:
    for i in range(taille_classes[classe]):
        texte += nom_classes[classe] + "," + generate_name(style='capital') + "\n"

f.write(texte)
f.close()

