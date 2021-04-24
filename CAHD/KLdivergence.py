import numpy as np
import itertools
import math


def KLdivergence(QIvals, SDvals, df, qi, sd, p, count_SD, dfResult, SD_DF):
    # Preparazione array contenente le label di QI e SD da usare per eliminare tutte le altre colonne
    arraySDQI = np.append(QIvals, SDvals)
    for column in df:
        if column not in arraySDQI:
            df.drop(column, axis=1, inplace=True)
    df = df[arraySDQI]

    # Combinazioni per celle
    iterList = list(itertools.product([False, True], repeat=qi))

    # Inizializzo array per contenere i valori di Act ed Est per ogni cella
    Act = []
    Est = []

    # Ciclo sulle combinazioni
    for _ in iterList:
        cellCount = 0
        count = 0

        # arrayLabel contiene le transazioni appartenenenti alla cella ?
        arrayLabel = []

        # groupCell array dei gruppi che intersecano la cella
        groupCell = []
        groupDict = dict()

        while count < len(df.index):
            i = 0
            stop = True
            for k in _:

                # Fino a qi-1 ho i QI
                if i == qi:
                    break
                if df.iloc[count, i] != k:
                    stop = False
                    break
                i += 1
            if stop:
                # Da QI a QI+SD-1 ho gli SD
                while i < qi + sd:
                    if df.iloc[count, i]:
                        cellCount += 1
                    i += 1
                label = df.index[count]
                index = dfResult.index.get_loc(label)
                # Index / p fornisce il gruppo di appartenenenza della transazione
                group = "Group" + str(math.floor(index / p))

                if group not in groupCell:
                    groupCell.append(group)
                if group in groupDict:
                    # Aumenta in un istogramma il contatore di transazione comprese nella cella per quel tale gruppo (per b)
                    # ogni valore dell'istogramma sarà il valore di b per quel gruppo
                    groupDict[group] += 1
                else:
                    # Se non avevo già aggiunto quel gruppo
                    groupDict[group] = 1
                arrayLabel.append(df.index[count])
            count += 1
        EstC = 0
        EstG = 0

        for x in groupCell:
            b = groupDict[x]
            a = 0
            for y in SDvals:
                if SD_DF.loc[x, y]:
                    a += 1
            EstG += (a * b) / p

        # Calcolo Est sommando i (a*b)/p che ottengo da ogni gruppo

        EstC = EstG / count_SD
        Est.append(EstC)
        Act.append(cellCount / count_SD)

        # Rimuovo dal df le transazioni che facevano parte della cella prima di partire
        # con l'iterazione per cella successiva
        df.drop(arrayLabel, axis=0, inplace=True)

    KLdiv = 0
    if np.array_equal(Act, Est):
        return KLdiv

    for idx, val in enumerate(Act):
        if Act[idx] == 0:
            continue
        KLdiv += (Act[idx] * math.log2(Act[idx] / Est[idx]))

    return KLdiv
