import pandas as pd
import numpy as np
from group import make_group


class CAHD:

    def __init__(self, df, p, alpha, SDvals, QIvals):
        self.df = df
        self.p = p
        self.alpha = alpha
        self.SDvals = SDvals
        self.QIvals = QIvals
        self.hist = dict()

    # INIZIALIZZO L'ISTOGRAMMA PER OGNI SD
    def compute_histogram(self):
        self.hist = dict(self.df[self.SDvals].sum())
        countSDinDf = 0
        for v in self.hist.values():
            countSDinDf += v 
        if countSDinDf == 0:
            print("No sensitive items")
        return countSDinDf

    def checkPrivacy(self):
        for value in self.hist.values():
            if value * self.p >= len(self.df) - 1:
                return False
        return True

    def startAlgorithm(self):
        count = self.compute_histogram()
        if count == 0:
            return
        satisfiable = False
        while not satisfiable and self.p > 0:
            satisfiable = self.checkPrivacy()
            if not satisfiable:
                self.p -= 1
        print("Privacy degree satisfiable: ", self.p)
        remaining = len(self.df.index)
        
        # CREAZIONE DEI GRUPPI
        result = make_group(self.df, self.SDvals, self.QIvals, self.p, self.alpha, self.hist, self.df.shape[0], remaining)
        return result, count

