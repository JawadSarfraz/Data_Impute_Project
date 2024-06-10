import pandas as pd
import numpy as np
import itertools
import os
import re

# Function to remove data based on a given percentage and seed
def remove_data(df, columns_to_modify, percentage, seed):
    """
    Randomly sets specified percentage of data to NaN in given columns of DataFrame.
    
    Params:
    df (pd.DataFrame): Original DataFrame.
    columns_to_modify (list): List of column names in which data will be removed.
    percentage (int): Percentage of data to remove
    seed (int): Random seed for reproducibility of results.
    
    Returns:
    pd.DataFrame: A DataFrame with data removed as specified.
    """
    np.random.seed(seed)
    modified_df = df.copy() # Create a copy of DataFrame to modify
    for col in columns_to_modify:
        if col != 'ID':  # Skip ID column
            mask = np.random.rand(len(modified_df)) < percentage / 100.0 # Create mask where data will be set to NaN
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

# Define percentages of data removal and seeds for randomization
percentages = [10, 15, 20]
seeds = [1, 2, 3, 4, 5]

# Loop through each file specified
for filename in filenames:
    # Read the dataset from file
    df = pd.read_excel(os.path.join(combination_base_path, filename))
    
    # Extract column names from the DataFrame, excluding the first column which is the ID
    columns = df.columns[1:]
    
    # Generate combinations of the given columns (up to the number of columns in the file)
    for L in range(1, len(columns) + 1):
        for subset in itertools.combinations(columns, L):
            subset_with_id = ['ID'] + list(subset)  # Ensure ID is the first column in the subset
            for percentage in percentages:
                for seed in seeds:
                    # Remove data based on the current configuration
                    modified_df = remove_data(df, subset_with_id, percentage, seed)
                    
                    # Construct the output path
                    dir_path = f"{filename.rstrip('.xlsx')}/{'' .join(subset)}/{percentage}/seed{seed}"
                    full_output_path = os.path.join(output_base_path, dir_path)
                    
                    # Create the directory if it does not exist
                    if not os.path.exists(full_output_path):
                        os.makedirs(full_output_path)
                    
                    # Save the modified DataFrame to an Excel file in created directory
                    output_file = 'missing_data.xlsx'
                    modified_df.to_excel(os.path.join(full_output_path, output_file), index=False)

print("Modified datasets created and saved successfully.")