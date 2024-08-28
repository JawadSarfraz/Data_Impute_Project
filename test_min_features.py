import pandas as pd

# Load data
file_path = 'data_impute_project/error_metrics/min_mae_mape_results.xlsx'
data = pd.read_excel(file_path)

# List of unique features in the dataset
unique_features = data['Feature'].unique()
combined_data = pd.DataFrame()

for feature in unique_features:
    # Filter data for specific feature
    feature_data = data[data['Feature'] == feature]
    
    # Find rows with minimum MAE for each percentage
    min_mae_rows = feature_data.loc[feature_data.groupby('Percentage')['Min MAE'].idxmin()]
        
    # Concatenate data to combined DataFrame
    combined_data = pd.concat([combined_data, min_mae_rows], ignore_index=True)

# Save combined data to single Excel file
combined_file_path = 'data_impute_project/error_metrics/min_mae_mape_all_features_combined.xlsx'
combined_data.to_excel(combined_file_path, index=False)

print(f"Combined file saved as {combined_file_path}")
