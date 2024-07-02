import pandas as pd
import numpy as np
import os
import itertools
import time

def ensure_dir(directory):
    """
    Ensure specified directory exists; create it if it does not.
    
    Params:
    directory (str): Path to dir to check/create.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

def collect_imputed_values(original, imputed_knn, imputed_svm, imputed_rf, missing_mask, id_col):
    """
    Collect imputed values along with original values and IDs.
    
    Params:
    original (pd.DataFrame): Original data values with missing values.
    imputed_knn (pd.DataFrame): KNN imputed data values.
    imputed_svm (pd.DataFrame): SVM imputed data values.
    imputed_rf (pd.DataFrame): Random Forest imputed data values.
    missing_mask (pd.Series): Boolean mask indicating where original data had missing values.
    id_col (pd.Series): IDs corresponding to data rows.
    
    Returns:
    pd.DataFrame: DataFrame containing IDs, original values, and imputed values for each method.
    """
    
    data = {
        'ID': id_col[missing_mask].values,
        'OriginalDataValue': original[missing_mask].values,
        'KNN': imputed_knn[missing_mask].values,
        'SVM': imputed_svm[missing_mask].values,
        'RF': imputed_rf[missing_mask].values
    }
    return pd.DataFrame(data)

def detect_outliers_mad(data, threshold=3.0):
    """
    Detect outliers using Median Absolute Deviation (MAD) method.
    
    Parameters:
    data (pd.Series): Data values to check for outliers.
    threshold (float): Threshold to determine what is considered an outlier.
    
    Returns:
    pd.Series: boolean mask indicating which values are outliers.
    """
    median = np.median(data)
    abs_deviation = np.abs(data - median)
    mad = np.median(abs_deviation)
    modified_z_scores = 0.6745 * abs_deviation / mad
    outliers = modified_z_scores > threshold
    return outliers

# Ensure output directory exists
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
algorithms = ['KNN', 'SVM', 'RandomForest']

# Iterate through each combination in combinations list
for combination in combinations_list:
    original_file_path = os.path.join(base_original_path, f"{combination}.xlsx")
    if os.path.exists(original_file_path):
        original_data = pd.read_excel(original_file_path)
        id_col = original_data.iloc[:, 0]
        features = original_data.columns[1:]
        
        # Iterate through each feature
        for target_feature in features:
            # Generate all possible non-empty combinations of the other features
            other_features = [f for f in features if f != target_feature]
            for L in range(len(other_features) + 1):
                for subset in itertools.combinations(other_features, L):
                    # Ensure the order of features in the combination is maintained as per the original data
                    feature_combination = "".join(sorted([target_feature] + list(subset), key=lambda x: features.get_loc(x)))
                    
                    # Iterate through each percentage and seed
                    for percentage in percentages:
                        for seed in seeds:
                            algo_paths = {algo: os.path.join(base_result_path, f"{combination}/{feature_combination}/{percentage}/{seed}/result_data_{algo}.xlsx") for algo in algorithms}
                            missing_file_path = os.path.join(removed_data_base_path, f"{combination}/{feature_combination}/{percentage}/{seed}/missing_data.xlsx")
                            if all(os.path.exists(path) for path in list(algo_paths.values()) + [missing_file_path]):
                                algo_data = {}
                                for algo, path in algo_paths.items():
                                    algo_data[algo] = pd.read_excel(path)
                                missing_data = pd.read_excel(missing_file_path)

                                # Filter rows based on missing values in target feature
                                missing_mask = missing_data[target_feature].isna()
                                if missing_mask.any():
                                    original_values = original_data.loc[missing_mask, [target_feature] + list(subset)]
                                    imputed_values = {algo: data.loc[missing_mask, [target_feature] + list(subset)] for algo, data in algo_data.items()}
                                    id_col_filtered = id_col[missing_mask]
                                    
                                    imputed_values_df = pd.DataFrame({
                                        'ID': id_col_filtered.values,
                                        'OriginalDataValue': original_values[target_feature].values,
                                        'KNN': imputed_values['KNN'][target_feature].values,
                                        'SVM': imputed_values['SVM'][target_feature].values,
                                        'RF': imputed_values['RandomForest'][target_feature].values
                                    })
                                    
                                    imputed_values_df['KNN_Outliers_MAD'] = detect_outliers_mad(imputed_values_df['KNN'])
                                    imputed_values_df['SVM_Outliers_MAD'] = detect_outliers_mad(imputed_values_df['SVM'])
                                    imputed_values_df['RF_Outliers_MAD'] = detect_outliers_mad(imputed_values_df['RF'])
                                    
                                    feature_output_dir = os.path.join(base_output_dir, combination, target_feature, feature_combination, percentage)
                                    ensure_dir(feature_output_dir)
                                    output_file_path = os.path.join(feature_output_dir, f"{seed}_imputed_comparison.xlsx")
                                    imputed_values_df.to_excel(output_file_path, index=False)
                                    print(f"Saved: {output_file_path}")

end_time = time.time()
print(f"Running time of the script: {end_time - start_time} seconds")
