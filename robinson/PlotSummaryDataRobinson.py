import matplotlib.pyplot as plt
import numpy as np

def PlotSummaryDataRobinson(current_time, accepts, discovers, visits, Ants):

    plt.ioff()
    plt.close(1)

    NumNests = visits.shape[0]
    selected = []
    for ant in Ants:
        selected.append(ant['selected'])
    nAnts = len(selected)
    nSelected = selected.count(1)

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, num=2)
    ax1.hist(accepts, bins=[-0.5, 0.5, 1.5, 2.5])
    ax1.set_xlabel('final site')
    ax1.set_ylabel('number of ants')
    ax1.set_title(str(nSelected) + '/' + str(nAnts) + ' selected a site')

    ax2.hist(current_time)
    ax2.set_xlabel('time till final decision')
    ax2.set_ylabel('number of ants')

    discovers[discovers < 0] = 0
    ax3.bar(range(NumNests), np.mean(discovers, 1))
    ax3.set_xlabel('site')
    ax3.set_ylabel('mean site discovery time')

    ax4.bar(range(NumNests), np.mean(visits, 1))
    ax4.set_xlabel('site')
    ax4.set_ylabel('mean # of visits')

    fig.tight_layout()
    plt.show()