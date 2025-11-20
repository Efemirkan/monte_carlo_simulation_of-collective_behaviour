from openpyxl import Workbook


def export_per_ant_results(filename, results):
    wb = Workbook()
    ws = wb.active
    ws.title = "Ant-Level"

    example = results[0]
    NumNests = example["visits"].shape[0]

    # Headings
    headings = [
        "noise", "ant_index", "threshold", "final_site",
        "selected_flag", "decision_time"
    ]

    for i in range(NumNests):
        headings.append(f"discover_site_{i}")

    for i in range(NumNests):
        headings.append(f"visits_site_{i}")

    headings.append("path")

    ws.append(headings)

    # Data rows
    for res in results:
        noise = res["noise"]
        Ants = res["Ants"]
        accepts = res["accepts"]
        current_time = res["current_time"]
        discovers = res["discovers"]
        visits = res["visits"]

        for i, ant in enumerate(Ants):
            row = [
                noise,
                i,
                ant["thresh"],
                accepts[i],
                ant["selected"],
                current_time[i],
            ]
            row.extend(list(discovers[:, i]))
            row.extend(list(visits[:, i]))
            row.append(str(ant["path"]))
            ws.append(row)

    wb.save(filename)
    print(f"Saved: {filename}")


def export_summary_results(filename, results):
    wb = Workbook()
    ws = wb.active
    ws.title = "Summary"

    ws.append([
        "noise", "accuracy", "selection_rate",
        "mean_decision_time", "num_selected", "total_ants"
    ])

    for r in results:
        ws.append([
            r["noise"],
            r["accuracy"],
            r["selection_rate"],
            r["mean_decision_time"],
            r["num_selected"],
            r["total_ants"],
        ])

    wb.save(filename)
    print(f"Saved: {filename}")
