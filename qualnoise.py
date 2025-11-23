import numpy as np
import PlotSummaryDataRobinson as psdr
import OutputRobinsonDataExcel as orde
import RobinsonCode as rc
import os
import matplotlib.pyplot as plt


def main():
    # Fodlers
    plot_dir = "plots"
    data_dir = "data"
    os.makedirs(plot_dir, exist_ok=True)
    os.makedirs(data_dir, exist_ok=True)

    # Noise values
    qual_noise = [0.0001, 1, 5, 10, 20]

    for noise in qual_noise:
        noise_tag = str(noise).replace(".", "_") # to prevent file extension complication
        excel_path = os.path.join(data_dir, f"Robinson_noise_{noise_tag}.xlsx")
        plot_path = os.path.join(plot_dir, f"noise_{noise_tag}.png")

        
        run_robinson(qual_val=noise, n=200, threshold_mean=5, threshold_stddev=0.1,
            output_file_xls=excel_path, plot_path=plot_path)


def run_robinson(qual_val, n=200, threshold_mean=5, threshold_stddev=0.1, 
                 output_file_xls="RobinsonTestExperimentTest1.xlsx", plot_path="plots"):

    # probabilities of visiting each site from each other
    probs = np.array([
        [0.91, 0.15, 0.03],
        [0.06, 0.80, 0.06],
        [0.03, 0.05, 0.91],
    ])

    # mean time to get between each nest
    time_means = np.array([
        [1,   36, 143],
        [36,   1, 116],
        [143, 116, 1],
    ])

    # standard deviation of time to get between each nest
    time_stddevs = time_means / 5

    # mean quality of each nest. Note home is -infinity so it never gets picked
    quals = np.array([-np.inf, 4, 6])

    # standard deviation of quality for each nest
    qual_stddev = np.array([qual_val, qual_val, qual_val])

    # run simulation
    (
        current_time,
        discovers,
        visits,
        accepts,
        Ants,
        rnd_seed,
        preqtimes,
        preqdiscovers,
        preqvisits,
        preqaccepts,
    ) = rc.RobinsonCode(
        n,
        quals,
        probs,
        threshold_mean,
        threshold_stddev,
        qual_stddev,
        time_means,
        time_stddevs,
        [],
        [],
    )

    # Save the data    
    orde.OutputRobinsonDataExcel(
        output_file_xls, Ants, current_time, accepts, discovers, visits
    )

    
    # Create the figure
    psdr.PlotSummaryDataRobinson(current_time, accepts, discovers, visits, Ants)

    # Save the figure
    plt.savefig(plot_path, dpi=300, bbox_inches="tight")
    plt.close() 


if __name__ == "__main__":
    main()
