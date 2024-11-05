import psutil
import subprocess
import re
import time

# Identifier le PID du processus de jeu
for proc in psutil.process_iter(['pid', 'name']):
    if proc.info['name'] == 'alex4':
        game_pid = proc.info['pid']
        break
else:
    raise Exception("Processus 'alex4' non trouvé.")

# Définir l'adresse mémoire du score et l'incrément souhaité
score_address = 0x7ffca8adb3e0
increment_value = 1000

def lire_score_actuel(pid, adresse):
    try:
        # Lire la valeur actuelle du score
        resultat = subprocess.check_output([
            "gdb", "-p", str(pid), "--batch", "-ex", f"x/d {hex(adresse)}"
        ]).decode()

        # Extraire la valeur numérique du score actuel avec une expression régulière
        score_match = re.search(r":\s+(\d+)", resultat)
        if score_match:
            score_actuel = int(score_match.group(1))
            return score_actuel
        else:
            print("Score non trouvé dans la sortie de gdb.")
            return None
    except Exception as e:
        print(f"Erreur de lecture du score : {e}")
        return None

def modifier_score(pid, adresse, nouveau_score):
    try:
        # Convertir le score en format GDB et écrire en mémoire
        subprocess.check_call([
            "gdb", "-p", str(pid), "--batch",
            "-ex", f"set *(int*){hex(adresse)} = {nouveau_score}"
        ])
        print(f"Valeur modifiée à : {nouveau_score}")
    except Exception as e:
        print(f"Erreur de modification du score : {e}")

# Lire le score actuel
score_actuel = lire_score_actuel(game_pid, score_address)
if score_actuel is not None:
    print(f"Score actuel : {score_actuel}")
    # Ajouter la valeur souhaitée et modifier le score
    nouveau_score = score_actuel + increment_value
    modifier_score(game_pid, score_address, nouveau_score)

    # Pause pour permettre la mise à jour
    time.sleep(1)  # Laisser un délai d'une seconde pour vérifier la mise à jour

    # Lire le score à nouveau pour vérifier s’il a changé
    score_apres_modif = lire_score_actuel(game_pid, score_address)
    if score_apres_modif is not None:
        print(f"Score après modification : {score_apres_modif}")
    else:
        print("Impossible de lire le score après modification.")
