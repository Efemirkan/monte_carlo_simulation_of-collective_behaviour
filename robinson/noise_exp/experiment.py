import numpy as np
import RobinsonCode as rc  # use your existing RobinsonCode.py


def run_single_experiment(qual_noise, n=27, threshold_mean=5, threshold_stddev=1):
    """
    Run one Robinson simulation for a given level of quality-estimation noise.
    Returns summary metrics + raw data.
    """

    # probabilities of visiting each site from each other
    probs = np.array([
        [0.91, 0.15, 0.03],
        [0.06, 0.80, 0.06],
        [0.03, 0.05, 0.91],
    ])

    # mean time to get between each nest
    time_means = np.array([
        [1, 36, 143],
        [36, 1, 116],
        [143, 116, 1],
    ])
    # standard deviation of time to get between each nest
    time_stddevs = time_means / 5

    # mean quality of each nest. Note home is -infinity so it never gets picked
    quals = np.array([-np.inf, 4, 6])

    # quality-estimation noise (same for all nests here)
    qual_stddev = np.array([qual_noise, qual_noise, qual_noise])

    current_time, discovers, visits, accepts, Ants, *_ = rc.RobinsonCode(
        n,
        quals,
        probs,
        threshold_mean,
        threshold_stddev,
        qual_stddev,
        time_means,
        time_stddevs,
        ToPlot=0,   # IMPORTANT: no per-ant path plotting
        quora=[]
    )

    # best nest index
    best = int(np.argmax(quals))
    selected_flags = np.array([a["selected"] for a in Ants])
    num_selected = selected_flags.sum()
    total_ants = len(Ants)

    decision_times = []
    correct = 0

    for i, ant in enumerate(Ants):
        if ant["selected"] == 1:
            decision_times.append(current_time[i])
            if accepts[i] == best:
                correct += 1

    if num_selected > 0:
        accuracy = correct / num_selected
        mean_time = float(np.mean(decision_times))
    else:
        accuracy = np.nan
        mean_time = np.nan

    return {
        "noise": qual_noise,
        "accuracy": accuracy,
        "selection_rate": num_selected / total_ants,
        "mean_decision_time": mean_time,
        "num_selected": num_selected,
        "total_ants": total_ants,
        "current_time": current_time,
        "discovers": discovers,
        "visits": visits,
        "accepts": accepts,
        "Ants": Ants,
    }


def run_noise_sweep(noise_levels, n=27, threshold_mean=5, threshold_stddev=1):
    results = []
    for noise in noise_levels:
        print(f"Running noise={noise}")
        results.append(
            run_single_experiment(
                qual_noise=noise,
                n=n,
                threshold_mean=threshold_mean,
                threshold_stddev=threshold_stddev,
            )
        )
    return results


if __name__ == "__main__":
    noise_levels = [0.2, 0.5, 1.0, 1.5, 2.0, 3.0]
    results = run_noise_sweep(noise_levels)

    np.savez(
        "noise_sensitivity_results.npz",
        noise=np.array([r["noise"] for r in results]),
        accuracy=np.array([r["accuracy"] for r in results]),
        selection_rate=np.array([r["selection_rate"] for r in results]),
        mean_time=np.array([r["mean_decision_time"] for r in results]),
    )

    from output import export_per_ant_results, export_summary_results

    export_per_ant_results("noise_ant_data.xlsx", results)
    export_summary_results("noise_summary.xlsx", results)
