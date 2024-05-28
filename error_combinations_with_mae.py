import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error
from math import sqrt
from itertools import combinations
import os
import time


def calculate_mae_filtered(original, imputed):
    """
    The function calculates mean absolute error (MAE) between two arrays(Columns)
    after filtering out zero differences.
    
    Params:
    original: array contains orignal column values before removal of values.
    imputed: array contains values after imputation of missing values.

    return: The function returns Mean Absolute Error (MAE) between
    original and imputed values, but only for non-zero differences. If there are no non-zero
    differences, it returns 0 to avoid division by zero.
    """
    # Calculate differences and filter out zero differences
    differences = original - imputed
    filtered_original = original[differences != 0]
    filtered_imputed = imputed[differences != 0]

    # Return MAE only for non-zero differences
    if len(filtered_original) > 0:
        return mean_absolute_error(filtered_original, filtered_imputed)
    else:
        return 0  # Return 0 if there are no differences to avoid division by zero

def ensure_dir(directory):
    """
    The function `ensure_dir` creates a directory if it does not already exist.    
    """
    if not os.path.exists(directory):
        os.makedirs(directory)





def get_feature_sets(features, current_feature):
    """
    Generate all combinations of features from the provided list while ensuring that each combination includes
    the specified 'current_feature'.

    Params:
    features (list): List of all features available.
    current_feature (str): The feature that must be included in all combinations.

    Returns:
    list: A list of feature combinations, each as a concatenated string, where 'current_feature' is included in each combination.
    """
    # Initialize an empty list to store feature combinations
    feature_sets = []

    # Loop over all possible lengths for combinations, from 1 up to the number of features available
    for i in range(1, len(features) + 1):
        # Generate all combinations of features of length 'i'
        for comb in combinations(features, i):
            # Check if the 'current_feature' is in this combination
            if current_feature in comb:
                # If 'current_feature' is in the combination, convert the tuple of features to a concatenated string
                # and add it to the list of feature sets
                feature_sets.append(''.join(comb))

    # Return the list of feature sets that include 'current_feature'
    return feature_sets




# Start the timer
start_time = time.time()

# Setup
base_original_path = 'data_impute_project/combinations/terrestrial_mammals'
combinations_list = ['combination_1_ABCD', 'combination_2_ABCDE', 'combination_3_ABCDF']
base_result_path = 'data_impute_project/algorithm_result/terrestrial_mammals'
output_dir = 'data_impute_project/error_metrics'
ensure_dir(output_dir)
percentages = ['10', '15', '20']
seeds = ['seed1', 'seed2', 'seed3', 'seed4', 'seed5']
algorithms = ['KNN', 'SVM', 'RandomForest']

# Store final results
final_results = []

# Iterating over different combinations of features, algorithms, percentages, and seeds to calculate Mean
# Absolute Error (MAE) for imputed data compared to original data.
for combination in combinations_list:
    original_file_path = os.path.join(base_original_path, f"{combination}.xlsx")
    if os.path.exists(original_file_path):
        original_data = pd.read_excel(original_file_path)
        features = original_data.columns.dropna()

        for feature in features:
            feature_sets = get_feature_sets(features, feature)

            for percentage in percentages:
                min_errors = {algo: {'MAE': float('inf'), 'FeatureSet': ''} for algo in algorithms}
                
                for feature_set in feature_sets:
                    for algorithm in algorithms:
                        mae_values = []

                        for seed in seeds:
                            result_file_path = os.path.join(base_result_path, f"{combination}/{feature_set}/{percentage}/{seed}/result_data_{algorithm}.xlsx")
                            if os.path.exists(result_file_path):
                                result_data = pd.read_excel(result_file_path)
                                if feature in result_data.columns:
                                    imputed_feature = result_data[feature]
                                    mae = calculate_mae_filtered(original_data[feature], imputed_feature)  # Using the modified MAE calculation
                                    mae_values.append(mae)

                        # Average MAE and update min_errors if this is the new minimum
                        mean_mae = np.mean(mae_values) if mae_values else float('inf')
                        
                        if mean_mae < min_errors[algorithm]['MAE']:
                            min_errors[algorithm]['MAE'] = mean_mae
                            min_errors[algorithm]['FeatureSet'] = feature_set

                # Aggregate final results
                for algo, error_info in min_errors.items():
                    final_results.append([combination, feature, percentage, algo,  error_info['MAE'], error_info['FeatureSet']])


# Create DataFrame and save to CSV
df_final = pd.DataFrame(final_results, columns=['Combination', 'Feature', 'Percentage', 'Algorithm', 'Min MAE', 'FeatureSet Removal Scenario'])
output_file_path = os.path.join(output_dir, 'min_error_analysis_with_feature_combinations.csv')
df_final.to_csv(output_file_path, index=False)

# End the timer and print the running time
end_time = time.time()
print(f"Final minimum error analysis saved to: {output_file_path}")
print(f"Running time of the script: {end_time - start_time} seconds")