import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
file_path = 'data_impute_project/error_metrics/error_analysis_with_all_featureset.csv'
data = pd.read_csv(file_path)

# Print first few rows of dataset to verify its structure
print("Dataset head:\n", data.head())

# Filter data for Feature A in combination_1_ABCD ---> TESTING pupose
feature_d_data = data[(data['Combination'] == 'combination_1_ABCD') & (data['Feature'] == 'A (δ13C coll)')]

# Print the filtered data to verify the filtering step
print("\nFiltered data for Feature A (δ13C coll):\n", feature_d_data)

# Check if filtered data is empty
if feature_d_data.empty:
    print("No data available for Feature A (δ13C coll) in combination_1_ABCD")
else:
    # Create a scatter plot for MAE values of Feature A
    plt.figure(figsize=(16, 10))

    # Scatter plot for MAE with different markers for percentages
    sns.scatterplot(x='FeatureSet', y='MAE', hue='Algorithm', style='Percentage', data=feature_d_data, s=100)

    # Add titles and labels
    plt.title('MAE for Each Feature Set of Feature A (δ13C coll) in combination_1_ABCD Across All Algorithms')
    plt.xlabel('Feature Set')
    plt.ylabel('MAE')
    plt.xticks(rotation=90)
    plt.legend(title='Algorithm / Percentage', bbox_to_anchor=(1.05, 1), loc='upper left')

    # Define the directory path and create it if it doesn't exist
    directory_path = 'data_impute_project/graph'
    os.makedirs(directory_path, exist_ok=True)

    # File path to save the plot
    plot_file_path = os.path.join(directory_path, 'feature_a_scatter_plot.png')

    # Save the plot
    plt.tight_layout()
    plt.savefig(plot_file_path)
    plt.show()

    print(f"Plot saved at: {plot_file_path}")