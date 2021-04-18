import operator

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
        SDindex = df.index.get_loc(tmp[0])
        for i in SDvals:
            if df.iloc[SDindex][i]:
                SD_conflict.append(i)

        # Candidate List (riga 5 pseudocodice)
        CL = []
        # range (riga 5 pseudocodice)
        range = alpha*p
        # Array del gruppo (riga 6 pseudocodice)
        group = []

        # ciclo per i successori di t
        range_count = 0
        SDindex_tmp = SDindex
        while (SDindex_tmp < len(df)-1 and range_count < range):
            SDindex_tmp += 1
            succ_row = df.iloc[SDindex_tmp]
            SD_to_insert = []
            for j in SDvals:
                conflict = False
                # se non è in conflitto ed è sensibile
                if succ_row.get(j):
                    if j not in SD_conflict:
                        SD_to_insert.append(j)
                    else:
                        conflict = True
                        break
            # la riga non contiene dati sensibili in conflitto la aggiungo alla CL
            if not conflict:
                CL.append(succ_row.name)
                range_count += 1
                SD_conflict.extend(SD_to_insert)    # INDIANATA STACK OVERFLOW

        # ciclo per i predecessori di t
        range_count = 0
        SDindex_tmp = SDindex
        while (SDindex_tmp > 0 and range_count < range):
            SDindex_tmp -= 1
            pred_row = df.iloc[SDindex_tmp]
            SD_to_insert = []
            for j in SDvals:
                conflict = False
                # se non è in conflitto ed è sensibile
                if pred_row.get(j):
                    if j not in SD_conflict:
                        SD_to_insert.append(j)
                    else:
                        conflict = True
                        break
            # la riga non contiene dati sensibili in conflitto la aggiungo alla CL
            if not conflict:
                CL.append(pred_row.name)
                range_count += 1
                SD_conflict.extend(SD_to_insert)  # INDIANATA STACK OVERFLOW

        # CL completata, creazione del gruppo
        group.append(tmp[0])
        # riordine della CL in ordine decrescente per QID in comune
        # ovvero: le righe con più QID in comune sono all'inizio
        CLtmp = list()
        for x in CL:
            QIDcount = 0
            for y in QIvals:
                if df.loc[tmp[0]][y] == df.loc[x][y]:
                    QIDcount += 1
            #aggiungo alla tupla il numero di riga accoppiata al num. di QI uguali trovati
            CLtmp.append(tuple((x, QIDcount)))

        #sort della lista in ordine decrescente per numero di QID
        CLtmp_sorted = sorted(CLtmp, key=operator.itemgetter(1), reverse=True)

        remaining = 0 # DEBUG
    return df, SD_DF