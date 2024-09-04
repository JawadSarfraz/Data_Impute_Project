import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error
from itertools import combinations
import os
import time

# List of valid datasets
datasets = ["bird", "fish", "human", "mammals_without_humans", "marine_mammals", 
            "terr_herb_and_marine_mammals", "terrestrial_herbivorous_mammals", "terrestrial_mammals"]

# Prompt user for dataset type
dataset_type = input(f"Enter the dataset type {datasets}: ").strip()

# Verify if entered dataset type is valid
if dataset_type not in datasets:
    raise ValueError("Invalid dataset type entered. Please try again.")

# Function to calculate MAE between imputed and original values
def calculate_mae_filtered(original, imputed, missing_mask):
    imputed_values = imputed[missing_mask]
    original_values = original[missing_mask]
    if len(original_values) > 0:
        return mean_absolute_error(original_values, imputed_values)
    else:
        return 0

# Function to calculate MAPE between imputed and original values
def calculate_mape_filtered(original, imputed, missing_mask):
    imputed_values = imputed[missing_mask]
    original_values = original[missing_mask]
    if len(original_values) > 0:
        return np.mean(np.abs((original_values - imputed_values) / original_values)) * 100
    else:
        return 0

# Function to calculate MAE in parts per thousand (‰)
def calculate_mae_per_thousand(mean_mae, original_values):
    mean_original = np.mean(original_values)
    if mean_original != 0:
        return (mean_mae / mean_original) * 1000
    else:
        return 0

# Ensure directory exists
def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Get combinations of feature sets that include the current feature
def get_feature_sets(features, current_feature):
    feature_sets = []
    for i in range(1, len(features) + 1):
        for comb in combinations(features, i):
            if current_feature in comb:
                feature_sets.append(''.join(comb))
    return feature_sets

# Translate feature set string to feature names
def translate_feature_set(feature_set, feature_names):
    return '_'.join(feature_names[feature] for feature in feature_set)

# Format feature name for display
def format_feature_name(feature, feature_names):
    return f"{feature} ({feature_names[feature]})"

# Mapping of features to their actual names
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

# Setup paths based on selected dataset type
base_original_path = os.path.join('..', 'data_impute_project', 'combinations', dataset_type)
combinations_list = ['combination_1_ABCD', 'combination_2_ABCDE', 'combination_3_ABCDF']
base_result_path = os.path.join('..', 'data_impute_project', 'impute_algos_result', dataset_type)
removed_data_base_path = os.path.join('..', 'data_impute_project', 'removed_data', dataset_type)
output_dir = os.path.join('..', 'data_impute_project', 'error_metrics', dataset_type)
ensure_dir(output_dir)

percentages = ['10', '15', '20']
seeds = ['seed1', 'seed2', 'seed3', 'seed4', 'seed5']
algorithms = ['KNN', 'SVM', 'RandomForest', 'RandomForest_MICE', 'HybridKNN_RF']

# Store final results
final_results = []

# Iterating over different combinations of features, algorithms, percentages, and seeds
for combination in combinations_list:
    original_file_path = os.path.join(base_original_path, f"{combination}.xlsx")
    if os.path.exists(original_file_path):
        original_data = pd.read_excel(original_file_path)
        features = original_data.columns[1:]  # Exclude the first column (ID column)

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
                                    missing_mask = missing_data[feature].isna()
                                    mae = calculate_mae_filtered(original_data[feature], imputed_feature, missing_mask)
                                    mape = calculate_mape_filtered(original_data[feature], imputed_feature, missing_mask)
                                    mae_values.append(mae)
                                    mape_values.append(mape)

                        # Average MAE and MAPE
                        mean_mae = np.mean(mae_values) if mae_values else float('inf')
                        mean_mape = np.mean(mape_values) if mape_values else float('inf')

                        # Calculate MAE in parts per thousand (‰)
                        mean_mae_per_thousand = calculate_mae_per_thousand(mean_mae, original_data[feature])

                        # Translate feature set name
                        translated_feature_set = translate_feature_set(feature_set, feature_names)

                        # Format feature name
                        formatted_feature = format_feature_name(feature, feature_names)

                        # Aggregate results
                        final_results.append([combination, formatted_feature, percentage, algorithm, feature_set, translated_feature_set, mean_mae, mean_mape, mean_mae_per_thousand])

# Create DataFrame and save to CSV
df_final = pd.DataFrame(final_results, columns=['Combination', 'Feature', 'Percentage', 'Algorithm', 'FeatureSet', 'TranslatedFeatureSet', 'MAE', 'MAPE', 'MAE (‰)'])
output_file_path = os.path.join(output_dir, 'global_error_analysis.csv')
df_final.to_csv(output_file_path, index=False)

# End timer and print running time
end_time = time.time()
print(f"Final error analysis saved to: {output_file_path}")
print(f"Running time of the script: {end_time - start_time} seconds")
