import matplotlib.pyplot as plt


def plotBench(exec_time, kl_divergence, p, sd, alpha):
    i = 0
    for a in alpha:
        # kl-divergence vs p
        plt.title("reconstruction error vs p for alpha %s" % a)
        plt.ylabel("KL-Divergence")
        plt.xlabel("p")
        plt.plot(p[i], kl_divergence[i], color='green', marker='o',
                 markerfacecolor='green', label='m=%s' % (sd[0]))
        plt.plot(p[i+1], kl_divergence[i+1], color='red', marker='o',
                 markerfacecolor='red', label='m=%s' % (sd[1]))
        plt.legend(loc="upper left")
        plt.show()

        # execution time
        plt.title("execution time for alpha %s" % a)
        plt.ylabel("times (sec)")
        plt.xlabel("p")
        plt.plot(p[i], exec_time[i], color='green', marker='o',
                 markerfacecolor='green', label='m=%s' % (sd[0]))
        plt.plot(p[i+1], exec_time[i+1], color='red', marker='o',
                 markerfacecolor='red', label='m=%s' % (sd[1]))
        plt.legend(loc="upper left")
        plt.show()

        i += 1

    return
