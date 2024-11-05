Tout d'abord, lors du démarrage du jeu, on commence au niveau 1. Pour récupérer le PID du jeu, on utilise la commande suivante : 
  ps aux | grep alex4

![Capture d’écran 2024-11-05 à 09 15 42](https://github.com/user-attachments/assets/53f88eec-25e0-4a68-8a17-07ba92eab7f6)

Ensuite, grâce au script Python ptrace2_sc.py, on peut créer un fichier contenant toutes les adresses mémoire en format .txt en exécutant la commande :
  python3 ptrace2_sc.py

![Capture d’écran 2024-11-05 à 09 29 13](https://github.com/user-attachments/assets/89bf823e-ea1c-49ca-bccc-02bacb50575b)

Après avoir modifié le score dans le jeu, il faut modifier le nom de fichier dans le code ptrace2_sc.py. Le premier fichier généré s’appelle new_memory.txt et le deuxième new_memory2.txt et ils auront du coup deux scores differents

![Capture d’écran 2024-11-05 à 09 33 31](https://github.com/user-attachments/assets/420db7dc-4400-45a8-a2ff-f8e40392e59a)


En utilisant le script compare.py, on peut comparer les deux fichiers texte pour voir les différences et identifier l'adresse où le score est stocké:
python3 compare.py

et on peut voir ceci:
![Capture d’écran 2024-11-05 à 09 35 59](https://github.com/user-attachments/assets/f622928d-e3bb-488a-a5c5-38ecd01f05a5)

Dans cet exemple, 0x294 en hexadécimal vaut 660, et 0x3ca vaut 970. Ce sont les valeurs de score dans mes fichiers new_memory1 et new_memory2.

![Capture d’écran 2024-11-05 à 09 40 04](https://github.com/user-attachments/assets/e85bf7cd-ad8f-4170-b699-359308e91d75)


Donc l'adresse se trouve bien a la ligne 15194: 

![Capture d’écran 2024-11-05 à 09 39 31](https://github.com/user-attachments/assets/87879d2b-4583-499b-8513-2e71af5fca09)
Ici il y a un écart de 1 car la ligne commence à 0

Ensuite, on utilise scanmem avec les étapes suivantes :
![Capture d’écran 2024-11-05 à 09 42 34](https://github.com/user-attachments/assets/f6a9627e-5778-4254-a136-25e3f067d4ef)
![Capture d’écran 2024-11-05 à 09 43 03](https://github.com/user-attachments/assets/8a061975-1ac8-457a-b285-08121f1c71cc)

Dans scanmem, on saisit d'abord le PID (ici 2027), puis le score actuel (ici 970). Comme il y a plusieurs adresses correspondantes, on augmente un peu le score dans le jeu (par exemple, on l’augmente à 1010). Ensuite, il ne reste que deux adresses en commun :

![Capture d’écran 2024-11-05 à 09 46 57](https://github.com/user-attachments/assets/0b0a5152-53c7-43c7-9a54-9389c9c45446)

On retrouve l’adresse identifiée par compare.py et une autre adresse : 55fb19b51c48. C'est cette seconde adresse, l’adresse miroir, qui peut être modifiée. Dans le script modifie.py, on modifie l'adresse en bas de code pour y indiquer 0x55fb19b51c48, et on y place le score souhaité.
![Capture d’écran 2024-11-05 à 09 50 40](https://github.com/user-attachments/assets/c5d68f6c-ea49-45aa-83e6-c774788d650d)
![Capture d’écran 2024-11-05 à 09 54 02](https://github.com/user-attachments/assets/6513ad94-829c-4cf7-b112-7992b9d5638b)
![Capture d’écran 2024-11-05 à 09 54 25](https://github.com/user-attachments/assets/f2a4dea4-36de-4063-9d58-8abf4debeba8)

Et voilà, le score a bien été modifié !









  
