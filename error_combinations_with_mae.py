import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error
from math import sqrt
from itertools import combinations
import os
import time

def calculate_rmse(original, imputed):
    return sqrt(mean_squared_error(original, imputed))

def calculate_nrmse(original, imputed, range_val):
    return calculate_rmse(original, imputed) / range_val if range_val != 0 else 0

def calculate_mae(original, imputed):
    return mean_absolute_error(original, imputed)

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_feature_sets(features, current_feature):
    """Generate all combinations of features excluding the current feature."""
    return [''.join(comb) for i in range(1, len(features)) for comb in combinations(features, i) if current_feature in comb]

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
algorithms = ['KNN', 'BayesianRidge', 'RandomForest']

# Store final results
final_results = []

for combination in combinations_list:
    original_file_path = os.path.join(base_original_path, f"{combination}.xlsx")
    if os.path.exists(original_file_path):
        original_data = pd.read_excel(original_file_path)
        features = original_data.columns.dropna()

        for feature in features:
            feature_sets = get_feature_sets(features, feature)

            for percentage in percentages:
                min_errors = {algo: {'RMSE': float('inf'), 'NRMSE': float('inf'), 'MAE': float('inf'), 'FeatureSet': ''} for algo in algorithms}
                
                for feature_set in feature_sets:
                    for algorithm in algorithms:
                        rmse_values, nrmse_values, mae_values = [], [], []

                        for seed in seeds:
                            result_file_path = os.path.join(base_result_path, f"{combination}/{feature_set}/{percentage}/{seed}/result_data_{algorithm}.xlsx")
                            if os.path.exists(result_file_path):
                                result_data = pd.read_excel(result_file_path)
                                if feature in result_data.columns:
                                    imputed_feature = result_data[feature]
                                    rmse = calculate_rmse(original_data[feature], imputed_feature)
                                    nrmse = calculate_nrmse(original_data[feature], imputed_feature, original_data[feature].max() - original_data[feature].min())
                                    mae = calculate_mae(original_data[feature], imputed_feature)
                                    rmse_values.append(rmse)
                                    nrmse_values.append(nrmse)
                                    mae_values.append(mae)

                        # Average RMSE/NRMSE/MAE and update min_errors if this is the new minimum
                        mean_rmse = np.mean(rmse_values) if rmse_values else float('inf')
                        mean_nrmse = np.mean(nrmse_values) if nrmse_values else float('inf')
                        mean_mae = np.mean(mae_values) if mae_values else float('inf')
                        if mean_rmse < min_errors[algorithm]['RMSE']:
                            min_errors[algorithm]['RMSE'] = mean_rmse
                            min_errors[algorithm]['FeatureSet'] = feature_set
                        if mean_nrmse < min_errors[algorithm]['NRMSE']:
                            min_errors[algorithm]['NRMSE'] = mean_nrmse
                            min_errors[algorithm]['FeatureSet'] = feature_set
                        if mean_mae < min_errors[algorithm]['MAE']:
                            min_errors[algorithm]['MAE'] = mean_mae
                            min_errors[algorithm]['FeatureSet'] = feature_set

                # Aggregate final results
                for algo, error_info in min_errors.items():
                    final_results.append([combination, feature, percentage, algo, error_info['RMSE'], error_info['NRMSE'], error_info['MAE'], error_info['FeatureSet']])

# Create DataFrame and save to CSV
df_final = pd.DataFrame(final_results, columns=['Combination', 'Feature', 'Percentage', 'Algorithm', 'Min RMSE', 'Min NRMSE', 'Min MAE', 'FeatureSet Removal Scenario'])
output_file_path = os.path.join(output_dir, 'min_error_analysis_with_feature_combination_mae.csv')
df_final.to_csv(output_file_path, index=False)

# End the timer and print the running time
end_time = time.time()
print(f"Final minimum error analysis saved to: {output_file_path}")
print(f"Running time of the script: {end_time - start_time} seconds")