import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from math import sqrt
import os

# Initialization of results list
results_summary = []
# Function to calculate RMSE and NRMSE
def calculate_rmse_nrmse(true_values, predicted_values):
    """
    Calculates root mean squared error (RMSE) and normalized root mean squared error (NRMSE) between true and predicted values.
    
    Params:
    true_values: True values are actual values of target variable.
    predicted_values: Predicted values are the values that model has predicted
    
    return: returns two values: root mean squared error (rmse) and normalized root mean squared error (nrmse).
    """
    rmse = sqrt(mean_squared_error(true_values, predicted_values))
    nrmse = rmse / (true_values.max() - true_values.min())
    return rmse, nrmse

# Def base directory and setup paths
base_dir = 'data_impute_project'
combinations_base = f'{base_dir}/combinations/terrestrial_mammals'
correlation_results_base = f'{base_dir}/corr_combinations/terrestrial_mammals'
missing_data_base = f'{base_dir}/removed_data/terrestrial_mammals'
output_base = f'{base_dir}/corr_test/terrestrial_mammals'

# List of combination files and features present in each
combination_features = {
    "combination_1_ABCD": ["A", "B", "C", "D"],
    "combination_2_ABCDE": ["A", "B", "C", "D", "E"],
    "combination_3_ABCDF": ["A", "B", "C", "D", "F"]
}

# Percentage levels and seeds
percentages = ['10', '15', '20']
seeds = ['seed1', 'seed2', 'seed3', 'seed4', 'seed5']

# Function to check if the correlation is significant
def is_significant(p_value, corr_factor, threshold=0.05, corr_threshold=0.5):
    """
    Determines if statistical test result is significant based on the p-value and correlation factor
    compared to specified thresholds.
    
    Params:
    p_value: It represents p-value obtained from statistical test.
    corr_factor: its the measures the strength and direction of a relationship between two variables.
    threshold: represents significance level for determining statistical significance.
    corr_threshold: it represents minimum absolute value of correlation factor that is considered significant. If absolute
    value of correlation factor is greater than this threshold, and p-value is less than threshold(0.05),
    
    return: a boolean value, it checks if p-value is less than given threshold and if absolute value of correlation
    factor is greater than another threshold. If both conditions are met, it returns True; otherwise False.
    """
    return p_value < threshold and abs(corr_factor) > corr_threshold

# Function to handle file existence and load data
def safe_load_data(path):
    """
    Reads Excel file from specified path if it exists, otherwise it returns `None`.
    
    Param:
    path: its file path that need to load.
    
    return: If file exists, function will return data loaded from Excel file using pandas `read_excel` function. 
    If file does not exist, the function will return `None`.
    """
    if os.path.exists(path):
        return pd.read_excel(path)
    else:
        return None

# Process each combination
def process_combination(combination_name, features):
    """
    The function iterates through combinations of features and percentages
    to check for significant correlations and calculate RMSE and NRMSE values.
    
    Params:
    combination_name: It is used to load relevant data files and results associated with that specific combination for further
    processing and analysis
    features: Its features present in file contains combinations. Its been iterated over all features to calc RMSE.
    
    return: The function returns list of dictionaries containing summary of
    results for each combination, feature, feature relation, percentage, RMSE, and NRMSE.
    """

    data_complete = safe_load_data(f"{combinations_base}/{combination_name}.xlsx")
    corr_results = safe_load_data(f"{correlation_results_base}/{combination_name}_correlation_results.xlsx")
    if data_complete is None or corr_results is None:
        return

    # Iterating over different combinations of features, percentages and
    # seeds to check for significant correlations and calculate RMSE and NRMSE values.
    for feature in features:
        for percentage in percentages:
            for variable in data_complete.columns.drop(feature):  # Check every possible variable relationship
                # Check correlation significance from the correlation results
                condition = ((corr_results['Variable 1'] == feature) & (corr_results['Variable 2'] == variable)) | \
                            ((corr_results['Variable 1'] == variable) & (corr_results['Variable 2'] == feature))
                filtered_corr_results = corr_results[condition]
                if not filtered_corr_results.empty and is_significant(filtered_corr_results['P-Value'].iloc[0], filtered_corr_results['Correlation Coefficient'].iloc[0]):
                    # This list is used to store temporary results, specifically
                    # RMSE and NRMSE values calculated for each seed iteration within nested loops
                    temp_results = []
                    for seed in seeds:
                        missing_data_path = f"{missing_data_base}/{combination_name}/{feature}/{percentage}/{seed}/missing_data.xlsx"
                        data_missing = safe_load_data(missing_data_path)
                        if data_missing is None:
                            continue
                        result, _ = impute_and_save(data_complete, data_missing, corr_results, feature, variable, combination_name, percentage, seed)
                        if result is not None:
                            rmse, nrmse = calculate_rmse_nrmse(data_complete[feature], result[feature])
                            temp_results.append((rmse, nrmse))
                    
                    # Calculate mean RMSE and NRMSE after all seeds are processed
                    if temp_results:
                        mean_rmse = pd.DataFrame(temp_results, columns=['RMSE', 'NRMSE']).mean()
                        results_summary.append({
                            "Combination": combination_name,
                            "Feature": feature,
                            "FeatureRelation": variable,
                            "Percentage": percentage,
                            "RMSE": mean_rmse['RMSE'],
                            "NRMSE": mean_rmse['NRMSE']
                        })

