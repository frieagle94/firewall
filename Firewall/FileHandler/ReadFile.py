import os

__author__ = 'Riccardo Frigerio'

# METODO per l'apertura di un file
def openFile(filename):
    try:
        base_dir = os.getenv("HOME")
        ryu_dir = "ryu"
        file_dir = "topoOutput"

        # Creazione della path
        path = os.path.join(base_dir, ryu_dir, file_dir, filename)

        # Apertura file
        in_file = open(path, "r")

        return in_file
        
    except IOError, ex:
        print ex

    return None


# METODO per la chiusura di un file precedentemente aperto
def closeFile(in_file):
    
    # Chiusura file
    in_file.close()
