import pandas as pd
import numpy as np
import os
import time

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Function to collect the imputed values along with the original values and the ID
def collect_imputed_values(original, imputed_knn, imputed_svm, imputed_rf, missing_mask, id_col):
    data = {
        'ID': id_col[missing_mask],
        'OriginalDataValue': original[missing_mask],
        'KNN': imputed_knn[missing_mask],
        'SVM': imputed_svm[missing_mask],
        'RF': imputed_rf[missing_mask]
    }
    return pd.DataFrame(data)

# Ensure the output directory exists
base_output_dir = 'data_impute_project/imputation_comparison'
ensure_dir(base_output_dir)

start_time = time.time()

# Setup paths and variables
base_original_path = 'data_impute_project/combinations/terrestrial_mammals'
combinations_list = ['combination_1_ABCD', 'combination_2_ABCDE', 'combination_3_ABCDF']
base_result_path = 'data_impute_project/algorithm_result/terrestrial_mammals'
removed_data_base_path = 'data_impute_project/removed_data/terrestrial_mammals'
percentages = ['10', '15', '20']
seeds = ['seed1', 'seed2', 'seed3', 'seed4', 'seed5']

for combination in combinations_list:
    original_file_path = os.path.join(base_original_path, f"{combination}.xlsx")
    if os.path.exists(original_file_path):
        original_data = pd.read_excel(original_file_path)
        id_col = original_data.iloc[:, 0]  # Assuming the first column is the ID column
        features = original_data.columns[1:]  # Exclude the ID column
        
        for feature in features:
            for percentage in percentages:
                for seed in seeds:
                    knn_path = os.path.join(base_result_path, f"{combination}/{feature}/{percentage}/{seed}/result_data_KNN.xlsx")
                    svm_path = os.path.join(base_result_path, f"{combination}/{feature}/{percentage}/{seed}/result_data_SVM.xlsx")
                    rf_path = os.path.join(base_result_path, f"{combination}/{feature}/{percentage}/{seed}/result_data_RandomForest.xlsx")
                    missing_file_path = os.path.join(removed_data_base_path, f"{combination}/{feature}/{percentage}/{seed}/missing_data.xlsx")
                    
                    if all(os.path.exists(path) for path in [knn_path, svm_path, rf_path, missing_file_path]):
                        knn_data = pd.read_excel(knn_path)
                        svm_data = pd.read_excel(svm_path)
                        rf_data = pd.read_excel(rf_path)
                        missing_data = pd.read_excel(missing_file_path)
                        
                        if feature in knn_data.columns and feature in svm_data.columns and feature in rf_data.columns:
                            original_feature = original_data[feature]
                            missing_mask = missing_data[feature].isna()
                            
                            imputed_values_df = collect_imputed_values(
                                original_feature,
                                knn_data[feature],
                                svm_data[feature],
                                rf_data[feature],
                                missing_mask,
                                id_col
                            )
                            
                            # Create the directory structure and save the file
                            feature_output_dir = os.path.join(base_output_dir, combination, feature, percentage)
                            ensure_dir(feature_output_dir)
                            output_file_path = os.path.join(feature_output_dir, f"{seed}_imputed_comparison.xlsx")
                            imputed_values_df.to_excel(output_file_path, index=False)
                            print(f"Saved: {output_file_path}")

end_time = time.time()
print(f"Running time of the script: {end_time - start_time} seconds")