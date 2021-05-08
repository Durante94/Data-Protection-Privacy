import warnings
from KLdivergence import KLdivergence
from DataFrame import DataFrame
from CAHD import CAHD
from Plot import plot

warnings.filterwarnings("ignore")

if __name__ == "__main__":
    # print("numero di item:")
    # size = input()
    size = 200
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

    nameFile = "BMS1_spmf.txt"

    # Dataframe creation
    create_df = DataFrame(nameFile, size, sd, qi)
    df, SDcols, QIcols = create_df.df_creation()

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
    dfResult, dfSD, count = cahd.startAlgorithm()

    # Compute the KL divergence

    KL = KLdivergence(QIcols, SDcols, df, qi, sd, p, count, dfResult, dfSD)

    print("KL Divergence:", KL)
