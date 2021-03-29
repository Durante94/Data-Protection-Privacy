import pandas as pd
from DataFrame import DataFrame


if __name__ == "__main__":
    #print("dimensioni del dataset:")
    # size = input()
    size = 500
    #print("Grado di Privacy:")
    # p = input()
    p = 10
    #print("numero di item sensibili:")
    # s = input()
    s = 10
    #print("numero di Quasi-Identifier:")
    # qi = input()
    qi = 4
    #print("valore di alpha desiderato (ottimale = 3):")
    # alpha = input()
    alpha = 3

    nameFile = "BMS1_spmf.txt"
    df = DataFrame(nameFile, size, s, qi)

    df.df_creation()



