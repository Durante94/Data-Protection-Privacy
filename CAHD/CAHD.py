import pandas as pd
import numpy as np


class CAHD:

    def __init__(self, df, p, alpha, SDvals, QIvals):
        self.df = df
        self.p = p
        self.alpha = alpha
        self.SDvals = SDvals
        self.QIvals = QIvals
        self.hist = dict()
        # self.prova = dict()

    def compute_histogram(self):
        # DEBUG (da rimuovere)
        # for index, row in self.df.iterrows():
        #    for column in self.df:
        #        if column in self.SDvals and (self.df.loc[row.name, column] == True):
        #            self.hist[column] += 1
        self.hist = dict(self.df[self.SDvals].sum())
        # print(self.hist)
        empty = False
        for v in self.hist.values():
            empty = v > 0 or empty
        if not empty:
            print("No sensitive items")
        return empty

    def sensitiveTransactions(self):
        trans = set(list(np.where(self.df[self.SDvals] == True)[0]))
        print("trans:", sorted(trans))
        print(self.df.loc[trans])

    def checkPrivacy(self):
        for value in self.hist.values():
            if value * self.p >= len(self.df) - 1:
                return False
        return True

    def checkConflict(self):

        return

    def startAlgorithm(self):
        if not self.compute_histogram():
            return
        satisfiable = False
        while not satisfiable and self.p > 0:
            satisfiable = self.checkPrivacy()
            if not satisfiable:
                self.p -= 1
        print(("Privacy degree satisfiable: ", self.p))
        remaining = len(self.df)
        self.sensitiveTransactions()
        tfile = open('test.txt', 'w')
        tfile.write(self.df.to_string())
        tfile.close()
