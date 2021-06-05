import pandas as pd
import os
from Plot import plot
from scipy.sparse.csgraph import reverse_cuthill_mckee
from scipy.sparse import csc_matrix
from mlxtend.preprocessing import TransactionEncoder
from sklearn.utils import shuffle


class DataFrameNORCM:
    # Constructor
    def __init__(self, namefile, size, sd, qi, maxsize):
        self.nameFile = namefile
        self.size = size
        self.sd = sd
        self.qi = qi
        self.SDcols = None
        self.QIcols = None
        self.df = None
        self.maxSize = maxsize

    def singleSdQi(self):
        # Extraction of quasi-identifier and sensitive data random
        dfCols = self.df.sample(self.qi + self.sd, axis=1).columns.values

        # Take the self.qi columns and save them in self
        self.QIcols = dfCols[:self.qi]

        # Take the others self.s columns and save them in self
        self.SDcols = dfCols[self.qi:]

    def multipleSdQi(self):
        QIvalues = []
        SDvalues = []
        for _ in range(0, len(self.sd)):
            dfCols = self.df.sample(
                self.qi + self.sd[_], axis=1).columns.values
            QIcols = dfCols[:self.qi]
            SDcols = dfCols[self.qi:]
            QIvalues.append(QIcols)
            SDvalues.append(SDcols)
        return SDvalues, QIvalues

    def df_creation(self):
        # Reading file
        path = os.path.join(os.getcwd(), self.nameFile)
        matrix = []
        with open(path) as fp:
            for line in fp:
                trans = [int(s)
                         for s in line.split() if (s != '-1' and s != '-2')]
                matrix.append(trans)

        # Creation of the dataset of transactions in a Numpy array and creation of the dataframe
        te = TransactionEncoder()
        te_ary = te.fit(matrix).transform(matrix)
        self.df = pd.DataFrame(te_ary, columns=te.columns_)

        # If the dimension is greater than the dimension of the dataset,
        # then select quasi-identifiers, sensitive datas and add fake items
        if self.size >= self.maxSize:
            if not isinstance(self.sd, list):
                self.singleSdQi()
            else:
                self.SDcols, self.QIcols = self.multipleSdQi()

            # Add the fake items
            add_cols = self.size - self.maxSize
            for i in range(0, add_cols):
                self.df['fake_item_' + str(i)] = False

        # Select a square subset ( dimension size*size) of the dataframe, then cut the dataframe
        self.df = self.df.iloc[0:self.size, 0:self.size]
        self.df = shuffle(self.df)

        # Plot of the initial dataset
        plot(self.df, "Initial Dataset NORCM")

        # If the dimension is less than self.maxSize, select quasi-identifiers and sensitive datas on the
        # dataframe cut
        if self.size <= self.maxSize:
            if not isinstance(self.sd, list):
                self.singleSdQi()
            else:
                self.SDcols, self.QIcols = self.multipleSdQi()

        print(self.df.shape)
        return self.df, self.SDcols, self.QIcols

    # Algorithm for compute the reverse_cuthill_mckee on the df
    def doRCM(self):
        # Compute the vector of permutations
        graph = csc_matrix(self.df.values)
        aux = reverse_cuthill_mckee(graph, False)

        # Generate the band matrix
        # recupero i valori degli indici (righe)
        rows = list(self.df.index.values)
        rows2 = []
        for i in aux:
            # li riordino secondo gli indici salvati in aux
            rows2.append(rows[i])
        self.df = self.df.reindex(rows2)  # carico il nuovo indice
        cols = list(self.df.columns.values)  # recupero i valori delle colonne
        cols2 = []
        for i in aux:
            cols2.append(cols[i])
        self.df = self.df[cols2]

        return self.df
