import os
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind, mannwhitneyu, shapiro, levene
# -------------------------------
# Configuration
# -------------------------------
NORMALIZE = True  # Set to True for ratio (%), False for raw count

# -------------------------------
# Directory paths
# -------------------------------
open_ended_dirs = ["./merge_result/dataname"] # put the path to your merged_result data here
closed_ended_dir = ["./merge_result/dataname"] # put the path to your merged_result data here

# Collect file paths
def get_file_paths(dirs, exclude_keywords=[]):
    files = []
    for dir_path in dirs:
        for f in os.listdir(dir_path):
            if f.endswith(".csv") and all(kw not in f for kw in exclude_keywords):
                files.append(os.path.join(dir_path, f))
    return files

open_files = get_file_paths(open_ended_dirs)
closed_files = get_file_paths(closed_ended_dir)

# Degrees of freedom calculation function (Satterthwaite approximation)
def welch_df(s1, s2, n1, n2):
    num = (s1**2 / n1 + s2**2 / n2)**2
    denom = ((s1**2 / n1)**2 / (n1 - 1)) + ((s2**2 / n2)**2 / (n2 - 1))
    return num / denom

# Function to calculate either raw counts or normalized ratios
def get_collaboration_values(file_list, normalize=False):
    values = []
    for file in file_list:
        df = pd.read_csv(file)
        df = df[df['final_label'] != '-']  # Remove bot utterances
        if len(df) == 0 or 'final_label' not in df.columns:
            continue
        is_collab = df['final_label'].apply(lambda x: 0 if x == 'x' else 1)
        if normalize:
            value = is_collab.sum() / len(is_collab)
        else:
            value = is_collab.sum()
        values.append(value)
    return values

# Get data
open_vals = get_collaboration_values(open_files, normalize=NORMALIZE)
closed_vals = get_collaboration_values(closed_files, normalize=NORMALIZE)

open_series = pd.Series(open_vals, name="Open-ended")
closed_series = pd.Series(closed_vals, name="Closed-ended")

# -------------------------------
# Statistical analysis
# -------------------------------

# 1. Normality test
shapiro_open = shapiro(open_series)
shapiro_closed = shapiro(closed_series)
print("\n[Normality Test (Shapiro-Wilk)]")
print(f"Open-ended: W={shapiro_open.statistic:.4f}, p-value={shapiro_open.pvalue:.4f}")
print(f"Closed-ended: W={shapiro_closed.statistic:.4f}, p-value={shapiro_closed.pvalue:.4f}")

# 2. Homogeneity of variances (Levene's test)
levene_stat, levene_p = levene(open_series, closed_series)
print("\n[Homogeneity of Variance Test (Levene's Test)]")
print(f"Levene statistic={levene_stat:.4f}, p-value={levene_p:.4f}")

# 3. Parametric test: Welch's t-test
welch_stat, welch_p = ttest_ind(open_series, closed_series, equal_var=False)

# 4. Non-parametric test: Mann-Whitney U test
mw_stat, mw_p = mannwhitneyu(open_series, closed_series, alternative='two-sided')

# 5. Summary statistics
mean1, std1, n1 = open_series.mean(), open_series.std(), len(open_series)
mean2, std2, n2 = closed_series.mean(), closed_series.std(), len(closed_series)
df_welch = welch_df(std1, std2, n1, n2)

# 6. Parametric tests
# Student's t-test (equal variances assumed)
student_stat, student_p = ttest_ind(open_series, closed_series, equal_var=True)

summary_stats = {
    "n1": n1,
    "n2": n2,
    "Open-ended Mean": mean1,
    "Open-ended Std Dev": std1,
    "Closed-ended Mean": mean2,
    "Closed-ended Std Dev": std2,
    "Open-ended Normality p-value": shapiro_open.pvalue,
    "Closed-ended Normality p-value": shapiro_closed.pvalue,
    "Levene's Test p-value": levene_p,
    "Student's t-test Statistic": student_stat,
    "Student's t-test p-value": student_p,
    "Welch’s t-test Statistic": welch_stat,
    "Welch’s t-test p-value": welch_p,
    "Welch Degrees of Freedom": df_welch,
    "Mann-Whitney U Statistic (reference)": mw_stat,
    "Mann-Whitney U p-value (reference)": mw_p,
}

# Print results
summary_df = pd.DataFrame.from_dict(summary_stats, orient='index', columns=["Value"])
print(f"[Statistical Analysis Results - NORMALIZE = {NORMALIZE}]")
print(summary_df)

# -------------------------------
# Visualization
# -------------------------------
plt.figure(figsize=(8, 6))
plt.boxplot([open_series, closed_series], labels=["Open-ended", "Closed-ended"])
ylabel = "Collaborative Utterances Ratio" if NORMALIZE else "Collaborative Utterances Count"
plt.ylabel(ylabel)
plt.title("Collaborative Utterances by Task Type")
plt.grid(axis='y')
plt.tight_layout()
plt.savefig(f"./statistic/collaboration_boxplot_{'ratio' if NORMALIZE else 'count'}.png", dpi=300)
plt.show()
