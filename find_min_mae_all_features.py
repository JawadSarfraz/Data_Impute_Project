import pandas as pd
import os

# Load Excel file
file_path = 'data_impute_project/error_metrics/min_mae_mape_results.xlsx' 
data = pd.read_excel(file_path)

output_dir = 'data_impute_project/error_metrics/min_mae_all_feature'
os.makedirs(output_dir, exist_ok=True)


# Get unique features
features = data['Feature'].unique()

# Iterate through each feature
for feature in features:
    # Filter data for specific feature
    feature_data = data[data['Feature'] == feature].copy()    
    feature_data = feature_data.drop(columns=['Feature'])
    
    # Find global minimum MAE across all algorithms and combinations for each percentage
    global_min_mae = feature_data.loc[feature_data.groupby('Percentage')['MAE'].idxmin()]
    global_min_mae = global_min_mae.rename(columns={
        'MAE': 'Global Best MAE', 
        'MAPE': 'MAPE at Global Best MAE', 
        'Algorithm': 'Best Algorithm (MAE)', 
        'Combination': 'Best Combination (MAE)',
        'FeatureSet': 'FeatureSet (Best MAE)'
    })
    
    # Find global minimum MAPE across all algorithms and combinations for each percentage
    global_min_mape = feature_data.loc[feature_data.groupby('Percentage')['MAPE'].idxmin()]
    global_min_mape = global_min_mape.rename(columns={
        'MAE': 'MAE at Global Best MAPE', 
        'MAPE': 'Global Best MAPE', 
        'Algorithm': 'Best Algorithm (MAPE)', 
        'Combination': 'Best Combination (MAPE)',
        'FeatureSet': 'FeatureSet (Best MAPE)'
    })
    
    # Merge global minimum MAE and MAPE data into one DataFrame
    combined_best_data = pd.merge(global_min_mae, global_min_mape, on='Percentage', how='outer')
    
    # Select and order necessary columns
    combined_best_data = combined_best_data[[
        'Percentage', 
        'Best Combination (MAE)', 'Best Algorithm (MAE)', 'FeatureSet (Best MAE)', 'Global Best MAE', 'MAPE at Global Best MAE',
        'Best Combination (MAPE)', 'Best Algorithm (MAPE)', 'FeatureSet (Best MAPE)', 'MAE at Global Best MAPE', 'Global Best MAPE'
    ]]
    
    # Save feature-specific results
    feature_output_file = os.path.join(output_dir, f'{feature}_global_min_mae_mape_results.xlsx')
    combined_best_data.to_excel(feature_output_file, index=False)
    print(f"Global best MAE/MAPE results for feature '{feature}' have been saved to {feature_output_file}")

print("All global best MAE/MAPE feature-specific files have been generated successfully.")