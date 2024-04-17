import pandas as pd
import matplotlib.pyplot as plt
import os

# Create dir if doesn't exist
def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Update combination names dictionary with full names for the feature sets
combination_names = {
    'combination_1_ABCD': 'combination_1_δ13C coll_δ15N coll_δ13C carb_δ18O carb',
    'combination_2_ABCDE': 'combination_2_δ13C coll_δ15N coll_δ13C carb_δ18O carb_δ18O phos',
    'combination_3_ABCDF': 'combination_3_δ13C coll_δ15N coll_δ13C carb_δ18O carb_δ34S coll'
}

feature_names = {
    'A': 'δ13C coll',
    'B': 'δ15N coll',
    'C': 'δ13C carb',
    'D': 'δ18O carb',
    'E': 'δ18O phos',
    'F': 'δ34S coll'
}

# Define plotting function
def plot_comparison(df, feature, combination, output_dir):
    # Prepare the plot
    plt.figure(figsize=(10, 6))
    feature_label = feature_names.get(feature, feature)  # Get full name for the feature

    # Filter data for specific combination and feature
    filtered_df = df[(df['Combination'] == combination) & (df['Feature'] == feature)]
    algorithms = filtered_df['Algorithm'].unique()
    
    # Plot for each algorithm across percentages
    for algorithm in algorithms:
        algorithm_df = filtered_df[filtered_df['Algorithm'] == algorithm]
        percentages = algorithm_df['Percentage'].unique()
        rmse_values = [algorithm_df[algorithm_df['Percentage'] == perc]['Min RMSE'].mean() for perc in percentages]
        
        # Plotting points and line
        plt.plot(percentages, rmse_values, '-o', label=algorithm)
    
    # Formatting the plot
    plt.title(f'Comparison of RMSE for {feature_label} ({combination_names[combination]})')
    plt.xlabel('Percentage of Data Removed')
    plt.ylabel('Min RMSE')
    plt.ylim(0, 1)  # Set y-axis from 0 to 1
    plt.legend()
    plt.grid(True)
    
    # Save the plot
    plot_filename = f'{feature_label}_{combination}.png'
    plot_path = os.path.join(output_dir, plot_filename)
    plt.savefig(os.path.join(output_dir, plot_filename))
    plt.close()
    print(f"Comparison plot saved: {plot_path}")

    
    

# Set file path and output directory
data_path = 'data_impute_project/error_metrics/min_error_analysis_with_feature_combination.csv'
output_dir = 'data_impute_project/graphs/rmse/plots/terrestrial_mammals'
ensure_dir(output_dir)

# Load data
df = pd.read_csv(data_path)

# Generate plots for each combination and feature
for combination in combination_names:
    for feature in feature_names:
        plot_comparison(df, feature, combination, output_dir)
