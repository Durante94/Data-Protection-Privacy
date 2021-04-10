from DataFrame import DataFrame
from CAHD import CAHD
from Plot import plot

if __name__ == "__main__":
    # print("numero di item:")
    # size = input()
    size = 150
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

    create_df = DataFrame(nameFile, size, sd, qi)
    df, SDcols, QIcols = create_df.df_creation()

    # STAMPA DEL NUMERO DI TRANSAZIONI E ITEM TOTALI CONTENUTI NELLA BAND MATRIX
    shape = df.shape
    print("numero di transazioni:", shape[0])  # Righe
    print("numero di items:", shape[1])  # Colonne

    # PLOT DELLA BAND MATRIX
    plot(df, "BAND MATRIX")

    # PRINT DEGLI SD E QI
    print("numero di sensitive data:", sd)
    print("sensitive data:", SDcols)
    print("numero di Quasi Identifier:", qi)
    print("quasi identifier:", QIcols)

    cahd = CAHD(df, p, alpha, SDcols, QIcols)
    cahd.startAlgorithm()
