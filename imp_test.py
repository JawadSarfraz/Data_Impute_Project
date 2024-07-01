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
    original (pd.Series): Original data values with missing values.
    imputed_knn (pd.Series): KNN imputed data values.
    imputed_svm (pd.Series): SVM imputed data values.
    imputed_rf (pd.Series): Random Forest imputed data values.
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
base_output_dir = 'data_impute_project/TEST5'
ensure_dir(base_output_dir)

start_time = time.time()

# Setup paths and variables
base_original_path = 'data_impute_project/combinations/terrestrial_mammals'
combinations_list = ['combination_1_ABCD']
base_result_path = 'data_impute_project/algorithm_result/terrestrial_mammals'
removed_data_base_path = 'data_impute_project/removed_data/terrestrial_mammals'
percentages = ['20' ]
seeds = ['seed2']
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
                    feature_combination = "".join([target_feature] + list(subset))
                    
                    # Iterate through each percentage and seed
                    for percentage in percentages:
                        for seed in seeds:
                            algo_paths = {algo: os.path.join(base_result_path, f"{combination}/{target_feature}/{percentage}/{seed}/result_data_{algo}.xlsx") for algo in algorithms}
                            missing_file_path = os.path.join(removed_data_base_path, f"{combination}/{target_feature}/{percentage}/{seed}/missing_data.xlsx")
                            if all(os.path.exists(path) for path in list(algo_paths.values()) + [missing_file_path]):
                                algo_data = {}
                                #algo_data = {algo: pd.read_excel(path) for algo, path in algo_paths.items()}
                                # Iterate over each algorithm and its corresponding file path
                                for algo, path in algo_paths.items():
                                    # Read the result data file for the current algorithm
                                    if feature_combination == "CABD" and target_feature == "C":
                                        print(pd.read_excel(path))
                                        #print(target_feature)
                                        exit()
                                    algo_data[algo] = pd.read_excel(path)
                                missing_data = pd.read_excel(missing_file_path)

                                # Filter rows based on missing values in target feature
                                missing_mask = missing_data[target_feature].isna()
                                if missing_mask.any():
                                    original_values = original_data.loc[missing_mask, target_feature]
                                    imputed_values = {algo: data.loc[missing_mask, target_feature] for algo, data in algo_data.items()}
                                    id_col_filtered = id_col[missing_mask]
                                    
                                    imputed_values_df = collect_imputed_values(
                                        original_values,
                                        imputed_values['KNN'],
                                        imputed_values['SVM'],
                                        imputed_values['RandomForest'],
                                        missing_mask,
                                        id_col_filtered
                                    )
                                    
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

# import pandas as pd
# import numpy as np
# import os
# import itertools
# import time

# def ensure_dir(directory):
#     """
#     Ensure specified directory exists; create it if it does not.
    
#     Params:
#     directory (str): Path to dir to check/create.
#     """
#     if not os.path.exists(directory):
#         os.makedirs(directory)

# def collect_imputed_values(original, imputed_knn, imputed_svm, imputed_rf, id_col):
#     """
#     Collect imputed values along with original values and IDs.
    
#     Params:
#     original (pd.Series): Original data values with missing values.
#     imputed_knn (pd.Series): KNN imputed data values.
#     imputed_svm (pd.Series): SVM imputed data values.
#     imputed_rf (pd.Series): Random Forest imputed data values.
#     id_col (pd.Series): IDs corresponding to data rows.
    
#     Returns:
#     pd.DataFrame: DataFrame containing IDs, original values, and imputed values for each method.
#     """
#     data = {
#         'ID': id_col.values,
#         'OriginalDataValue': original.values,
#         'KNN': imputed_knn.values,
#         'SVM': imputed_svm.values,
#         'RF': imputed_rf.values
#     }
#     return pd.DataFrame(data)

# def detect_outliers_mad(data, threshold=3.0):
#     """
#     Detect outliers using Median Absolute Deviation (MAD) method.
    
