import matplotlib.pyplot as plt

def PlotAntPath(Ant, perceivedQuality=None):

    t = Ant['t']
    path = Ant['path']
    NumSteps = len(path)

    plt.figure(1).clear()

    fig, (ax1, ax2) = plt.subplots(2, 1, num=1)

    plt.ion()
    plt.show()

    ax1.plot(path, 'r-o') # we can let the x variable be created automatically in this case
    ax1.plot(NumSteps-1, path[-1], 'b*', markersize=12)
    ax1.set_xlabel('steps')
    ax1.set_ylabel('site')
    ax1.set_ylim([-0.2, 2.2])

    if perceivedQuality:
        qstr = ', Perceived quality = ' + str("%.3f" % round(perceivedQuality,3))
    else:
        qstr = ''

    if Ant['selected'] == 1:
        tstr = qstr + ': SELECTED'
    else:
        tstr = qstr + ': NOT SELECTED'

    ax1.set_title('ant path, threshold=' + str("%.3f" % round(Ant['thresh'],3)) +
                  ', step=' + str(NumSteps) + tstr, loc='center', wrap=True)

    ax2.plot(t, path, 'r-o')
    ax2.plot(t[-1], path[-1], 'b*', markersize=14)
    ax2.set_xlabel('time (s)')
    ax2.set_ylabel('site')
    ax2.set_title('ant path, threshold=' + str("%.3f" % round(Ant['thresh'], 3)) + ', time=' +
                  str("%.3f" % round(t[-1], 3)) + tstr, loc='center', wrap=True)
    ax2.set_ylim([-0.2, 2.2])

    fig.tight_layout()

    plt.draw()
    plt.pause(0.1)
    # fig.clf()
