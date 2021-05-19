import matplotlib.pyplot as plt


def plotBench(exec_time, kl_divergence,p):
    # kl-divergence vs p
    plt.title("reconstruction error vs p")
    plt.ylabel("KL-Divergence")
    plt.xlabel("p")
    plt.plot(p, kl_divergence,color='green', marker='o', markerfacecolor='red')
    plt.show()

    # execution time
    plt.title("execution time")
    plt.ylabel("times (sec)")
    plt.xlabel("p")
    plt.plot(p, exec_time, color='green', marker='o', markerfacecolor='red')
    plt.show()

    return