# Uses Shapiro-Wilk Test to determine whether the facet values within each team
# (closed or open tasks) are uniformally distributed, thereas which we can use
# to determine whether certain t-tests are valid or not. To that end, the IDS
# and IDS2 folders should be combined into 1 (note the overlapping file names)
# within each before running this script on the folder.

import os
import pandas as pd
from scipy.stats import shapiro

# === CONFIG ===
folder_path = "FCDS"  # FCDS or IDScombined

# === Initialize storage for facet counts ===
facet_counts = {
    "f1": [],
    "f2": [],
    "f3": []
}

# === Process each CSV file ===
for filename in os.listdir(folder_path):
    if filename.endswith(".csv"):
        filepath = os.path.join(folder_path, filename)
        df = pd.read_csv(filepath)

        # Count occurrences of each facet
        counts = df["facet"].value_counts()

        for facet in ["f1", "f2", "f3"]:
            facet_counts[facet].append(counts.get(facet, 0))  # default to 0 if facet not present

# === Run Shapiro-Wilk test on each facet array ===
for facet, values in facet_counts.items():
    print(f"\n== Shapiro-Wilk Test for {facet} ==")
    if len(values) >= 3:
        stat, p = shapiro(values)
        print(f"Counts per file: {values}")
        print(f"Statistic = {stat:.4f}, p-value = {p:.4f}")
        if p > 0.05:
            print("Yes, Likely normal distribution (fail to reject H₀)")
        else:
            print("No, Likely not a normal distribution (reject H₀)")
    else:
        print("Not enough data (need at least 3 values)")
