import ptrace.debugger
import time
import numpy as np
import os

def pause_game(pid):
    debugger = ptrace.debugger.PtraceDebugger()
    process = debugger.addProcess(pid, False)
    print(f"Process {pid} en pause.")
    time.sleep(5)  # Met en pause le processus pendant 5 secondes
    return process  # Retourne le processus pour une utilisation ultérieure

def get_stack_memory_mappings(pid):
    """Renvoie les mappings de mémoire du stack d'un processus et les affiche.
    
    Arguments:
        pid -- int, le PID du processus concerné.
    """
    try:
        with open(f"/proc/{pid}/maps", "r") as f:
            mappings = f.readlines()
            stack_mapping = [mapping.strip() for mapping in mappings if 'stack' in mapping]
            if stack_mapping:
                print("Mappings de mémoire du stack :")
                for mapping in stack_mapping:
                    print(mapping)
                return stack_mapping[0]  # Retourne le premier mapping trouvé
            else:
                print("Aucun mapping de mémoire du stack trouvé.")
                return None
    except FileNotFoundError:
        print(f"Process {pid} not found. It may have terminated.")
    except Exception as e:
        print(f"Error getting memory mappings: {e}")

def read_stack_memory(process, start, end):
    """Lit la mémoire du stack entre les adresses start et end.
    
    Arguments:
        process -- PtraceProcess, le processus à partir duquel lire.
        start -- int, adresse de début.
        end -- int, adresse de fin.
    """
    stack_data = []
    address = start
    while address < end:
        try:
            word = process.readWord(address)  # Lire un mot à l'adresse donnée
            stack_data.append((address, word))  # Ajouter l'adresse et le mot à la liste
            address += 8  # Avancer à l'adresse suivante (8 octets pour une adresse 64 bits)
        except Exception as e:
            print(f"Error reading memory at {hex(address)}: {e}")
            break
    return stack_data

def compare_arrays(array1, array2):
    """Compare deux tableaux NumPy et affiche les différences."""
    diff = array1 != array2
    for index, is_different in enumerate(diff):
        if is_different:
            print(f"Differente à l'index {index}: {hex(array1[index])} -> {hex(array2[index])}")

def save_memory_to_file(memory_data, filename):
    """Enregistre les données de mémoire dans un fichier."""
    with open(filename, 'w') as f:
        for address, value in memory_data:
            f.write(f"{hex(address)}, {hex(value)}\n")

def load_memory_from_file(filename):
    """Charge les données de mémoire à partir d'un fichier et les retourne sous forme de tableau NumPy."""
    addresses, values = [], []
    with open(filename, 'r') as f:
        for line in f:
            address, value = line.strip().split(', ')
            addresses.append(int(address, 16))
            values.append(int(value, 16))
    return np.array(addresses, dtype=np.uint64), np.array(values, dtype=np.uint64)

if __name__ == "__main__":
    pid = int(input("PID? : "))
    process = pause_game(pid)
    
    # Récupérer les mappings de mémoire du stack
    stack_mapping = get_stack_memory_mappings(pid)

    # Lire la mémoire du stack si un mapping est trouvé
    if stack_mapping:
        # Extraire les adresses de début et de fin
        addresses = stack_mapping.split()[0:2]  # Prendre les deux premières colonnes
        start = int(addresses[0].split('-')[0], 16)  # Adresse de début
        end = int(addresses[0].split('-')[1], 16)  # Adresse de fin
        
        # Lire la mémoire du stack
        stack_memory = read_stack_memory(process, start, end)

        # Créer un tableau NumPy pour stocker les valeurs du stack
        original_values = np.array([data for address, data in stack_memory], dtype=np.uint64)

        # Enregistrer les valeurs initiales dans un fichier
        save_memory_to_file(stack_memory, "initial_memory3.txt")
        print("Valeurs initiales enregistrées.")

        # Simuler la modification des valeurs du jeu
        if len(original_values) > 0:
            original_values[0] += 10  # Incrémenter le score pour simuler une partie
            # Notez que ce changement est local dans le tableau, mais pas encore écrit dans le processus.

        # Lire à nouveau la mémoire après les modifications (ici on va relire directement le même endroit)
        new_stack_memory = read_stack_memory(process, start, end)
        new_values = np.array([data for address, data in new_stack_memory], dtype=np.uint64)

        # Enregistrer les nouvelles valeurs dans un fichier
        save_memory_to_file(new_stack_memory, "new_memory3.txt")
        print("Nouvelles valeurs enregistrées.")

        # Comparer les tableaux
        print("\nComparaison des valeurs du stack :")
        compare_arrays(original_values, new_values)

    # Nettoyage
    try:
        process.detach()  # Détacher le processus
    except Exception as e:
        print(f"Error detaching process: {e}")
