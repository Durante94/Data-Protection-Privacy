import pandas as pd
import os
from scipy.sparse.csgraph import reverse_cuthill_mckee
from scipy.sparse import csr_matrix
from scipy.sparse import csc_matrix

class DataFrame:
    # costruttore
    def __init__(self, namefile, size, s, qi):
        self.nameFile = namefile
        self.size = size
        self.s = s
        self.qi = qi

    def df_creation(self):
        # TODO:
        #   1.  lettura del dataset di input e salvataggio in un array di
        #   transazioni
        #   2.  creazione del dataframe dall'array di transizioni (vedere
        #   libreria pandas.dataframe)
        #   3.  creazione della matrice quadrata di dimensione size*size
        #   4.  estrazione SD e QI il dataframe creato potrà quindi essere dato
        #   in pasto a scipy.sparse.csgraph.reverse_cuthill_mckee.
        #       Decidere quindi se farlo direttamente all'interno di questa
        #       classe (importando scipy qui) oppure nel main.

        # APERTURA FILE
        f = open(os.path.join(os.getcwd(), "CAHD\BMS1_spmf.txt"), "r")
        matrix = []

        # LETTURA FILE
        for row in range(0, int(self.size)):
            readedLine = f.readline().split()
            matrix.append([])

            for val in readedLine:
                if int(val) == -2: # fine linea
                    break

                if int(val) == -1: # elemento di separazione valori
                    continue

                matrix[row].append(int(val))

            # COMPLETAMENTO COLONNA PER OTTENERE MATRICE OMOGENEA QUADRATA
            tmp = len(matrix[row])
            if tmp < self.size:
                matrix[row].extend([0] * (self.size - tmp)) # SIA BENEDETTO STACK OVERFLOW

        #CHIUSURA FILE
        f.close()

        revDF = reverse_cuthill_mckee(csr_matrix(matrix), False)

        toDF = []

        # PRINT SU FILE STRUTTURA DATI
        fPre = open(os.path.join(os.getcwd(), "CAHD\preElab.txt"), "w")
        for row in matrix:
            for val in row:
                fPre.write(str(val))
                fPre.write(', ')
            fPre.write('\n')
        fPre.close()

        for rowIdx in revDF:
            toDF.append(matrix[rowIdx])

        # PRINT SU FILE DATI PERMUTATI
        fPost = open(os.path.join(os.getcwd(), "CAHD\postElab.txt"), "w")
        for row in toDF:
            for val in row:
                fPost.write(str(val))
                fPost.write(', ')
            fPost.write('\n')
        fPost.close()

        #CREAZIONE DATAFRAME
        df = pd.DataFrame.from_records(toDF)

        return


