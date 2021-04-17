import pandas as pd

def make_group (df, SDvals, QIvals, p, alpha, hist, size, remaining):

    # costruisco dataframe di soli SD
    SD_DF = pd.DataFrame(columns=SDvals)

    # cerco il primo SD
    SDfound = False
    tmp = 0
    i = 0
    while i<size and not SDfound:
        for j in SDvals:
            if df.iloc[i][j]:
                SDfound = True
                # recupero l'indice di riga della prima occorrenza di un SD
                tmp = df.iloc[[i]].index
                break
        i +=1

    while(remaining>p):
        # SD già in t con cui non devo andare in conflitto
        SD_conflict = []
        # recupero il num. di riga dentro il df corrispondente a tmp
        k = df.index.get_loc(tmp[0])
        for i in SDvals:
            if df.iloc[k][i]:
                SD_conflict.append(j)

        # Candidate List (riga 5 pseudocodice)
        CL = []
        # range (riga 5 pseudocodice)
        range = alpha*p
        # Array del gruppo (riga 6 pseudocodice)

        remaining = 0
    return df, SD_DF