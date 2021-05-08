import matplotlib.pyplot as plt

def plot(df, title):
    shape = df.shape
    plt.title(title)
    plt.ylabel("Transactions")
    plt.xlabel("Items")
    plt.spy(df.values)
    plt.show()

    return
