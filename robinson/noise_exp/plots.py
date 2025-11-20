import matplotlib.pyplot as plt
import numpy as np


def PlotAntPath(Ant, perceivedQuality=None):

    t = Ant['t']
    path = Ant['path']
    NumSteps = len(path)

    plt.figure(1).clear()
    fig, (ax1, ax2) = plt.subplots(2, 1, num=1)

    plt.ion()
    plt.show()

    # --- Top: Path vs Steps ---
    ax1.plot(path, 'r-o')
    ax1.plot(NumSteps - 1, path[-1], 'b*', markersize=12)
    ax1.set_xlabel('steps')
    ax1.set_ylabel('site')
    ax1.set_ylim([-0.2, 2.2])

    if perceivedQuality is not None:
        qstr = ', Perceived quality=' + str("%.3f" % round(perceivedQuality, 3))
    else:
        qstr = ''

    status = 'SELECTED' if Ant['selected'] == 1 else 'NOT SELECTED'

    ax1.set_title(
        f'ant path, threshold={Ant["thresh"]:.3f}, step={NumSteps}{qstr}: {status}',
        wrap=True,
        loc='center'
    )

    # --- Bottom: Path vs Time ---
    ax2.plot(t, path, 'r-o')
    ax2.plot(t[-1], path[-1], 'b*', markersize=14)
    ax2.set_xlabel('time (s)')
    ax2.set_ylabel('site')
    ax2.set_ylim([-0.2, 2.2])
    ax2.set_title(
        f'ant path, threshold={Ant["thresh"]:.3f}, time={t[-1]:.3f}: {status}',
        wrap=True,
        loc='center'
    )

    fig.tight_layout()
    plt.draw()
    plt.pause(0.1)



def PlotSummaryDataRobinson(current_time, accepts, discovers, visits, Ants):

    plt.ioff()
    plt.close(1)

    NumNests = visits.shape[0]
    selected = [ant['selected'] for ant in Ants]
    # plots.py
    # Combined plotting utilities:
    # - Single-run plots (paths + summary)
    # - Noise-sweep plots (accuracy, decision time, selection rate)

    import numpy as np
    import matplotlib.pyplot as plt

    # ================================================================
    # 1. Single ant path plot
    # ================================================================
    def PlotAntPath(Ant, perceivedQuality=None):
        """
        Plot the path of a single ant over steps and over time.
        """

        t = Ant["t"]
        path = Ant["path"]
        NumSteps = len(path)

        fig, (ax1, ax2) = plt.subplots(2, 1)

        # --- Path vs Steps ---
        ax1.plot(path, "r-o")
        ax1.plot(NumSteps - 1, path[-1], "b*", markersize=12)
        ax1.set_xlabel("steps")
        ax1.set_ylabel("site")
        ax1.set_ylim([-0.2, 2.2])

        qstr = f", Perceived={perceivedQuality:.3f}" if perceivedQuality is not None else ""
        status = "SELECTED" if Ant["selected"] == 1 else "NOT SELECTED"

        ax1.set_title(
            f"Ant path, threshold={Ant['thresh']:.3f}, step={NumSteps}{qstr}: {status}",
            wrap=True,
        )

        # --- Path vs Time ---
        ax2.plot(t, path, "r-o")
        ax2.plot(t[-1], path[-1], "b*", markersize=14)
        ax2.set_xlabel("time (s)")
        ax2.set_ylabel("site")
        ax2.set_ylim([-0.2, 2.2])
        ax2.set_title(
            f"Ant path, threshold={Ant['thresh']:.3f}, time={t[-1]:.3f}: {status}",
            wrap=True,
        )

        fig.tight_layout()
        plt.show()

    # ================================================================
    # 2. Summary visualisation (single run)
    # ================================================================
    def PlotSummaryDataRobinson(current_time, accepts, discovers, visits, Ants):
        """
        Summary plots for a single simulation run:
        - final site choices
        - decision times
        - mean discovery times
        - mean visit counts
        """

        NumNests = visits.shape[0]
        selected = [ant["selected"] for ant in Ants]
        nAnts = len(selected)
        nSelected = selected.count(1)

        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)

        # Final sites
        ax1.hist(accepts, bins=[-0.5, 0.5, 1.5, 2.5])
        ax1.set_xlabel("final site")
        ax1.set_ylabel("number of ants")
        ax1.set_title(f"{nSelected}/{nAnts} selected a site")

        # Decision times
        ax2.hist(current_time)
        ax2.set_xlabel("time (s)")
        ax2.set_ylabel("count")

        # Discovery time
        d = discovers.copy()
        d[d < 0] = 0
        ax3.bar(range(NumNests), np.mean(d, axis=1))
        ax3.set_xlabel("site")
        ax3.set_ylabel("mean discovery time")

        # Visits
        ax4.bar(range(NumNests), np.mean(visits, axis=1))
        ax4.set_xlabel("site")
        ax4.set_ylabel("# visits")

        fig.tight_layout()
        plt.show()

    # ================================================================
    # 3. Sweep-level plots (noise vs metrics)
    # ================================================================
    def PlotNoiseSweep(noise, accuracy, selection_rate, mean_time):
        """
        Plot high-level sweep plots for noise-sensitivity analysis:
        - Accuracy vs noise
        - Mean decision time vs noise
        - Selection rate vs noise
        """

        # Accuracy vs Noise
        plt.figure()
        plt.plot(noise, accuracy, marker="o")
        plt.xlabel("Quality-estimation noise (std dev)")
        plt.ylabel("Accuracy (proportion choosing best nest)")
        plt.title("Noise vs Accuracy")
        plt.grid(True)

        # Decision time vs Noise
        plt.figure()
        plt.plot(noise, mean_time, marker="s")
        plt.xlabel("Quality-estimation noise (std dev)")
        plt.ylabel("Mean decision time")
        plt.title("Noise vs Decision Time")
        plt.grid(True)

        # Selection rate vs Noise
        plt.figure()
        plt.plot(noise, selection_rate, marker="^")
        plt.xlabel("Quality-estimation noise (std dev)")
        plt.ylabel("Selection Rate (decision likelihood)")
        plt.title("Noise vs Selection Rate")
        plt.grid(True)

        plt.show()

    nAnts = len(selected)
    nSelected = selected.count(1)

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, num=2)

    # Final site choices
    ax1.hist(accepts, bins=[-0.5, 0.5, 1.5, 2.5])
    ax1.set_xlabel('final site')
    ax1.set_ylabel('number of ants')
    ax1.set_title(f'{nSelected}/{nAnts} ants selected a site')

    # Decision time
    ax2.hist(current_time)
    ax2.set_xlabel('decision time')
    ax2.set_ylabel('count')

    # Mean discovery time
    d = discovers.copy()
    d[d < 0] = 0
    ax3.bar(range(NumNests), np.mean(d, axis=1))
    ax3.set_xlabel('site')
    ax3.set_ylabel('mean discovery time')

    # Mean visits
    ax4.bar(range(NumNests), np.mean(visits, axis=1))
    ax4.set_xlabel('site')
    ax4.set_ylabel('# visits')

    fig.tight_layout()
    plt.show()
