import numpy as np
import itertools
import math


def KLdivergence(QIvals, SDvals, df, qi, sd, p, count_SD, dfResult, SD_DF):
    # Setup array containing the labels for quasi-identifiers and sensitive datas,
    # in order to eliminate the other columns
    arraySDQI = np.append(QIvals, SDvals)
    for column in df:
        if column not in arraySDQI:
            df.drop(column, axis=1, inplace=True)
    df = df[arraySDQI]

    # Combinations between cells
    iterList = list(itertools.product([False, True], repeat=qi))

    # Array initilization which will contain the values for Act and Est
    Act = []
    Est = []

    # Loop combinations
    for _ in iterList:
        cellCount = 0
        count = 0

        # arrayLabel contains the transactions for the label
        arrayLabel = []

        # groupCell contains the groups who intersect the label
        groupCell = []
        groupDict = dict()

        while count < len(df.index):
            i = 0
            stop = True
            for k in _:

                # from 0 to qi-1 we have the quasi-identifiers
                if i == qi:
                    break
                if df.iloc[count, i] != k:
                    stop = False
                    break
                i += 1
            if stop:
                # from qi to qi+sd-1 we have the sensitive datas
                while i < qi + sd:
                    if df.iloc[count, i]:
                        cellCount += 1
                    i += 1
                label = df.index[count]
                index = dfResult.index.get_loc(label)
                # Index / p retrieve in which group belongs the transaction
                group = "Group" + str(math.floor(index / p))

                if group not in groupCell:
                    groupCell.append(group)
                if group in groupDict:
                    # increase the counter of transactions included in the group label in the histogram
                    # each value of the histogram will be for the label in that group
                    groupDict[group] += 1
                else:
                    # add in the group if doesn't belong to any
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

        # compute Est by sum (a*b)/p computed from each group

        EstC = EstG / count_SD
        Est.append(EstC)
        Act.append(cellCount / count_SD)

        # Remove the cells belonging the transactions from dataframe
        df.drop(arrayLabel, axis=0, inplace=True)

    KLdiv = 0
    if np.array_equal(Act, Est):
        return KLdiv

    for idx, val in enumerate(Act):
        if Act[idx] == 0:
            continue
        KLdiv += (Act[idx] * math.log2(Act[idx] / Est[idx]))

    return KLdiv
