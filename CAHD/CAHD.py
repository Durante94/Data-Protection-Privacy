import pandas as pd
import numpy as np


class CAHD:

    def __init__(self, df, p, alpha, SDCols, QICols):
        self.df = df
        self.p = p
        self.alpha = alpha
        self.SDCols = SDCols
        self.QICols = QICols


    def compute_histogram(self):
        histogram = dict()
        for sd in self.SDCols:
            histogram[str(sd)] = self.df[str(sd)]
        return histogram

    def startAlgorithm(self):
        df = pd.DataFrame.hist(self.df, self.SDCols)
        print(df)

