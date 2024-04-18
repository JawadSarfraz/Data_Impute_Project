import os
import pandas as pd
from scipy.stats import pearsonr
from itertools import combinations
import numpy as np

def calculate_and_save_correlation(base_path, result_base):
    # Mapping from column letters to descriptive names
    column_map = {
        'A': 'δ13C coll',
        'B': 'δ15N coll',
        'C': 'δ13C carb',
        'D': 'δ18O carb',
        'E': 'δ34S coll',
        'F': 'δ18O phos',
        'G': '87Sr/86Sr bone',
        'H': '87Sr/86Sr enamel'
    }
    
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.xlsx'):
                # Construct full file path
                file_path = os.path.join(root, file)

                # Read data, converting empty strings/spaces to NaN's and apply the column name mapping
                data = pd.read_excel(file_path).replace({'': np.nan, ' ': np.nan}).rename(columns=column_map)

                # Prepare DataFrame to store results
                results = pd.DataFrame(columns=['Variable 1', 'Variable 2', 'Correlation Coefficient', 'P-Value'])

                # Calculate correlations and p-values
                for col1, col2 in combinations(data.columns, 2):
                    # Drop rows where either column is NaN before correlation calculation
                    subset = data[[col1, col2]].dropna()
                    if not subset.empty:
                        corr_coefficient, p_value = pearsonr(subset[col1], subset[col2])
                        new_row = pd.DataFrame({
                            'Variable 1': [col1],
                            'Variable 2': [col2],
                            'Correlation Coefficient': [corr_coefficient],
                            'P-Value': [p_value]
                        })
                        results = pd.concat([results, new_row], ignore_index=True)

                # Path for results to save in specified directory
                relative_path = os.path.relpath(root, base_path)
                result_directory = os.path.join(result_base, relative_path)
                os.makedirs(result_directory, exist_ok=True)
                result_file_name = file.replace('.xlsx', '_correlation_results.xlsx')
                result_file_path = os.path.join(result_directory, result_file_name)

                # Save the results
                results.to_excel(result_file_path, index=False)

                print(f'Results saved to: {result_file_path}')

# Base path to folder and result base path
base_path = 'data_impute_project/combinations'
result_base = 'data_impute_project/corr_combinations_test_rename'
calculate_and_save_correlation(base_path, result_base)