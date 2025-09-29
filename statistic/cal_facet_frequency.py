import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from scipy.stats import ttest_ind, mannwhitneyu

# ----------------------------
# Configuration
# ----------------------------
MODE = "facet"         # "facet" or "subfacet"
NORMALIZE = True      # True = use ratios, False = use raw counts

# ----------------------------
# Mode-specific settings
# ----------------------------
if MODE == "facet":
    TARGET_COLUMN = "facet"
    TARGET_KEYS = ['f1', 'f2', 'f3']
elif MODE == "subfacet":
    TARGET_COLUMN = "final_label"
    TARGET_KEYS = ['a', 'b', 'c', 'd', 'e', 'f']
else:
    raise ValueError("MODE must be either 'facet' or 'subfacet'")

VALUE_LABEL = "Ratio" if NORMALIZE else "Count"
PLOT_XLABEL = "Facet" if MODE == "facet" else "Subfacet"
PLOT_TITLE = f"{PLOT_XLABEL}-wise Collaboration {'Ratios' if NORMALIZE else 'Counts'} by Task Type"
OUTPUT_FILENAME = f"{MODE}_{'ratio' if NORMALIZE else 'count'}_boxplot.png"

# ----------------------------
# Directories
# ----------------------------
open_ended_dirs = "./merge_result/dataname" # put the path to your merged_result data here
closed_ended_dir = "./merge_result/dataname" # put the path to your merged_result data here
def get_file_paths(dirs, exclude_keywords=[]):
    files = []
    for dir_path in dirs:
        for f in os.listdir(dir_path):
            if f.endswith(".csv") and all(kw not in f for kw in exclude_keywords):
                files.append(os.path.join(dir_path, f))
    return files

open_files = get_file_paths(open_ended_dirs)
closed_files = get_file_paths([closed_ended_dir], exclude_keywords=["IDS", "2.csv"])

# ----------------------------
# Count or Normalize
# ----------------------------
def extract_features(file_list, normalize=False):
    data = []
    for file in file_list:
        df = pd.read_csv(file)
        df = df[df['final_label'] != '-']
        if len(df) == 0 or TARGET_COLUMN not in df.columns:
            continue
        counts = Counter(df[TARGET_COLUMN])
        if normalize:
            total = sum(counts.values())
            values = {k: counts.get(k, 0) / total for k in TARGET_KEYS}
        else:
            values = {k: counts.get(k, 0) for k in TARGET_KEYS}
        data.append(values)
    return pd.DataFrame(data).fillna(0)

open_df = extract_features(open_files, normalize=NORMALIZE)
closed_df = extract_features(closed_files, normalize=NORMALIZE)

# ----------------------------
# Statistical Analysis
# ----------------------------
results = {}
for key in TARGET_KEYS:
    open_vals = open_df[key]
    closed_vals = closed_df[key]
    t_stat, t_p = ttest_ind(open_vals, closed_vals, equal_var=False)
    u_stat, u_p = mannwhitneyu(open_vals, closed_vals, alternative='two-sided')
    results[key] = {
        'Open Mean': open_vals.mean(),
        'Open SD': open_vals.std(),
        'Closed Mean': closed_vals.mean(),
        'Closed SD': closed_vals.std(),
        'Welch t': t_stat,
        'Welch p': t_p,
        'MW U': u_stat,
        'MW p': u_p,
    }

stat_df = pd.DataFrame(results).T.round(4)
print(f"[Statistical Analysis Results - MODE: {MODE}, NORMALIZED: {NORMALIZE}]")
print(stat_df)

# ----------------------------
# Visualization
# ----------------------------
open_df['Type'] = 'Open-ended'
closed_df['Type'] = 'Closed-ended'
combined_df = pd.concat([open_df, closed_df], ignore_index=True)

melted_df = pd.melt(combined_df, id_vars='Type', value_vars=TARGET_KEYS,
                    var_name=PLOT_XLABEL, value_name=VALUE_LABEL)

plt.figure(figsize=(10, 6))
sns.boxplot(data=melted_df, x=PLOT_XLABEL, y=VALUE_LABEL, hue='Type')
plt.title(PLOT_TITLE)
plt.ylabel(VALUE_LABEL)
plt.xlabel(PLOT_XLABEL)
plt.legend(title="Task Type")
plt.tight_layout()
plt.savefig(OUTPUT_FILENAME, dpi=300)
plt.show()
