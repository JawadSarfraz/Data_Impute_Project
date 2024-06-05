import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error
from itertools import combinations
import os
import time

def calculate_mae_filtered(original, imputed, missing_mask):
    """
    Func calculates mean absolute error (MAE) between two arrays (columns)
    after filtering out zero differences and considering only imputed values.
    
    Params:
    original: array contains original column values before removal of values.
    imputed: array contains values after imputation of missing values.
    missing_mask: boolean array where True indicates values that were originally missing.
    
    return: function returns Mean Absolute Error (MAE) between original and imputed values,
    but only for the values that were imputed.
    """
    imputed_values = imputed[missing_mask]
    original_values = original[missing_mask]
    # Return MAE for imputed values
    if len(original_values) > 0:
        return mean_absolute_error(original_values, imputed_values)
    else:
        return 0  # Return 0 if there are no imputed values to avoid division by zero

def calculate_mape_filtered(original, imputed, missing_mask):
    """
    The function calculates mean absolute percentage error (MAPE) between two arrays (columns)
    after considering only imputed values.
    
    Params:
    original: array contains original column values before removal of values.
    imputed: array contains values after imputation of missing values.
    missing_mask: boolean array where True indicates the values that were originally missing.
    
    return: The function returns Mean Absolute Percentage Error (MAPE) between
    original and imputed values, but only for the values that were imputed.
    """
    imputed_values = imputed[missing_mask]
    original_values = original[missing_mask]

    # Return MAPE for imputed values
    if len(original_values) > 0:
        return np.mean(np.abs((original_values - imputed_values) / original_values)) * 100
    else:
        return 0  # Return 0 if there are no imputed values to avoid division by zero

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
    feature_sets = []
    for i in range(1, len(features) + 1):
        for comb in combinations(features, i):
            if current_feature in comb:
                feature_sets.append(''.join(comb))
    return feature_sets

def translate_feature_set(feature_set, feature_names):
    """
    Translate feature set string into its corresponding feature names.

    Params:
    feature_set (str): Concatenated string of feature set (e.g., 'ABC').
    feature_names (dict): Mapping of single feature characters to their actual names.

    Returns:
    str: Translated feature set name (e.g., 'δ13C coll_δ15N coll_δ13C carb').
    """
    return '_'.join(feature_names[feature] for feature in feature_set)

def format_feature_name(feature, feature_names):
    """
    Format feature name for the DataFrame.

    Params:
    feature (str): Single character representing the feature (e.g., 'A').
    feature_names (dict): Mapping of single feature characters to their actual names.

    Returns:
    str: Formatted feature name (e.g., 'A (δ13C coll)').
    """
    return f"{feature} ({feature_names[feature]})"

# Mapping of features into their actual names.
feature_names = {
    'A': 'δ13C coll',
    'B': 'δ15N coll',
    'C': 'δ13C carb',
    'D': 'δ18O carb',
    'E': 'δ18O phos',
    'F': 'δ34S coll'
}

# Start the timer
start_time = time.time()

# Setup
base_original_path = 'data_impute_project/combinations/terrestrial_mammals'
combinations_list = ['combination_1_ABCD', 'combination_2_ABCDE', 'combination_3_ABCDF']
base_result_path = 'data_impute_project/algorithm_result/terrestrial_mammals'
removed_data_base_path = 'data_impute_project/removed_data/terrestrial_mammals'
output_dir = 'data_impute_project/error_metrics'
ensure_dir(output_dir)
percentages = ['10', '15', '20']
seeds = ['seed1', 'seed2', 'seed3', 'seed4', 'seed5']
algorithms = ['KNN', 'SVM', 'RandomForest']

# Store final results
final_results = []

# Iterating over different combinations of features, algorithms, percentages, and seeds to calculate Mean
# Absolute Error (MAE) and Mean Absolute Percentage Error (MAPE) for imputed data compared to original data.
for combination in combinations_list:
    original_file_path = os.path.join(base_original_path, f"{combination}.xlsx")
    if os.path.exists(original_file_path):
        original_data = pd.read_excel(original_file_path)
        features = original_data.columns.dropna()

        for feature in features:
            feature_sets = get_feature_sets(features, feature)

            for percentage in percentages:
                for feature_set in feature_sets:
                    for algorithm in algorithms:
                        mae_values = []
                        mape_values = []

                        for seed in seeds:
                            result_file_path = os.path.join(base_result_path, f"{combination}/{feature_set}/{percentage}/{seed}/result_data_{algorithm}.xlsx")
                            missing_file_path = os.path.join(removed_data_base_path, f"{combination}/{feature}/{percentage}/{seed}/missing_data.xlsx")
                            
                            if os.path.exists(result_file_path) and os.path.exists(missing_file_path):
                                result_data = pd.read_excel(result_file_path)
                                missing_data = pd.read_excel(missing_file_path)
                                
                                if feature in result_data.columns:
                                    imputed_feature = result_data[feature]
                                    missing_mask = missing_data[feature].isna()  # Identify missing values mask
                                    mae = calculate_mae_filtered(original_data[feature], imputed_feature, missing_mask)
                                    mape = calculate_mape_filtered(original_data[feature], imputed_feature, missing_mask)
                                    mae_values.append(mae)
                                    mape_values.append(mape)

                        # Average MAE and MAPE
                        mean_mae = np.mean(mae_values) if mae_values else float('inf')
                        mean_mape = np.mean(mape_values) if mape_values else float('inf')
                        
                        # Translate feature set name
                        translated_feature_set = translate_feature_set(feature_set, feature_names)
                        
                        # Format feature name
                        formatted_feature = format_feature_name(feature, feature_names)

                        # Aggregate results
                        final_results.append([combination, formatted_feature, percentage, algorithm, feature_set, translated_feature_set, mean_mae, mean_mape])

# Create DataFrame and save to CSV
df_final = pd.DataFrame(final_results, columns=['Combination', 'Feature', 'Percentage', 'Algorithm', 'FeatureSet', 'TranslatedFeatureSet', 'MAE', 'MAPE'])
output_file_path = os.path.join(output_dir, 'error_analysis_with_all_featureset.csv')
df_final.to_csv(output_file_path, index=False)

# End timer and print running time
end_time = time.time()
print(f"Final error analysis saved to: {output_file_path}")
print(f"Running time of the script: {end_time - start_time} seconds")