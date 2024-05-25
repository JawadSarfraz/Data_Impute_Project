# NEED TO WORK ON THIS SCRIPT SO IT WILL WORK TO REMOVE DATA FROM ALL DATASET SIMILAR TO TERR MAM...
import pandas as pd
import numpy as np
import itertools
import os
import re

def remove_data(df, columns_to_modify, percentage, seed):
    np.random.seed(seed)
    modified_df = df.copy()
    for col in columns_to_modify:
        if col in df.columns:
            mask = np.random.rand(len(modified_df)) < percentage / 100.0
            modified_df.loc[mask, col] = np.nan
    return modified_df

def process_dataset(category, combination_base_path, output_base_path):
    # Dynamically list filenames for the given category
    filenames = [f for f in os.listdir(os.path.join(combination_base_path, category)) if f.endswith('.xlsx')]

    percentages = [10, 15, 20]
    seeds = [1, 2, 3, 4, 5]

    for filename in filenames:
        df = pd.read_excel(os.path.join(combination_base_path, category, filename))
        
        # Extract column labels from the filename
        columns = re.findall(r'combination_\d+_([A-Z]+).xlsx', filename)[0]
        
        for L in range(1, len(columns) + 1):
            for subset in itertools.combinations(columns, L):
                for percentage in percentages:
                    for seed in seeds:
                        modified_df = remove_data(df, subset, percentage, seed)
                        dir_path = f"{filename.rstrip('.xlsx')}/{'' .join(subset)}/{percentage}/seed{seed}"
                        full_output_path = os.path.join(output_base_path, category, dir_path)
                        
                        if not os.path.exists(full_output_path):
                            os.makedirs(full_output_path)
                        
                        output_file = 'seed{seed}.xlsx'.format(seed=seed)
                        modified_df.to_excel(os.path.join(full_output_path, output_file), index=False)

base_data_dir = 'data_impute_project/data'
base_combination_dir = 'data_impute_project/combinations'
output_base_path = 'data_impute_project/removed_data'

# List of dataset categories to process
categories = ['terrestrial_mammals', 'fish', 'birds', 'mammals_without_humans', 'humans']

for category in categories:
    process_dataset(category, base_combination_dir, output_base_path)

print("Modified datasets created and saved successfully for all categories.")