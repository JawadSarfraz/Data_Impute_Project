import pandas as pd
import numpy as np
import itertools
import os
import re

# Function to remove data based on a given percentage and seed
def remove_data(df, columns_to_modify, percentage, seed):
    np.random.seed(seed)
    modified_df = df.copy()
    for col in columns_to_modify:
        mask = np.random.rand(len(modified_df)) < percentage / 100.0
        modified_df.loc[mask, col] = np.nan
    return modified_df

# Define base paths
combination_base_path = 'data_impute_project/combinations/terrestrial_mammals/'
output_base_path = 'data_impute_project/removed_data/terrestrial_mammals/'

# List of filenames to be processed, you can adjust this to loop through your actual files
filenames = [
    'combination_1_ABCD.xlsx',
    'combination_2_ABCDE.xlsx',
    'combination_3_ABCDF.xlsx'
    # Add other filenames as necessary
]

percentages = [10, 15, 20]
seeds = [1, 2, 3, 4, 5]

for filename in filenames:
    # Read the dataset
    df = pd.read_excel(os.path.join(combination_base_path, filename))
    
    # Get the column labels from the filename (assuming they start right after 'combination_N_')
    columns = re.findall(r'combination_\d+_([A-Z]+).xlsx', filename)[0]
    
    # Generate combinations of the given columns (up to the number of columns in the file)
    for L in range(1, len(columns) + 1):
        for subset in itertools.combinations(columns, L):
            for percentage in percentages:
                for seed in seeds:
                    # Remove data based on the current configuration
                    modified_df = remove_data(df, subset, percentage, seed)
                    
                    # Construct the output path
                    dir_path = f"{filename.rstrip('.xlsx')}/{'' .join(subset)}/{percentage}/seed{seed}"
                    full_output_path = os.path.join(output_base_path, dir_path)
                    
                    # Create the directory if it does not exist
                    if not os.path.exists(full_output_path):
                        os.makedirs(full_output_path)
                    
                    # Save the modified dataframe
                    output_file = 'missing_data.xlsx'
                    modified_df.to_excel(os.path.join(full_output_path, output_file), index=False)

print("Modified datasets created and saved successfully.")