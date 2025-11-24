import numpy as np
import PlotSummaryDataRobinson as psdr
import OutputRobinsonDataExcel as orde
import RobinsonCode as rc
import os
import matplotlib.pyplot as plt

def main():
    # Folders for output
    plot_dir = "plots"
    data_dir = "data"
    os.makedirs(plot_dir, exist_ok=True)
    os.makedirs(data_dir, exist_ok=True)

    # Noise values to test
    qual_noise = [0.0001, 1, 5, 10, 20]

    # Threshold stddev values to test
    threshold_stddev_vals = [0.05, 0.1, 0.2]

    for th in threshold_stddev_vals:
        th_tag = str(th).replace(".", "_")

        for noise in qual_noise:
            noise_tag = str(noise).replace(".", "_")

            # File names now encode BOTH noise and threshold
            excel_path = os.path.join(
                data_dir,
                f"Robinson_noise_{noise_tag}_th_{th_tag}.xlsx"
            )
            plot_path = os.path.join(
                plot_dir,
                f"noise_{noise_tag}_th_{th_tag}.png"
            )

            print(f"\n=== Running experiment for noise = {noise}, "
                  f"threshold_stddev = {th} ===")

            run_robinson(
                qual_val=noise,
                n=200,
                threshold_mean=5,
                threshold_stddev=th,
                output_file_xls=excel_path,
                plot_path=plot_path,
            )

def run_robinson(
    qual_val=1,
    n=200,
    threshold_mean=5,
    threshold_stddev=0.1,
    output_file_xls="RobinsonTestExperimentTest1.xlsx",
    plot_path="plots",
):
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

    # Save data
    exc_data = orde.OutputRobinsonDataExcel(
        output_file_xls, Ants, current_time, accepts, discovers, visits
    )

    # Create plot summary
    psdr.PlotSummaryDataRobinson(current_time, accepts, discovers, visits, Ants)

    # Save the plots
    plt.savefig(plot_path, dpi=300, bbox_inches="tight")
    plt.close() 


if __name__ == "__main__":
    main()
