from DataFrame import DataFrame
from CAHD import CAHD

if __name__ == "__main__":
    # print("numero di item:")
    # size = input()
    size = 150
    # print("Grado di Privacy:")
    # p = input()
    p = 10
    # print("numero di item sensibili:")
    # s = input()
    s = 10
    # print("numero di Quasi-Identifier:")
    # qi = input()
    qi = 4
    # print("valore di alpha desiderato (ottimale = 3):")
    # alpha = input()
    alpha = 3

    nameFile = "BMS1_spmf.txt"

    df = DataFrame(nameFile, size, s, qi)
    df.df_creation()
    # cahd = CAHD(df.df, p, alpha, df.SDcols, df.QIcols)
    # cahd.compute_histogram()

    print('porcoddio')