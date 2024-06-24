import pandas as pd
import os

# Load CSV file
file_path = 'data_impute_project/error_metrics/error_analysis_with_all_featureset.csv'
data = pd.read_csv(file_path)

# Create a list to store the results
results = []

# Iterate through each combination and feature
combinations = data['Combination'].unique()
for combination in combinations:
    # Get unique features for the current combination
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
                
                # Append result to the list
                results.append({
                    'Combination': combination,
                    'Feature': feature,
                    'Algorithm': algorithm,
                    'Percentage': percentage,
                    'FeatureSet': min_mae_row['FeatureSet'],
                    'Min MAE': min_mae_row['MAE']
                })

# Convert results list to DataFrame
results_df = pd.DataFrame(results)

# Save results
output_file = 'data_impute_project/error_metrics/min_mae_results.xlsx'
results_df.to_excel(output_file, index=False)

print(f"Results have been saved to {output_file}")