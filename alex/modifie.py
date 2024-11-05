import os
import subprocess

def modify_memory_value(pid, address, increment):
    current_score = read_memory_value(pid, address)
    if current_score is None:
        print("Impossible de lire le score actuel.")
        return

    print(f"Score actuel : {current_score}")

    # Calculer le nouveau score
    new_score = current_score + increment
    print(f"Nouvelle valeur calculée pour le score : {new_score}")

    # Commande GDB pour écrire la nouvelle valeur en mémoire
    gdb_command = f"gdb -p {pid} --batch -ex 'set *(int*){hex(address)}={new_score}' -ex 'detach' -ex 'quit'"
    
    # Exécution de la commande GDB
    result = subprocess.run(gdb_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Vérification des erreurs
    if result.returncode == 0:
        print(f"Score modifié à : {new_score} à l'adresse {hex(address)}")
    else:
        print(f"Erreur GDB : {result.stderr.decode()}")

def read_memory_value(pid, address):
    gdb_command = f"gdb -p {pid} --batch -ex 'print *(int*){hex(address)}' -ex 'detach' -ex 'quit'"
    
    result = subprocess.run(gdb_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode == 0:
        output = result.stdout.decode()
        print(f"Sortie de GDB : {output}")  # Afficher la sortie pour le débogage
        try:
            lines = output.splitlines()
            for line in lines:
                if line.startswith('$1 ='):
                    score_value = line.split('=')[1].strip()
                    return int(score_value.split()[0], 16)
            print("Erreur : valeur du score introuvable dans la sortie.")
            return None
        except (IndexError, ValueError) as e:
            print(f"Erreur lors de l'extraction du score : {e}")
            return None
    else:
        print(f"Erreur GDB lors de la lecture : {result.stderr.decode()}")
        return None

if __name__ == "__main__":
    game_pid = int(input("Entrez le PID du processus à analyser : "))
    score_address = 0x55fb19b51c48  # L'adresse correcte que vous avez déterminée
    increment_value = 100000000000

    modify_memory_value(game_pid, score_address, increment_value)
