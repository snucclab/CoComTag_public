import pandas as pd
import glob
import os

# Set target folder
folder_path = './best_predictions/dataname' # update to the name of your data
csv_files = glob.glob(os.path.join(folder_path, '*.csv'))
# print(csv_files)
# Facet mapping function
def map_to_facet(pred):
    if pred in ['a', 'b']:
        return 'f1'
    elif pred in ['c', 'd']:
        return 'f2'
    elif pred in ['e', 'f']:
        return 'f3'
    else:
        return 'x'

# Process all CSV files
for file_path in csv_files:
    if 'csv_2' in os.path.basename(file_path):
        print(f"Skipped: {file_path}")
        continue  # Skip files that contain 'csv_2' in their name

    df = pd.read_csv(file_path)
    
    # Create 'facet' column
    df['facet'] = df['final_label'].apply(map_to_facet)
    
    # Overwrite the original file
    df.to_csv(file_path, index=False)
    # print(df)
    print(f"Updated: {file_path}")
