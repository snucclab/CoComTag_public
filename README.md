# Capturing Collaborative Competency with GPT-4o and ENA [(Paper)](https://repository.isls.org/handle/1/11963)

# CoComTag

## 1. Installation

#### 1) Clone the repository
```bash
git clone https://github.com/snucclab/CoComTag_public.git
cd CoComTag
```

#### 2) Create and activate a virtual environment
```bash
conda create -n CoComTag python=3.11.11
conda activate CoComTag
```

#### 3) Install required dependencies
```bash
pip install -r requirements.txt
```

## 2. Dataset Setup
Save the dataset as the following structure. The original datasets and folders are deleted for privacy.
```bash
data/
├── FCDS/
│   ├── group1_file1.csv   # Closed-ended task files (Group 1)
│   └── ...
├── IDS/
│   ├── group2_file1.csv   # Open-ended task files (Group 2)
│   └── ...
├── IDS2/
│   ├── group3_file1.csv   # Open-ended task files (Group 3)
│   └── ...
```
Each CSV file should contain at least the following columns:

- username — speaker ID (e.g., Student1)
- content — the uttered sentence

If you want to run CoComTag without modifying the code, the columns should be in the following order:
- #, timestamp, username, type, content


## 3. LLM-Based Labeling (CoComTag Framework)
- input: CSV files from: "data/FCDS/", "data/IDS/", "data/IDS2/" (must contain "username" and "content" columns)
- output: Adds a "pred" column (subfacet code: sf1(a)–sf6(f)) to each file, Output is saved in the result folders: "result/FCDS/", "result/IDS/", "result/IDS2/"
- Both CSV and JSON files are generated as output. From now on, we will only use the CSV files.

```bash
python LLM_label_with_kappa_subfacet.py
```
- Inside the code, the number of prediction results to output can be specified using the "repeat_count" variable.
- We run the prediction 3 times and select the most frequently occurring label among the 3 prediction results. If all 3 results are different, we select one randomly.
- Each of the 3 prediction results is saved with filenames in the following format: run0_filename.csv, run1_filename.csv, run2_filename.csv.
  
### 3.1. Combine multiple prediction results into a single prediction result
- input: CSV files from: "result/FCDS/", "result/IDS/", "result/IDS2/"
- output: Adds a "final_label" column (subfacet code: sf1(a)–sf6(f)) to each file, Output is saved in the result folders: "merge_result/FCDS/", "merge_result/IDS/", "merge_result/IDS2/"

** before you run the following code, modify the extrace_final_label.py file following the inline comments.
```bash
python merge_result/extract_final_label.py
```

  
### 3.2. Add facet Column (Mapping from pred)
Maps subfacet predictions (final_label) to higher-level facets (facet = f1–f3).
- input: CSV files from: "merge_result/FCDS/", "merge_result/IDS/", "merge_result/IDS2/" (must contain the "final_label" column)
- output: Adds "facet" column to each file, Saved in-place in the same folders: "merge_result/FCDS/", "merge_result/IDS/", "merge_result/IDS2/"

** before you run the following code, modify the make_facet.py file following the inline comments.
```bash
python statistic/preproc/make_facet.py
```

## 4. Statistical Analysis
The framework compares collaborative competence across different task types (open-ended vs closed-ended), using a hierarchical structure:
- Overall → Facet (f1–f3) → Subfacet (sf1(a)–sf6(f))

<div align="center">
  <img src="https://github.com/user-attachments/assets/15c88ce8-8014-4b39-8b2c-21432b605d2a" width="800"/>
</div>

```bash
## visualization library setup
pip install matplotlib
pip install seaborn
```

### 1) Overall Competence Comparison
Compares the count or ratio of collaborative utterances (Overall level):
- input: Labeled CSV files from: "merge_result/FCDS/", "merge_result/IDS/", "merge_result/IDS2/" (must contain the "final_label" column)
- output:
  - Console Output: Descriptive statistics and hypothesis test results (Welch's t-test and Mann–Whitney U) printed to the terminal
  - Visualization path:    
  "statistic/collaboration_boxplot_ratio.png" (if NORMALIZE = True)   
  "statistic/collaboration_boxplot_count.png" (if NORMALIZE = False)   

** before you run the following code, modify the cal_overall_frequency.py file following the inline comments.
```bash
python statistic/cal_overall_frequency.py
```

Set the analysis mode inside the script:
```bash
NORMALIZE = True # Compare ratios of (sub)facet utterances, normalized per file
# or
NORMALIZE = False # Compare the number of utterances 
```

### 2) (Sub)Facet-Level Competence Comparison

Compares the count or ratio of utterances per facet (f1-f3) or subfacet (sf1(a)-sf6(f)).
- input: Labeled CSV files from: "merge_result/FCDS/", "merge_result/IDS/", "merge_result/IDS2/" (must contain the "final_label" and "facet" column)
- output:
  - Console Output: Descriptive statistics and hypothesis test results (Welch's t-test and Mann–Whitney U) printed to the terminal
  - Visualization path: File name depends on mode and normalization   
    "statistic/facet_ratio_boxplot.png"   
    "statistic/facet_count_boxplot.png"   
    "statistic/subfacet_ratio_boxplot.png"  
    "statistic/subfacet_count_boxplot.png"   

** before you run the following code, modify the cal_facet_frequency.py file following the inline comments.
```bash
python statistic/cal_facet_frequency.py
```
  

Set the analysis mode inside the script:
```bash
MODE = "facet"     # for f1, f2, f3
# or
MODE = "subfacet"  # for sf1(a)–sf6(f)
```
```bash
NORMALIZE = True # Compare ratios of (sub)facet utterances, normalized per file
# or
NORMALIZE = False # Compare the number of utterances 
```



