import os
import pandas as pd
from scipy.stats import pearsonr
from itertools import combinations
import numpy as np

def classify_correlation(corr_coefficient, p_value, significance_level=0.05):
    """
    Classify strength of a correlation coefficient considering the p-value.
    
    Params:
    corr_coefficient (float): Pearson correlation coefficient.
    p_value (float): The p-value associated with the correlation coefficient.
    significance_level (float): The threshold for determining statistical significance. Default is 0.05.
    
    Returns:
    str: Classification of the correlation ('Very Weak', 'Weak', 'Moderate', 'Strong', 'Very Strong', 'Not Significant').
    """
    if p_value > significance_level:
        return 'Not Significant'
    elif abs(corr_coefficient) > 0.8:
        return 'Very Strong'
    elif 0.6 < abs(corr_coefficient) <= 0.8:
        return 'Strong'
    elif 0.4 < abs(corr_coefficient) <= 0.6:
        return 'Moderate'
    elif 0.2 < abs(corr_coefficient) <= 0.4:
        return 'Weak'
    else:
        return 'Very Weak'

def calculate_and_save_correlation(base_path, result_base):
    """
    Traverse directory starting at base_path, finds all Excel files, calculates Pearson correlation coefficients between pairs
    of variables, and saves the results in structured format in specified results directory.

    Params:
    base_path (str): Path where function begins searching for Excel files.
    result_base (str): Root directory where correlation results will be stored.
    """
    # Walk through each directory and file starting from base path
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.xlsx'):
                # Construct the full file path
                file_path = os.path.join(root, file)

                # Read data, converting empty strings/spaces to NaN's
                data = pd.read_excel(file_path).replace({'': np.nan, ' ': np.nan})

                # Filter for numeric columns only
                numeric_data = data.select_dtypes(include=[np.number])

                # Prepare the DataFrame to store results
                results = pd.DataFrame(columns=['Feature 1', 'Feature 2', 'Correlation Coefficient', 'P-Value', 'Classification'])

                # Calculate correlations and p-values
                for col1, col2 in combinations(numeric_data.columns, 2):
                    # Drop rows where either column is NaN before correlation calculation
                    subset = numeric_data[[col1, col2]].dropna()
                    if not subset.empty:
                        corr_coefficient, p_value = pearsonr(subset[col1], subset[col2])
                        classification = classify_correlation(corr_coefficient, p_value)
                        new_row = pd.DataFrame({
                            'Feature 1': [col1],
                            'Feature 2': [col2],
                            'Correlation Coefficient': [corr_coefficient],
                            'P-Value': [p_value],
                            'Classification': [classification]
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

# Base path to project folder and result base path
base_path = 'data_impute_project/combinations'
result_base = 'data_impute_project/corr_combinations'
calculate_and_save_correlation(base_path, result_base)
