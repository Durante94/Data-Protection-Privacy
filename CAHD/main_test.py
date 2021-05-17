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
    p = [4, 6, 8, 10, 14]
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

    dfTimeStart = time.time()
    # Dataframe creation
    create_df = DataFrame(nameFile, size, sd, qi, maxSize)
    original_df, SDcols, QIcols = create_df.df_creation()

    # Plot of the band matrix
    plot(original_df, "Band matrix")
    dfCreationTime = time.time() - dfTimeStart

    exec_time = []
    kl_divergence = []
    for i in range(0, len(p)):
        df = original_df.copy()
        #dimension of the dataset
        # shape = df.shape
        # print("Number of transactions:", shape[0])
        # print("Number of items:", shape[1])

        # Timer start
        start_time = time.time()

        # Start of CAHD algorithm
        cahd = CAHD(df, p[i], alpha, SDcols, QIcols)
        dfResult, dfSD, count, p[i] = cahd.startAlgorithm()

        # Compute the KL divergence
        KL = KLdivergence(QIcols, SDcols, df, qi, sd, p[i], count, dfResult, dfSD)

        # Timer end
        end_time = time.time() - start_time

        print("the execution time for the privacy degree %s is %s seconds" % (p[i], round(end_time, 2)))
        print("KL Divergence:", KL)
        print("---------END OF EXECUTION %s---------" % (i+1))
        exec_time.append(round(end_time, 2))
        kl_divergence.append(KL)

    print(p)
    print(exec_time)
    print(kl_divergence)
    print(round(dfCreationTime, 2))

