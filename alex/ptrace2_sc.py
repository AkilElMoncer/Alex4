import ptrace.debugger
import time

def pause_game(pid):
    """Met en pause le processus spécifié pendant 5 secondes."""
    debugger = ptrace.debugger.PtraceDebugger()
    process = debugger.addProcess(pid, False)
    print(f"Processus {pid} en pause.")
    time.sleep(5)
    return process

def get_stack_memory_range(pid):
    """Récupère les adresses de début et de fin de la mémoire du stack pour le processus."""
    try:
        with open(f"/proc/{pid}/maps", "r") as f:
            for line in f:
                if 'stack' in line:
                    start, end = line.split()[0].split('-')
                    return int(start, 16), int(end, 16)
            print("Aucun stack mapping trouvé.")
            return None, None
    except FileNotFoundError:
        print(f"Le processus {pid} est introuvable.")
    except Exception as e:
        print(f"Erreur lors de la récupération du stack: {e}")
    return None, None

def read_memory(process, start, end):
    """Lit la mémoire entre deux adresses et renvoie les données sous forme de liste."""
    data = []
    for address in range(start, end, 8):  # Lit des mots de 8 octets (64 bits)
        try:
            word = process.readWord(address)
            data.append((address, word))
        except:
            break
    return data

def save_to_file(data, filename):
    """Enregistre les données de mémoire dans un fichier texte."""
    with open(filename, 'w') as f:
        for address, value in data:
            f.write(f"{hex(address)}, {hex(value)}\n")
    print(f"Données enregistrées dans {filename}")

if __name__ == "__main__":
    pid = int(input("Entrez le PID du processus : "))
    process = pause_game(pid)

    # Récupère les adresses de début et de fin de la mémoire du stack
    start, end = get_stack_memory_range(pid)
    
    if start and end:
        # Lit et enregistre la mémoire du stack
        memory_data = read_memory(process, start, end)
        save_to_file(memory_data, "new_memory.txt")
    
    process.detach()  # Détache le processus
