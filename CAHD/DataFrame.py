import pandas as pd
import os
from scipy.sparse.csgraph import reverse_cuthill_mckee
from scipy.sparse import csc_matrix
from mlxtend.preprocessing import TransactionEncoder
from Plot import plot


class DataFrame:
    # constructor
    def __init__(self, namefile, size, sd, qi):
        self.nameFile = namefile
        self.size = size
        self.sd = sd
        self.qi = qi
        self.SDcols = None
        self.QIcols = None
        self.df = None

    def df_creation(self):

        # READING FILE
        path = os.path.join(os.getcwd(), "BMS1_spmf.txt")
        matrix = []
        with open(path) as fp:
            for line in fp:
                trans = [int(s) for s in line.split() if (s != '-1' and s != '-2')]
                matrix.append(trans)

        # CODIFICA DEL DATASET DI TRANSAZIONI IN UN ARRAY NUMPY E CREAZIONE DEL DATAFRAME
        te = TransactionEncoder()
        te_ary = te.fit(matrix).transform(matrix)
        df = pd.DataFrame(te_ary) #, columns=te.columns_

        # SE LA DIMENSIONE E' > DEL DATASET ALLORA SELEZIONO QI, SD E SUCCESSIVAMENTE AGGIUNGO FAKE ITEMS
        if self.size >= 497:
            # ESTRAZIONE DI QI E SD RANDOM
            dfCols = df.sample(self.qi + self.sd, axis=1).columns.values
            # print(dfCols)

            # prendiamo le self.qi colonne e le salviamo in self
            self.QIcols = dfCols[:self.qi]

            # prendiamo le altre self.s colonne e le salviamo in self
            self.SDcols = dfCols[self.qi:]

            # AGGIUNTA DEI FAKE ITEMS
            add_cols = self.size - 497
            for i in range(0, add_cols):
                df['fake_item_' + str(i)] = False

        # SELEZIONO UN SOTTOINSIEME QUADRATO (dimensioni size*size) DEL DATAFRAME -> TAGLIO DEL DF
        df = df.iloc[0:self.size, 0:self.size]

        # SE LA DIMENSIONE E' MINORE DI 497 SELEZIONO QI ED SD SUL DF TAGLIATO
        if self.size <= 497:
            # ESTRAZIONE DI QI E SD RANDOM
            dfCols = df.sample(self.qi + self.sd, axis=1).columns.values
            # print(dfCols)

            # prendiamo le self.qi colonne e le salviamo in self
            self.QIcols = dfCols[:self.qi]

            # prendiamo le altre self.s colonne e le salviamo in self
            self.SDcols = dfCols[self.qi:]

        # CALCOLO IL VETTORE DELLE PERMUTAZIONI
        graph = csc_matrix(df.values)
        aux = reverse_cuthill_mckee(graph, False)

        # GENERO LA BAND MATRIX
        rows = list(df.index.values)  # recupero i valori degli indici (righe)
        rows2 = []
        for i in aux:
            rows2.append(rows[i])  # li riordino secondo gli indici salvati in aux
        df = df.reindex(rows2)  # carico il nuovo indice
        cols = list(df.columns.values)  # recupero i valori delle colonne
        cols2 = []
        for i in aux:
            cols2.append(cols[i])
        df = df[cols2]

        return df, self.SDcols, self.QIcols
