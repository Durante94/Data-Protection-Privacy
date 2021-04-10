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
        self.prova = dict()
        for sd in SDCols:
            self.hist[sd] = 0
    def compute_histogram(self):
        # DEBUG (da rimuovere)
        for i in self.SDvals:
            self.hist[i] = 0
        for index, row in self.df.iterrows():
            for column in self.df:
                if column in self.SDvals and (self.df.loc[row.name, column] == True):
                    self.hist[column] += 1

        #for sd in self.SDCols:
        #    for i, val in self.df[sd].items():
        #        if val:
        #            self.hist[sd] += 1
        print(self.hist)

        self.prova = dict(self.df[self.SDvals].sum())
        print(self.prova)

    def checkPrivacy(self):
        for value in self.hist.values():
            if value * self.p >= len(self.df) - 1:
                return False
        return True

    def checkConflict(self):

        return

    def startAlgorithm(self):
        self.compute_histogram()
        satisfiable = False
        while not satisfiable and self.p > 0:
            satisfiable = self.checkPrivacy()
            if not satisfiable:
                self.checkPrivacy() - 1
        print(("Privacy degree satisfiable: ", self.p))
        remaining = len(self.df)
