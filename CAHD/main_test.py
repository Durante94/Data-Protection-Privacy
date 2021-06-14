import warnings
from KLdivergence import KLdivergence
from DataFrame import DataFrame
from CAHD import CAHD
from Plot import plot
from PlotBench import plotBench
import time

warnings.filterwarnings("ignore")

if __name__ == "__main__":
    # numero di item
    size = 1000
    # Grado di Privacy
    p = [4, 6, 8, 10, 12, 14, 16, 18, 20]
    # numero di item sensibili
    sd = [10, 20]
    # numero di Quasi-Identifier
    qi = 5
    # valore di alpha desiderato (ottimale = 3)
    alpha = 3

    nameFile = None
    dsSelect = 0
    while dsSelect != 1 and dsSelect != 2:
        print("Which dataset do you want to execute? 1 or 2?")
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

    # debug: print of SDcols and QIcols
    # print("SDcols:",SDcols)
    # print("QIcols:",QIcols)

    total_exec_time = []
    total_kl_divergence = []
    total_p_satisfied = []
    for _ in range(0, len(sd)):
        # print("SDcols:", SDcols[_])
        # print("QIcols:", QIcols[_])
        print("--------------STARTING WITH %s SENSITIVE DATA--------------" % sd[_])
        exec_time = []
        kl_divergence = []
        p_satisfied = p
        for i in range(0, len(p)):
            df = original_df.copy()

            # Timer start
            start_time = time.time()

            # Start of CAHD algorithm
            cahd = CAHD(df, p_satisfied[i], alpha, SDcols[_], QIcols[_])
            dfResult, dfSD, count, p_satisfied[i] = cahd.startAlgorithm()

            # Compute the KL divergence
            KL = KLdivergence(QIcols[_], SDcols[_], df, qi, sd[_], p_satisfied[i], count, dfResult, dfSD)

            # Timer end
            end_time = time.time() - start_time

            print("The execution time for the privacy degree %s is %s seconds" % (p_satisfied[i], round(end_time, 2)))
            print("KL Divergence:", KL)
            print("---------END OF EXECUTION %s---------" % (i+1))
            exec_time.append(round(end_time, 2))
            kl_divergence.append(KL)
        total_exec_time.append(exec_time)
        total_kl_divergence.append(kl_divergence)
        total_p_satisfied.append(p_satisfied)

    # print("privacy degrees satisfied:", total_p_satisfied)
    # print("execution times:", total_exec_time)
    # print("kl-divergence:", total_kl_divergence)
    # print("dataframe creation time:", round(dfCreationTime, 2))
    plotBench(total_exec_time, total_kl_divergence, total_p_satisfied, sd)

