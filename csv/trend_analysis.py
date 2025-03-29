import sys
import csv
import argparse
import shutil
import os
from collections import defaultdict
from datetime import datetime

# Parse arguments
parser = argparse.ArgumentParser(description="Detect recurring spikes in historical data.")
parser.add_argument("csv_file", help="Path to the input CSV file")
parser.add_argument("percent_threshold", type=float, help="Percentage threshold for spikes (e.g., 5 for 5 percent)")
parser.add_argument("min_occurrence_ratio", type=float, help="Minimum ratio (0 to 1) of years in which spike must appear, e.g. 0.9 for 90 percent")
args = parser.parse_args()

# Clean up old outputs
if os.path.exists("spike_results.csv"):
    os.remove("spike_results.csv")

if os.path.exists("spike_reports"):
    shutil.rmtree("spike_reports")
os.makedirs("spike_reports", exist_ok=True)

# Load data
data = []
with open(args.csv_file, newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        if len(row) != 2:
            continue
        try:
            dt = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
            value = float(row[1])
            data.append((dt, value))
        except:
            continue

data.sort()

# Organize data by year
data_by_year = defaultdict(list)
for dt, val in data:
    data_by_year[dt.year].append((dt, val))

# Prepare spike registry
spike_registry = defaultdict(lambda: {"years": set(), "pct_changes": [], "details": {}})
years = sorted(data_by_year.keys())
window_sizes = list(range(4, 32))  # 1 to 31 days max

# Output file setup
out_file = open("spike_results.csv", "w", newline='')
writer = csv.writer(out_file)
writer.writerow([
    "Report ID", "Month", "Start Day", "Window Size (Days)", "Years Found",
    "Occurrence Ratio", "Avg % Change"
])
out_file.flush()

# Progress tracking
total_steps = len(window_sizes)
completed_steps = 0
report_id = 0

# Analyze spikes
for window_size in window_sizes:
    for year in years:
        year_data = data_by_year[year]
        for i in range(len(year_data) - window_size):
            start_dt, start_val = year_data[i]
            end_dt, end_val = year_data[i + window_size]
            pct_change = ((end_val - start_val) / start_val) * 100

            if pct_change >= args.percent_threshold:
                spike_id = (start_dt.month, start_dt.day, window_size)
                registry = spike_registry[spike_id]
                registry["years"].add(year)
                registry["pct_changes"].append(pct_change)
                registry["details"][year] = {
                    "start_date": start_dt.strftime("%Y-%m-%d"),
                    "end_date": end_dt.strftime("%Y-%m-%d"),
                    "start_val": round(start_val, 2),
                    "end_val": round(end_val, 2),
                    "pct_change": round(pct_change, 2)
                }

    # Check and write results for each spike
    for (month, day, win), spike_data in list(spike_registry.items()):
        year_set = spike_data["years"]
        ratio = len(year_set) / len(years)
        if ratio >= args.min_occurrence_ratio:
            avg_pct = sum(spike_data["pct_changes"]) / len(spike_data["pct_changes"])
            report_id += 1
            report_filename = f"spike_reports/report_{report_id}.txt"
            with open(report_filename, "w") as rf:
                for y in sorted(year_set):
                    d = spike_data["details"][y]
                    rf.write(f"Year: {y} | {d['start_date']} ({d['start_val']}) -> {d['end_date']} ({d['end_val']}) | Change: {d['pct_change']}%\n")

            writer.writerow([
                report_id, month, day, win, ", ".join(map(str, sorted(year_set))),
                f"{ratio:.2f}", f"{avg_pct:.2f}%"
            ])
            out_file.flush()
            del spike_registry[(month, day, win)]

    completed_steps += 1
    progress = (completed_steps / total_steps) * 100
    print(f"Progress: {progress:.2f}%", flush=True)

out_file.close()
print("Done. Results saved to spike_results.csv and individual reports in /spike_reports/")
