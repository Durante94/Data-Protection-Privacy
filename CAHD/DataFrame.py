import pandas as pd
import os
from scipy.sparse.csgraph import reverse_cuthill_mckee
from scipy.sparse import csc_matrix
from mlxtend.preprocessing import TransactionEncoder
from Plot import plot

class DataFrame:
    # costruttore
    def __init__(self, namefile, size, s, qi):
        self.nameFile = namefile
        self.size = size
        self.s = s
        self.qi = qi

    def df_creation(self):

        # LETTURA FILE
        path = os.path.join(os.getcwd(), "BMS1_spmf.txt")
        matrix = []
        with open(path) as fp:
            for line in fp:
                trans = [int(s) for s in line.split() if (s!='-1' and s!='-2')]
                matrix.append(trans)

        # CODIFICA DEL DATASET DI TRANSAZIONI IN UN ARRAY NUMPY
        te = TransactionEncoder()
        te_ary = te.fit(matrix).transform(matrix)

        # CREAZIONE DEL DATAFRAME
        df = pd.DataFrame(te_ary, columns=te.columns_)

        # TAGLIO DEL DATAFRAME ED ASSEGNAZIONE QI E SD
        if (self.size >= 497):
            # TODO: ESTRAZIONE DI QI RANDOM (vedere df.sample)
            # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sample.html

            # TODO: ESTRAZIONE DI SD RANDOM (vedere df.sample)

            # TODO: VERIFICA CHE QI ed SD NON SIANO UGUALI

            # AGGIUNTA DEI FAKE ITEMS
            add_cols = self.size - 497
            for i in range(0, add_cols):
                df['fake_item_'+str(i)] = False
        else:
            # TODO: ESTRAZIONE DI QI RANDOM

            # TODO ESTRAZIONE DI SD RANDOM

            # TODO: VERIFICA CHE QI ED SD NON SIANO UGUALI
            print("DEBUG: blocco < 497")

        # SELEZIONO UN SOTTOINSIEME QUADRATO (dimensioni size*size) DEL DATAFRAME
        df = df.iloc[0:self.size, 0:self.size]

        # CALCOLO IL VETTORE DELLE PERMUTAZIONI
        graph = csc_matrix(df.values)
        aux = reverse_cuthill_mckee(graph, False)

        # GENERO LA BAND MATRIX
        rows = list(df.index.values)
        rows2 = []
        for i in aux:
            rows2.append(rows[i])
        df = df.reindex(rows2)
        cols = list(df.columns.values)
        cols2 = []
        for i in aux:
            cols2.append(cols[i])
        df = df[cols2]

        # STAMPA DEL NUMERO DI TRANSAZIONI E ITEM TOTALI CONTENUTI NELLA BAND MATRIX
        shape = df.shape
        print("numero di transazioni:", shape[0]) # Righe
        print("numero di items:", shape[1]) # Colonne

        # PLOT DELLA BAND MATRIX
        plot(df, "BAND MATRIX")