#     Parameters:
#     data (pd.Series): Data values to check for outliers.
#     threshold (float): Threshold to determine what is considered an outlier.
    
#     Returns:
#     pd.Series: boolean mask indicating which values are outliers.
#     """
#     median = np.median(data)
#     abs_deviation = np.abs(data - median)
#     mad = np.median(abs_deviation)
#     modified_z_scores = 0.6745 * abs_deviation / mad
#     outliers = modified_z_scores > threshold
#     return outliers

# # Ensure output directory exists
# base_output_dir = 'data_impute_project/TEST5'
# ensure_dir(base_output_dir)

# start_time = time.time()

# # Setup paths and variables
# base_original_path = 'data_impute_project/combinations/terrestrial_mammals'
# combinations_list = ['combination_1_ABCD']
# base_result_path = 'data_impute_project/algorithm_result/terrestrial_mammals'
# removed_data_base_path = 'data_impute_project/removed_data/terrestrial_mammals'
# percentages = ['10', '15']
# seeds = ['seed1', 'seed2']
# algorithms = ['KNN', 'SVM', 'RandomForest']

# # Iterate through each combination in combinations list
# for combination in combinations_list:
#     original_file_path = os.path.join(base_original_path, f"{combination}.xlsx")
#     if os.path.exists(original_file_path):
#         original_data = pd.read_excel(original_file_path)
#         id_col = original_data.iloc[:, 0]
#         features = original_data.columns[1:]
        
#         # Iterate through each feature
#         for target_feature in features:
#             # Generate all possible non-empty combinations of other features
#             other_features = [f for f in features if f != target_feature]
#             for L in range(1, len(other_features) + 1):
#                 for subset in itertools.combinations(other_features, L):
#                     feature_combination = "".join(list(subset))
                    
#                     # Iterate through each percentage and seed
#                     for percentage in percentages:
#                         for seed in seeds:
#                             algo_paths = {algo: os.path.join(base_result_path, f"{combination}/{target_feature}/{percentage}/{seed}/result_data_{algo}.xlsx") for algo in algorithms}
#                             missing_file_path = os.path.join(removed_data_base_path, f"{combination}/{target_feature}/{percentage}/{seed}/missing_data.xlsx")
                            
#                             if all(os.path.exists(path) for path in list(algo_paths.values()) + [missing_file_path]):
#                                 algo_data = {algo: pd.read_excel(path) for algo, path in algo_paths.items()}
#                                 missing_data = pd.read_excel(missing_file_path)
                                
#                                 # Filter rows based on missing values in target feature
#                                 missing_mask = missing_data[target_feature].isna()
#                                 if missing_mask.any():
#                                     original_values = original_data.loc[missing_mask, target_feature]
#                                     imputed_values = {algo: data.loc[missing_mask, target_feature] for algo, data in algo_data.items()}
#                                     id_col_filtered = id_col[missing_mask]
                                    
#                                     imputed_values_df = collect_imputed_values(
#                                         original_values,
#                                         imputed_values['KNN'],
#                                         imputed_values['SVM'],
#                                         imputed_values['RandomForest'],
#                                         id_col_filtered
#                                     )
                                    
#                                     imputed_values_df['KNN_Outliers_MAD'] = detect_outliers_mad(imputed_values_df['KNN'])
#                                     imputed_values_df['SVM_Outliers_MAD'] = detect_outliers_mad(imputed_values_df['SVM'])
#                                     imputed_values_df['RF_Outliers_MAD'] = detect_outliers_mad(imputed_values_df['RF'])
                                    
#                                     feature_output_dir = os.path.join(base_output_dir, combination, target_feature, feature_combination, percentage)
#                                     ensure_dir(feature_output_dir)
#                                     output_file_path = os.path.join(feature_output_dir, f"{seed}_imputed_comparison.xlsx")
#                                     imputed_values_df.to_excel(output_file_path, index=False)
#                                     print(f"Saved: {output_file_path}")

# end_time = time.time()
# print(f"Running time of the script: {end_time - start_time} seconds")
