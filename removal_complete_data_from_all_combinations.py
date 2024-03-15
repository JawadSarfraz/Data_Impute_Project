import pandas as pd
import numpy as np
import itertools
import os
import re
import time

def remove_data(df, columns_to_modify, percentage, seed):
    np.random.seed(seed)
    modified_df = df.copy()
    for col in columns_to_modify:
        if col in df.columns:  # Ensure column exists in the dataframe
            mask = np.random.rand(len(modified_df)) < percentage / 100.0
            modified_df.loc[mask, col] = np.nan
    return modified_df

def process_dataset(dataset_name, percentages, seeds):
    combination_base_path = os.path.join('data_impute_project/combinations', dataset_name)
    output_base_path = os.path.join('data_impute_project/removed_data', dataset_name)
    
    filenames = [f for f in os.listdir(combination_base_path) if f.endswith('.xlsx')]
    
    for filename in filenames:
        df = pd.read_excel(os.path.join(combination_base_path, filename))
        
        match = re.search('combination_\d+_([A-Z_]+).xlsx', filename)
        if match:
            columns = match.group(1).split('_')
            columns_to_modify = [col for col in columns if col >= 'F']  # Exclude 'A' to 'E'
            
            for percentage in percentages:
                for seed in seeds:
                    for L in range(1, min(len(columns_to_modify) + 1, 6)):  # Up to 5 columns
                        for subset in itertools.combinations(columns_to_modify, L):
                            modified_df = remove_data(df, subset, percentage, seed)
                            combination_dir = filename.split('.xlsx')[0]
                            columns_dir = ''.join(subset)
                            specific_path = os.path.join(output_base_path, combination_dir, columns_dir, str(percentage), f"seed{seed}")
                            os.makedirs(specific_path, exist_ok=True)
                            
                            modified_filename = "missing_data.xlsx"
                            modified_df.to_excel(os.path.join(specific_path, modified_filename), index=False)

start_time = time.time()

datasets = [
    'marine_mammals',
     'fish', 
     'human',
     'mammals_without_humans',
     'terr_herb_and_marine_mammals',
     'terrestrial_herbivorous_mammals',
     'terrestrial_mammals'
]
percentages = [10, 15, 20]
seeds = [1, 2, 3, 4, 5]

for dataset_name in datasets:
    process_dataset(dataset_name, percentages, seeds)

end_time = time.time()
print("Modified datasets for all combinations have been created...:)")
print(f"Overall Running Time for generating combinations: {end_time - start_time:.2f} seconds.")