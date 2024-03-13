import pandas as pd
import numpy as np
import itertools
import os
import re

# Randomly remove data
def remove_data(df, columns_to_modify, percentage, seed):
    np.random.seed(seed)
    modified_df = df.copy()
    for col in columns_to_modify:
        mask = np.random.rand(len(modified_df)) < percentage / 100.0
        modified_df.loc[mask, col] = np.nan
    return modified_df

# Base path for combinations and modified datasets
combination_base_path = 'data_impute_project/combinations/terrestrial_mammals/'
output_base_path = 'data_impute_project/removed_data/terrestrial_mammals/'

# List combination files
filenames = [f for f in os.listdir(combination_base_path) if f.endswith('.xlsx')]

percentages = [10, 15, 20]
seeds = [1, 2, 3, 4, 5]

for filename in filenames:
    df = pd.read_excel(os.path.join(combination_base_path, filename))
    
    # Extract columns from filename and exclude 'A' to 'E'
    match = re.search('combination_\d+_([A-Z_]+).xlsx', filename)
    if match:
        columns = match.group(1).split('_')
        # Filter out columns 'A' to 'E'
        columns_to_modify = [col for col in columns if col >= 'F']
        
        for percentage in percentages:
            for seed in seeds:
                for L in range(1, min(len(columns_to_modify) + 1, 6)):  # Upto 5 Columns
                    for subset in itertools.combinations(columns_to_modify, L):
                        modified_df = remove_data(df, subset, percentage, seed)
                        combination_dir = filename.split('.xlsx')[0]
                        columns_dir = ''.join(subset)
                        specific_path = os.path.join(output_base_path, combination_dir, columns_dir, str(percentage), f"seed{seed}")
                        os.makedirs(specific_path, exist_ok=True)
                        
                        modified_filename = "missing_data.xlsx"
                        modified_df.to_excel(os.path.join(specific_path, modified_filename), index=False)

print("Modified datasets created Successfully...:)")