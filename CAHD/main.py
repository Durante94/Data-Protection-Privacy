import warnings
from KLdivergence import KLdivergence
from DataFrame import DataFrame
from CAHD import CAHD
from Plot import plot
import time

warnings.filterwarnings("ignore")

if __name__ == "__main__":
    # print("numero di item:")
    # size = input()
    size = 1000
    # print("Grado di Privacy:")
    # p = input()
    p = 10
    # print("numero di item sensibili:")
    # sd = input()
    sd = 10
    # print("numero di Quasi-Identifier:")
    # qi = input()
    qi = 4
    # print("valore di alpha desiderato (ottimale = 3):")
    # alpha = input()
    alpha = 3

    nameFile = None
    dsSelect = 0
    while dsSelect != 1 and dsSelect != 2:
        print("which dataset do you want to execute? 1 or 2?")
        dsSelect = int(input())
    if dsSelect == 1:
        maxSize = 497
        nameFile = "dataset/BMS1_spmf.txt"
    elif dsSelect == 2:
        maxSize = 3340
        nameFile = "dataset/BMS2.txt"

    # Timer start
    start_time = time.time()

    # Dataframe creation
    create_df = DataFrame(nameFile, size, sd, qi, maxSize)
    df, SDcols, QIcols = create_df.df_creation()
    # Plot of the band matrix

    # Print of number of transactions and total items contained in the band matrix
    shape = df.shape
    print("Number of transactions:", shape[0])  # Righe
    print("Number of items:", shape[1])  # Colonne

    # Plot of the band matrix
    plot(df, "Band matrix")

    # Print of sensitive datas and quasi-identifiers
    print("Number of sensitive datas:", sd)
    print("Sensitive data:", SDcols)
    print("Number of Quasi Identifiers:", qi)
    print("Quasi identifier:", QIcols)

    # Start of CAHD algorithm
    cahd = CAHD(df, p, alpha, SDcols, QIcols)
    dfResult, dfSD, count, p = cahd.startAlgorithm()

    # Compute the KL divergence

    KL = KLdivergence(QIcols, SDcols, df, qi, sd, p, count, dfResult, dfSD)

    # Timer end
    end_time = time.time() - start_time

    print("the execution time for the privacy degree %s is %s seconds" % (p, round(end_time, 2)))
    print("KL Divergence:", KL)
