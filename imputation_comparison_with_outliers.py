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

# def collect_imputed_values(original, imputed_knn, imputed_svm, imputed_rf, missing_mask, id_col):
#     """
#     Collect imputed values along with original values and the IDs.
    
#     Parames:
#     original (pd.Series): Original data values with missing values.
#     imputed_knn (pd.Series): KNN imputed data values.
#     imputed_svm (pd.Series): SVM imputed data values.
#     imputed_rf (pd.Series): Random Forest imputed data values.
#     missing_mask (pd.Series): Boolean mask indicating where original data had missing values.
#     id_col (pd.Series): IDs corresponding to the data rows.
    
#     Returns:
#     pd.DataFrame: DataFrame containing IDs, original values, and imputed values for each method.
#     """

#     data = {
#         'ID': id_col[missing_mask],
#         'OriginalDataValue': original[missing_mask],
#         'KNN': imputed_knn[missing_mask],
#         'SVM': imputed_svm[missing_mask],
#         'RF': imputed_rf[missing_mask]
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
#     median = np.median(data) # Calculate median of data
#     abs_deviation = np.abs(data - median) #Calculate absolute deviation from median
#     mad = np.median(abs_deviation) # Calculate median of absolute deviations
#     modified_z_scores = 0.6745 * abs_deviation / mad #  Calculate modified Z-scores
#     outliers = modified_z_scores > threshold # Identify outliers based on the threshold
#     return outliers

# # Ensure output directory exists
# base_output_dir = 'data_impute_project/imputation_comparison'
# ensure_dir(base_output_dir)

# start_time = time.time()

# # Setup paths and variables
# base_original_path = 'data_impute_project/combinations/terrestrial_mammals'
# combinations_list = ['combination_1_ABCD','combination_2_ABCDE', 'combination_3_ABCDF']
# base_result_path = 'data_impute_project/algorithm_result/terrestrial_mammals'
# removed_data_base_path = 'data_impute_project/removed_data/terrestrial_mammals'
# percentages = ['10', '15', '20']
# seeds = ['seed1', 'seed2', 'seed3', 'seed4', 'seed5']

# # Iterate through each combination in the combinations list
# for combination in combinations_list:
#     original_file_path = os.path.join(base_original_path, f"{combination}.xlsx")
#     if os.path.exists(original_file_path): # Check if original file exists
#         original_data = pd.read_excel(original_file_path)
#         id_col = original_data.iloc[:, 0]  # As first column is the ID column
#         features = original_data.columns[1:]  # Exclude the ID column
        
#         # Generate all possible non-empty combinations of the features
#         for L in range(1, len(features) + 1):
#             for subset in itertools.combinations(features, L):
#                 feature_combination = "".join(subset)  # Join features
                
#                 # Iterate through each percentage and seed
#                 for percentage in percentages:
#                     for seed in seeds:
#                         knn_path = os.path.join(base_result_path, f"{combination}/{feature_combination}/{percentage}/{seed}/result_data_KNN.xlsx")
#                         svm_path = os.path.join(base_result_path, f"{combination}/{feature_combination}/{percentage}/{seed}/result_data_SVM.xlsx")
#                         rf_path = os.path.join(base_result_path, f"{combination}/{feature_combination}/{percentage}/{seed}/result_data_RandomForest.xlsx")
#                         missing_file_path = os.path.join(removed_data_base_path, f"{combination}/{feature_combination}/{percentage}/{seed}/missing_data.xlsx")
                        
#                         # Def paths for imputed data and missing data files
#                         if all(os.path.exists(path) for path in [knn_path, svm_path, rf_path, missing_file_path]):
#                             knn_data = pd.read_excel(knn_path)
#                             svm_data = pd.read_excel(svm_path)
#                             rf_data = pd.read_excel(rf_path)
#                             missing_data = pd.read_excel(missing_file_path)
                            
#                             # Check if all necessary files exist
#                             if all(feature in knn_data.columns for feature in subset) and all(feature in svm_data.columns for feature in subset) and all(feature in rf_data.columns for feature in subset):
#                                 # Collect imputed values for each feature in the subset
#                                 original_values = original_data[list(subset)]
#                                 knn_values = knn_data[list(subset)]
#                                 svm_values = svm_data[list(subset)]
#                                 rf_values = rf_data[list(subset)]
#                                 # Correctly identifying missing values
#                                 missing_mask = missing_data[list(subset)].isna().any(axis=1)
                                
