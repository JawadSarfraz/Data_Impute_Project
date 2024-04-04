import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
from math import sqrt
import os

def calculate_rmse(original, imputed):
    return sqrt(mean_squared_error(original, imputed))

def calculate_nrmse(original, imputed, range_val):
    return calculate_rmse(original, imputed) / range_val if range_val != 0 else 0

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Setup
base_original_path = 'data_impute_project/combinations/terrestrial_mammals'
combinations_list = ['combination_1_ABCD', 'combination_2_ABCDE', 'combination_3_ABCDF']
base_result_path = 'data_impute_project/algorithm_result/terrestrial_mammals'
output_dir = 'data_impute_project/error_metrics'
ensure_dir(output_dir)
percentages = ['10', '15','20']
seeds = ['seed1', 'seed2', 'seed3','seed4','seed5']
algorithms = ['KNN', 'MICE', 'RandomForest']

# Main Loop
for combination in combinations_list:
    original_file_path = f'{base_original_path}/{combination}.xlsx'
    if os.path.exists(original_file_path):
        original_data = pd.read_excel(original_file_path)
        features = original_data.columns.dropna()
        
        for feature in features:
            for percentage in percentages:
                aggregated_results = []
                
                for algorithm in algorithms:
                    # Initialize lists to store RMSE and NRMSE values for averaging
                    rmse_values = []
                    nrmse_values = []

                    for seed in seeds:
                        result_file_path = f'{base_result_path}/{combination}/{feature}/{percentage}/{seed}/result_data_{algorithm}.xlsx'
                        if os.path.exists(result_file_path):
                            result_data = pd.read_excel(result_file_path)
                            if feature in result_data:
                                imputed_feature = result_data[feature]
                                rmse = calculate_rmse(original_data[feature], imputed_feature)
                                nrmse = calculate_nrmse(original_data[feature], imputed_feature, original_data[feature].max() - original_data[feature].min())
                                
                                # Append the calculated values to their respective lists
                                rmse_values.append(rmse)
                                nrmse_values.append(nrmse)
                    
                    # Calculate mean RMSE and NRMSE across all seeds
                    mean_rmse = np.mean(rmse_values) if rmse_values else None
                    mean_nrmse = np.mean(nrmse_values) if nrmse_values else None
                    aggregated_results.append([combination, feature, percentage, algorithm, mean_rmse, mean_nrmse])
                
                # Save aggregated results to CSV
                df_aggregated_results = pd.DataFrame(aggregated_results, columns=['Combination', 'Feature', 'Percentage', 'Algorithm', 'Mean RMSE', 'Mean NRMSE'])
                output_file_path = f'{output_dir}/{combination}_{feature}_{percentage}_mean_errors.csv'
                df_aggregated_results.to_csv(output_file_path, index=False)