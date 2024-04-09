import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
from math import sqrt
import os
from itertools import combinations

def calculate_rmse(original, imputed):
    return sqrt(mean_squared_error(original, imputed))

def calculate_nrmse(original, imputed, range_val):
    return calculate_rmse(original, imputed) / range_val if range_val != 0 else 0

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_feature_combinations(features):
    """Generate all combinations of features excluding single feature scenarios."""
    all_combinations = []
    for r in range(1, len(features) + 1):
        for combo in combinations(features, r):
            all_combinations.append(''.join(combo))
    return all_combinations

# Setup
base_original_path = 'data_impute_project/combinations/terrestrial_mammals'
combinations_list = ['combination_1_ABCD', 'combination_2_ABCDE', 'combination_3_ABCDF']
base_result_path = 'data_impute_project/algorithm_result/terrestrial_mammals'
output_dir = 'data_impute_project/error_metrics'
ensure_dir(output_dir)
percentages = ['10', '15', '20']
seeds = ['seed1', 'seed2', 'seed3', 'seed4', 'seed5']
algorithms = ['KNN', 'MICE', 'RandomForest']

final_results = []

for combination in combinations_list:
    original_file_path = os.path.join(base_original_path, f"{combination}.xlsx")
    if os.path.exists(original_file_path):
        original_data = pd.read_excel(original_file_path)
        features_in_combination = original_data.columns.dropna()
        
        # Generate all possible feature combinations for the current combination
        feature_combinations = get_feature_combinations(features_in_combination)

        for percentage in percentages:
            for feature_comb in feature_combinations:
                for algorithm in algorithms:
                    rmse_values, nrmse_values = [], []

                    for seed in seeds:
                        result_file_path = os.path.join(base_result_path, f"{combination}/{feature_comb}/{percentage}/{seed}/result_data_{algorithm}.xlsx")
                        if os.path.exists(result_file_path):
                            result_data = pd.read_excel(result_file_path)
                            for feature in feature_comb:
                                if feature in result_data.columns:
                                    imputed_feature = result_data[feature]
                                    original_feature = original_data[feature]
                                    print(original_feature)
                                    rmse = calculate_rmse(original_feature, imputed_feature)
                                    nrmse = calculate_nrmse(original_feature, imputed_feature, original_feature.max() - original_feature.min())
                                    rmse_values.append(rmse)
                                    nrmse_values.append(nrmse)

                    # Calculate mean RMSE and NRMSE for the current feature combination
                    mean_rmse, mean_nrmse = np.mean(rmse_values), np.mean(nrmse_values)
                    final_results.append([combination, feature_comb, percentage, algorithm, mean_rmse, mean_nrmse])

# Convert final results to DataFrame and save to CSV
df_final = pd.DataFrame(final_results, columns=['Combination', 'FeatureComb', 'Percentage', 'Algorithm', 'Mean RMSE', 'Mean NRMSE'])
output_file_path = os.path.join(output_dir, 'final_error_analysis_feature_sets.csv')
df_final.to_csv(output_file_path, index=False)
print(f"Final error analysis across feature sets saved to: {output_file_path}")