# Function to impute and save data
def impute_and_save(data_complete, data_missing, corr_results, feature, variable, combination_name, percentage, seed):
    """
    The function takes in complete and missing data and correlation results
    parameters to impute missing values using linear regression and save results to Excel file.
    
    Params:
    data_complete: its complete dataset that contains all data including missing values for imputation
    data_missing: `data_missing` is DataFrame containing dataset with missing values that
    we want to impute. It includes feature  for which we perform imputation.
    corr_results: contains correlation results between different variables.
    feature: refers to column in dataset that contains missing values which we wanna impute.
    variable: used to impute missing values in `feature` column of  dataset. It is column in
    dataset that will be used as a predictor to estimate the missing values in feature.
    combination_name: combination of features used for imputation.
    percentage: percentage of missing values that were imputed in dataset.
    seed: The `seed` parameter used to set the random seed
    for reproducibility in imputation process. Setting a seed ensures that same random values
    are generated each time the function is run with same seed value.

    :return: The function `impute_and_save` returns a tuple containing the result DataFrame after
    imputation and the output filename where the imputed data is saved. If there is no correlation data
    found for the specified feature with the variable, it returns `None` along with a message indicating
    the absence of correlation data. If the correlation is not significant based on the p-value and
    correlation coefficient, it returns None
    """
    # Check if correlation significant for both cases: feature as Variable 1 or Variable 2
    condition = ((corr_results['Variable 1'] == feature) & (corr_results['Variable 2'] == variable)) | \
                ((corr_results['Variable 1'] == variable) & (corr_results['Variable 2'] == feature))
    filtered_corr_results = corr_results[condition]

    if filtered_corr_results.empty:
        return None, f"No correlation data found for {feature} with {variable}"

    # Select relevant row if multiple rows, prioritize feature as Variable 1
    if len(filtered_corr_results) > 1:
        row = filtered_corr_results[filtered_corr_results['Variable 1'] == feature]
        if row.empty:
            row = filtered_corr_results.iloc[0]  # Fallback to any available row
    else:
        row = filtered_corr_results.iloc[0]

    if not is_significant(row['P-Value'], row['Correlation Coefficient']):
        return None, f"Imputation not performed for {feature} with {variable} due to low correlation or high p-value."
    
    # Prepare data
    train = data_missing.dropna(subset=[feature]).copy()
    test = data_missing[data_missing[feature].isnull()].copy()
    
    # Train and predict
    model = LinearRegression()
    model.fit(train[[variable]], train[feature])
    predicted_values = model.predict(test[[variable]])
    test.loc[:, feature] = test[feature].fillna(pd.Series(predicted_values, index=test.index))
    
    # Combine the train and test datasets into result DataFrame
    result = pd.concat([train, test]).sort_index()
    
    # Define output filename and path
    output_path = f"{output_base}/{combination_name}/{feature}/{percentage}"
    os.makedirs(output_path, exist_ok=True)
    output_filename = f"{seed}_imputed_by_{variable}.xlsx"
    result.to_excel(os.path.join(output_path, output_filename), index=False)
    
    return result, output_filename

# Export summary results to Excel
def export_results_to_excel():
    df = pd.DataFrame(results_summary)
    output_path = os.path.join(output_base, "imputation_summary.xlsx")
    df.to_excel(output_path, index=False)

# Run process for each combination and its features
for combination, features in combination_features.items():
    process_combination(combination, features)
export_results_to_excel()