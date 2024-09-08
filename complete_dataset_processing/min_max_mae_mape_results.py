import os
import pandas as pd

# List of valid datasets
datasets = ["bird", "fish", "human", "mammals_without_humans", "marine_mammals", 
            "terr_herb_and_marine_mammals", "terrestrial_herbivorous_mammals", "terrestrial_mammals"]

# Prompt user for dataset type
dataset_type = input(f"Enter the dataset type {datasets}: ").strip()

if dataset_type not in datasets:
    raise ValueError("Invalid dataset type entered. Please try again.")

# Construct file path based on dataset type
file_path = os.path.join("..", "data_impute_project", "error_metrics", dataset_type, 'error_analysis_with_all_featuresets.csv')

# Check if file exists
if not os.path.exists(file_path):
    raise FileNotFoundError(f"No error metrics file found for {dataset_type}. Please check the file path or select another dataset.")

data = pd.read_csv(file_path)

# Create list to store results
results = []

# Iterate through each combination and feature
combinations = data['Combination'].unique()
for combination in combinations:
    # Get unique features for current combination
    features = data[data['Combination'] == combination]['Feature'].unique()
    for feature in features:
        # Filter data for specific combination and feature
        filtered_data = data[(data['Combination'] == combination) & (data['Feature'] == feature)]
        
        # Get unique algorithms and percentages
        algorithms = filtered_data['Algorithm'].unique()
        percentages = filtered_data['Percentage'].unique()
        
        for algorithm in algorithms:
            for percentage in percentages:
                # Filter data for specific algorithm and percentage
                algo_data = filtered_data[(filtered_data['Algorithm'] == algorithm) & (filtered_data['Percentage'] == percentage)]
                
                # Find row with minimum MAE
                min_mae_row = algo_data.loc[algo_data['MAE'].idxmin()]
                
                # Append result to list
                results.append({
                    'Combination': combination,
                    'Feature': feature,
                    'Algorithm': algorithm,
                    'Percentage': percentage,
                    'FeatureSet': min_mae_row['FeatureSet'],
                    'Min MAE': min_mae_row['MAE'],
                    'MAPE at Min MAE': min_mae_row['MAPE']
                })

# Convert results list to DataFrame
results_df = pd.DataFrame(results)

# Construct output file path based on dataset type
output_file = os.path.join("..", "data_impute_project", "error_metrics", dataset_type, f'test_min_mae_mape_results.xlsx')

# Save results to Excel file
results_df.to_excel(output_file, index=False)

print(f"Results have been saved to {output_file}")
