import operator
import copy
import pandas as pd


def make_group(df, SDvals, QIvals, p, alpha, hist, size, remaining):
    # dichiariamo il dataframe raggruppato
    dfResult = pd.DataFrame()

    # array di gruppi di SD per ognuno dei gruppi creati
    sdResult = []

    # nuovo istogramma creato con deepcopy

    new_hist = dict()

    rollbackCount = 0

    # costruisco dataframe di soli SD
    SD_DF = pd.DataFrame(columns=SDvals)

    # cerco il primo SD
    SDfound = False
    tmp = 0
    i = 0
    while i < size and not SDfound:
        for j in SDvals:
            if df.iloc[i][j]:
                SDfound = True
                # recupero l'indice di riga della prima occorrenza di un SD
                tmp = df.iloc[[i]].index
                break
        i += 1

    while remaining > p:
        # SD già in t con cui non devo andare in conflitto
        SD_conflict = []
        # recupero il numero  di riga dentro il df corrispondente a tmp
        SDindex = df.index.get_loc(tmp[0])
        for i in SDvals:
            if df.iloc[SDindex][i]:
                SD_conflict.append(i)

        # Candidate List (riga 5 pseudocodice)
        CL = []
        # range (riga 5 pseudocodice)
        range = alpha * p
        # Array del gruppo (riga 6 pseudocodice), righe del dataframe che
        # anonimizziamo
        group = []
        conflict = False

        # ciclo per i successori di t
        range_count = 0
        SDindex_tmp = SDindex
        while SDindex_tmp < len(df) - 1 and range_count < range:
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
            # la riga non contiene dati sensibili in conflitto la aggiungo alla
            # CL
            if not conflict:
                CL.append(succ_row.name)
                range_count += 1
                SD_conflict.extend(SD_to_insert)  # INDIANATA STACK OVERFLOW

        # ciclo per i predecessori di t
        range_count = 0
        SDindex_tmp = SDindex
        while SDindex_tmp > 0 and range_count < range:
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
            # aggiungo alla tupla il numero di riga accoppiata al numero  di QI uguali trovati
            CLtmp.append(tuple((x, QIDcount)))

        # sort della lista in ordine decrescente per numero di QID
        CLtmp_sorted = sorted(CLtmp, key=operator.itemgetter(1), reverse=True)

        # Punto 7 pseudocodice

        count = 0
        # nuovo istogramma
        new_hist = copy.deepcopy(hist)
        group_SD = []
        for j in SDvals:
            if df.loc[tmp[0]][j]:
                new_hist[j] -= 1
                group_SD.append(j)
        while count < p - 1:
            CL_item = CLtmp_sorted.pop(0)
            for j in SDvals:
                if df.loc[CL_item[0]][j]:
                    new_hist[j] -= 1
                    group_SD.append(j)
            group.append(CL_item[0])
            count += 1

        test = True
        remaining -= len(group)
        for _ in SDvals:
            if new_hist[_] * p > remaining:
                remaining += len(group)
                group = []
                test = False
                break

        if test:
            # test passato
            # dfResult.append(df.loc[group, :])
            dfResult = dfResult.append(df.loc[group, :])

            # cerco il prossimo SD
            SDfound = False
            i = SDindex
            while i < len(df) and not SDfound:
                for j in SDvals:
                    if df.iloc[i][j] and df.iloc[[i]].index not in group:
                        SDfound = True
                        # recupero l'indice di riga della prima occorrenza di un SD
                        tmp = df.iloc[[i]].index
                        break
                i += 1

            df = df.drop(group)
            hist = copy.deepcopy(new_hist)
            sdResult.append(group_SD)

            # se non ce ne sono più sensibili esco perchè devo solo scaricare in gruppi i rimanenti
            if not SDfound:
                # dfResult.append(df)
                dfResult = dfResult.append(df)
                df = df.iloc[0:0]
                break
        else:
            rollbackCount += 1
            i = SDindex
            SDfound = False
            while i < len(df) - 1 and not SDfound:
                i += 1
                for _ in SDvals:
                    if df.iloc[i][_]:
                        SDfound = True
                        tmp = df.iloc[[i]].index
                        break

            if not SDfound:
                i = -1
                while i < SDindex and not SDfound:
                    i += 1
                    for _ in SDvals:
                        if df.iloc[i][_]:
                            SDfound = True
                            tmp = df.iloc[[i]].index
                            break

    print("Dimension of df", len(df))

    if not df.empty:

        # We still have some rows in the dataframe, we have collected less than p
        k = 0
        group_SD = []
        while k < len(df):
            for _ in SDvals:
                if df.iloc[k][_]:
                    new_hist[_] -= 1
                    group_SD.append(_)
            k += 1

        Ok = True
        for sdIdx in new_hist:
            if new_hist[sdIdx] != 0:
                Ok = False

        if Ok:
            print("Algorithm result correct")
        else:
            print("Error: there are some SD left")
            return -1, -1

        # dfResult.append(df)
        dfResult = dfResult.append(df)
        df = df.iloc[0:0]

        if group_SD:
            print("We have still some SD: ", group_SD)
            sdResult.append(group_SD)
        else:
            print("We don't have SD anymore: ", group_SD)

    # Now that we have the final dataframe, organized by groups,
    # we delete the columns from the sensitive datas
    for j in SDvals:
        dfResult.drop(j, axis=1, inplace=True)

    groupNumber = size / p
    countGroup = -1
    for x in sdResult:
        countGroup += 1
        for y in x:
            nameGroup = "Group" + str(countGroup)
            SD_DF.loc[nameGroup] = False
            SD_DF.loc[nameGroup][y] = True
    remainingGroups = groupNumber - len(sdResult)
    while remainingGroups > 0:
        # Now remain only the groups without sensitive transactions
        remainingGroups -= 1
        countGroup += 1
        nameGroup = "Group" + str(countGroup)
        SD_DF.loc[nameGroup] = False

    return dfResult, SD_DF
