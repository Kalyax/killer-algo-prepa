import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.exceptions import InvalidSignature
from cryptography.fernet import InvalidToken
from getpass import getpass

print("Si vous souhaitez chiffrer, inventez un mot de passe")
print("Si vous souhaitez déchiffrer, donnez le mot de passe utilisé lors du chiffrement")
password = getpass("Mot de passe (le mot de passe est invisible à l'écran mais il s'écrit bien): ").encode("ascii")
salt = "killer".encode("ascii")
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=390000,
)
key = base64.urlsafe_b64encode(kdf.derive(password))
f = Fernet(key)

try:
    boucle_f = None
    encrypt_f = None
    choix = input("Ecrivez 1 pour chiffrer la boucle ou 2 pour la déchiffrer: ")
    if choix == "1":
        boucle_f = open("boucle.txt", "r")
        encrypt_f = open("encrypt.txt", "w")
        boucle = boucle_f.read().encode("ascii")
        boucle_encrypt = f.encrypt(boucle)
        encrypt_f.write(boucle_encrypt.decode("utf-8"))
        os.remove("boucle.txt")
        print("La boucle a été chiffrée dans le fichier encrypt.txt avec le mot de passe donné. Le fichier boucle.txt a été supprimé")
    elif choix == "2":
        boucle_f = open("boucle.txt", "w")
        encrypt_f = open("encrypt.txt", "r")
        boucle_encrypt = encrypt_f.read().encode("ascii")
        boucle = f.decrypt(boucle_encrypt)
        boucle_f.write(boucle.decode("utf-8"))
        print("La boucle a été déchiffrée dans le fichier boucle.txt")
    else:
        print("ERREUR: Ce choix n'existe pas, relancez le programme")
    boucle_f.close()
    encrypt_f.close()
except FileNotFoundError:
    print("ERREUR: Impossible de trouver les fichiers boucle.txt ou encrypt.txt. Ils doivent être dans le même dossier que encrypt.py")
except InvalidSignature:
    print("ERREUR: Le mot de passe est incorrect")
except InvalidToken:
    print("ERREUR: Le mot de passe est incorrect")
