import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from math import sqrt
import os

# Initialization of results list
results_summary = []
# Function to calculate RMSE and NRMSE
def calculate_rmse_nrmse(true_values, predicted_values):
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
    return p_value < threshold and abs(corr_factor) > corr_threshold

# Function to handle file existence and load data
def safe_load_data(path):
    if os.path.exists(path):
        return pd.read_excel(path)
    else:
        return None

# Process each combination
def process_combination(combination_name, features):
    data_complete = safe_load_data(f"{combinations_base}/{combination_name}.xlsx")
    corr_results = safe_load_data(f"{correlation_results_base}/{combination_name}_correlation_results.xlsx")
    if data_complete is None or corr_results is None:
        return

    for feature in features:
        for percentage in percentages:
            for variable in data_complete.columns.drop(feature):  # Check every possible variable relationship
                # Check correlation significance from the correlation results
                condition = ((corr_results['Variable 1'] == feature) & (corr_results['Variable 2'] == variable)) | \
                            ((corr_results['Variable 1'] == variable) & (corr_results['Variable 2'] == feature))
                filtered_corr_results = corr_results[condition]
                if not filtered_corr_results.empty and is_significant(filtered_corr_results['P-Value'].iloc[0], filtered_corr_results['Correlation Coefficient'].iloc[0]):
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