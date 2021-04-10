import pandas as pd
import numpy as np


class CAHD:

    def __init__(self, df, p, alpha, SDCols, QICols):
        self.df = df
        self.p = p
        self.alpha = alpha
        self.SDCols = SDCols
        self.QICols = QICols
        self.hist = dict()
        for sd in SDCols:
            self.hist[sd] = 0

    def compute_histogram(self):
        """
        histogram = dict()
        for sd in self.SDCols:
            histogram[str(sd)] = self.df[str(sd)]
        return histogram
        """
        #self.hist = dict(self.df[self.SDCols].sum())

        for sd in self.SDCols:
            for i, val in self.df[sd].items():
                if val:
                    self.hist[sd] += 1

        print(self.hist)

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




