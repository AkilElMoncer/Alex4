import numpy as np

def load_memory_from_file(filename):
    """Charge les données de mémoire à partir d'un fichier et les retourne sous forme de tableau NumPy."""
    addresses, values = [], []
    with open(filename, 'r') as f:
        for line in f:
            address, value = line.strip().split(', ')
            addresses.append(int(address, 16))
            values.append(int(value, 16))
    return np.array(addresses, dtype=np.uint64), np.array(values, dtype=np.uint64)

def compare_arrays(array1, array2):
    """Compare deux tableaux NumPy et affiche les différences."""
    diff = array1 != array2
    for index, is_different in enumerate(diff):
        if is_different:
            print(f"Differente à l'index {index}: {hex(array1[index])} -> {hex(array2[index])}")

if __name__ == "__main__":
    # Charger les valeurs des deux fichiers
    addresses1, values1 = load_memory_from_file("new_memory2.txt")
    addresses2, values2 = load_memory_from_file("new_memory3.txt")

    # Afficher les adresses chargées
    print("Adresses et valeurs dans new_memory2.txt :")
    for address, value in zip(addresses1, values1):
        print(f"Adresse: {hex(address)}, Valeur: {hex(value)}")

    print("\nAdresses et valeurs dans new_memory3.txt :")
    for address, value in zip(addresses2, values2):
        print(f"Adresse: {hex(address)}, Valeur: {hex(value)}")

    # Comparer les valeurs
    print("\nComparaison des valeurs :")
    compare_arrays(values1, values2)
