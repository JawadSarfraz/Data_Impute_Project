import os
import pandas as pd

def combine_min_mae_data(input_file_path, output_file_path):
    # Load data
    data = pd.read_excel(input_file_path)

    # List of unique features in dataset
    unique_features = data['Feature'].unique()

    # Create an empty DataFrame to concatenate all features data
    combined_data = pd.DataFrame()

    for feature in unique_features:
        # Filter data for specific feature
        feature_data = data[data['Feature'] == feature]
        
        # Find rows with minimum MAE for each percentage
        min_mae_rows = feature_data.loc[feature_data.groupby('Percentage')['Min MAE'].idxmin()]
            
        # Concatenate data to combined DataFrame
        combined_data = pd.concat([combined_data, min_mae_rows], ignore_index=True)

    # Save combined data to single Excel file
    combined_data.to_excel(output_file_path, index=False)
    print(f"Combined file saved as {output_file_path}")

if __name__ == "__main__":
    # List of datasets to process
    datasets = ["bird", "fish", "human", "mammals_without_humans", "marine_mammals", 
                "terr_herb_and_marine_mammals", "terrestrial_herbivorous_mammals", "terrestrial_mammals"]

    for dataset in datasets:
        # Set file paths using relative paths
        input_file_path = os.path.join("..", "data_impute_project", "error_metrics", dataset, "min_mae_mape_results.xlsx")
        output_file_path = os.path.join("..", "data_impute_project", "error_metrics", dataset, f"test_min_mae_mape_all_features_combined_{dataset}.xlsx")

        # Check if input file exists before processing
        if os.path.exists(input_file_path):
            # Run combination function
            combine_min_mae_data(input_file_path, output_file_path)
        else:
            print(f"No input file found for {dataset}. Skipping...")
