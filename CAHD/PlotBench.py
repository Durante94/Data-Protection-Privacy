import matplotlib.pyplot as plt


def plotBench(exec_time, kl_divergence, p, sd):
    # kl-divergence vs p
    plt.title("reconstruction error vs p")
    plt.ylabel("KL-Divergence")
    plt.xlabel("p")
    plt.plot(p[0], kl_divergence[0], color='green', marker='o', markerfacecolor='green', label='m=%s' % (sd[0]))
    plt.plot(p[1], kl_divergence[1], color='red', marker='o', markerfacecolor='red', label='m=%s' % (sd[1]))
    plt.legend(loc="upper left")
    plt.show()

    # execution time
    plt.title("execution time")
    plt.ylabel("times (sec)")
    plt.xlabel("p")
    plt.plot(p[0], exec_time[0], color='green', marker='o', markerfacecolor='green', label='m=%s' % (sd[0]))
    plt.plot(p[1], exec_time[1], color='red', marker='o', markerfacecolor='red', label='m=%s' % (sd[1]))
    plt.legend(loc="upper left")
    plt.show()

    return
