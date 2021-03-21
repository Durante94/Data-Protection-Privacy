import pandas as pd


class DataFrame:
    # costruttore
    def __init__(self, namefile, size, s, qi):
        self.nameFile = namefile
        self.size = size
        self.s = s
        self.qi = qi

    def df_creation(self):
        # TODO:
        #   1. lettura del dataset di input e salvataggio in un array di transazioni
        #   2. creazione del dataframe dall'array di transizioni (vedere libreria pandas.dataframe
        #   3. creazione della matrice quadrata di dimensione size*size
        #   4. estrazione SD e QI
        #   il dataframe creato potrà quindi essere dato in pasto a scipy.sparse.csgraph.reverse_cuthill_mckee. Decidere
        #   quindi se farlo direttamente all'interno di questa classe (importando scipy qui) oppure nel main.
        return


