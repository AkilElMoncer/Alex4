# Modification de Score dans le Jeu ALEX4

## **Auteurs**
- **El Moncer Akil**
- **Alexanian Eric**
- **Wache Tristan**

---

## **1. Introduction**

Dans cet exercice éducatif, nous expliquons comment modifier le score dans le jeu ALEX4 en manipulant directement les adresses mémoire du jeu. Les étapes suivantes incluent l'identification du PID, l'analyse des différences de mémoire et la modification du score via des scripts Python et des outils comme `scanmem`.

---

## **2. Identifier le PID du jeu**

1. Lancez le jeu ALEX4.
2. Identifiez le PID du processus en exécutant la commande suivante :
   ```bash
   ps aux | grep alex4
   ```

   Exemple de résultat :
   ![Capture PID](https://github.com/user-attachments/assets/53f88eec-25e0-4a68-8a17-07ba92eab7f6)

---

## **3. Générer les fichiers mémoire**

### Étape 1 : Exécuter `ptrace2_sc.py`
Utilisez le script Python `ptrace2_sc.py` pour générer un fichier contenant les adresses mémoire :
```bash
python3 ptrace2_sc.py
```

Le fichier généré est nommé **`new_memory.txt`**.

### Étape 2 : Modifier le score dans le jeu
1. Augmentez le score dans le jeu.
2. Exécutez à nouveau `ptrace2_sc.py` pour générer un deuxième fichier : **`new_memory2.txt`**.

   Exemple de capture :
   ![Fichiers mémoire générés](https://github.com/user-attachments/assets/420db7dc-4400-45a8-a2ff-f8e40392e59a)

---

## **4. Comparer les fichiers mémoire**

Utilisez le script `compare.py` pour identifier les différences entre les deux fichiers mémoire :
```bash
python3 compare.py
```

Exemple de résultat :
![Résultats de compare.py](https://github.com/user-attachments/assets/f622928d-e3bb-488a-a5c5-38ecd01f05a5)

### Identification des adresses
- Dans cet exemple, les adresses 0x294 et 0x3ca représentent respectivement les scores 660 et 970.
- L'adresse mémoire correspondante est confirmée à la ligne 15194 :
   ![Adresse mémoire](https://github.com/user-attachments/assets/87879d2b-4583-499b-8513-2e71af5fca09)

---

## **5. Modifier le score avec scanmem**

### Étape 1 : Lancer `scanmem`
1. Exécutez `scanmem` et saisissez le PID du jeu :
   ```bash
   scanmem
   > pid 2027
   ```

2. Entrez le score actuel (exemple : 970).

### Étape 2 : Identifier les adresses restantes
1. Augmentez le score dans le jeu (par exemple, à 1010).
2. Les adresses restantes incluent l'adresse principale et une adresse miroir :
   ![Adresses identifiées](https://github.com/user-attachments/assets/0b0a5152-53c7-43c7-9a54-9389c9c45446)

---

## **6. Modifier le score avec modifie.py**

### Étape 1 : Modifier le script
Dans `modifie.py`, remplacez l'adresse par celle identifiée :
```python
address = 0x55fb19b51c48  # Exemple d'adresse miroir
score = 9999             # Nouveau score
```

### Étape 2 : Exécuter le script
```bash
python3 modifie.py
```

### Résultat attendu
- Le score est modifié dans le jeu, comme illustré ci-dessous :
   ![Modification réussie](https://github.com/user-attachments/assets/c5d68f6c-ea49-45aa-83e6-c774788d650d)

---

## **7. Modifier directement avec scanmem**

Vous pouvez également modifier le score directement dans le terminal avec `scanmem` :
```bash
> set 9999
```

Exemple :
![Modification via scanmem](https://github.com/user-attachments/assets/6513ad94-829c-4cf7-b112-7992b9d5638b)

---

## **8. Résultat Final**

- Le score a été modifié avec succès dans le jeu ALEX4.
- Les outils utilisés (scripts Python, scanmem) ont permis d'identifier et de manipuler les adresses mémoire du jeu de manière efficace.

---