#                                 imputed_values_df = collect_imputed_values(
#                                     original_values[subset[0]],
#                                     knn_values[subset[0]],
#                                     svm_values[subset[0]],
#                                     rf_values[subset[0]],
#                                     missing_mask,
#                                     id_col # Collecting IDs corresponding to missing values
#                                 )

#                                 # Detect outliers using MAD method
#                                 imputed_values_df['KNN_Outliers_MAD'] = detect_outliers_mad(imputed_values_df['KNN'])
#                                 imputed_values_df['SVM_Outliers_MAD'] = detect_outliers_mad(imputed_values_df['SVM'])
#                                 imputed_values_df['RF_Outliers_MAD'] = detect_outliers_mad(imputed_values_df['RF'])
                                
#                                 # Create the directory structure and save the file
#                                 feature_output_dir = os.path.join(base_output_dir, combination, feature_combination, percentage)
#                                 ensure_dir(feature_output_dir)
#                                 output_file_path = os.path.join(feature_output_dir, f"{seed}_imputed_comparison.xlsx")
#                                 imputed_values_df.to_excel(output_file_path, index=False)
#                                 print(f"Saved: {output_file_path}")

# end_time = time.time() # End the time/clock
# print(f"Running time of the script: {end_time - start_time} seconds")

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
    Collect imputed values along with original values and the IDs.
    
    Params:
    original (pd.Series): Original data values with missing values.
    imputed_knn (pd.Series): KNN imputed data values.
    imputed_svm (pd.Series): SVM imputed data values.
    imputed_rf (pd.Series): Random Forest imputed data values.
    missing_mask (pd.Series): Boolean mask indicating where original data had missing values.
    id_col (pd.Series): IDs corresponding to the data rows.
    
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
base_output_dir = 'data_impute_project/TEST3'
ensure_dir(base_output_dir)

start_time = time.time()

# Setup paths and variables
base_original_path = 'data_impute_project/combinations/terrestrial_mammals'
combinations_list = ['combination_1_ABCD']
base_result_path = 'data_impute_project/algorithm_result/terrestrial_mammals'
removed_data_base_path = 'data_impute_project/removed_data/terrestrial_mammals'
percentages = ['10', '15', '20']
seeds = ['seed1']

# Iterate through each combination in the combinations list
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
                            knn_path = os.path.join(base_result_path, f"{combination}/{target_feature}/{percentage}/{seed}/result_data_KNN.xlsx")
                            svm_path = os.path.join(base_result_path, f"{combination}/{target_feature}/{percentage}/{seed}/result_data_SVM.xlsx")
                            rf_path = os.path.join(base_result_path, f"{combination}/{target_feature}/{percentage}/{seed}/result_data_RandomForest.xlsx")
                            missing_file_path = os.path.join(removed_data_base_path, f"{combination}/{target_feature}/{percentage}/{seed}/missing_data.xlsx")
                            
                            if all(os.path.exists(path) for path in [knn_path, svm_path, rf_path, missing_file_path]):
                                knn_data = pd.read_excel(knn_path)
                                svm_data = pd.read_excel(svm_path)
                                rf_data = pd.read_excel(rf_path)
                                missing_data = pd.read_excel(missing_file_path)
                                
                                # Filter rows based on missing values in the target feature
                                missing_mask = missing_data[target_feature].isna()
                                if missing_mask.any():
                                    original_values = original_data.loc[missing_mask, [target_feature] + list(subset)]
                                    knn_values = knn_data.loc[missing_mask, [target_feature] + list(subset)]
                                    svm_values = svm_data.loc[missing_mask, [target_feature] + list(subset)]
                                    rf_values = rf_data.loc[missing_mask, [target_feature] + list(subset)]
                                    id_col_filtered = id_col[missing_mask]
                                    
                                    imputed_values_df = collect_imputed_values(
                                        original_values[target_feature],
                                        knn_values[target_feature],
                                        svm_values[target_feature],
                                        rf_values[target_feature],
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
