import pandas as pd
import matplotlib.pyplot as plt
import os

def ensure_dir(directory):
    """Ensure directory exists, if not, create it."""
    if not os.path.exists(directory):
        os.makedirs(directory)

combination_names = {
    'combination_1_ABCD': 'Combination 1: δ13C coll, δ15N coll, δ13C carb, δ18O carb',
    'combination_2_ABCDE': 'Combination 2: δ13C coll, δ15N coll, δ13C carb, δ18O carb, δ18O phos',
    'combination_3_ABCDF': 'Combination 3: δ13C coll, δ15N coll, δ13C carb, δ18O carb, δ34S coll'
}

feature_names = {
    'A': 'δ13C coll',
    'B': 'δ15N coll',
    'C': 'δ13C carb',
    'D': 'δ18O carb',
    'E': 'δ18O phos',
    'F': 'δ34S coll'
}

def plot_comparison(df, feature, combination, output_dir):
    plt.figure(figsize=(12, 8))
    feature_label = feature_names.get(feature, feature)
    filtered_df = df[(df['Combination'] == combination) & (df['Feature'] == feature)]
    algorithms = filtered_df['Algorithm'].unique()
    percentages = sorted(filtered_df['Percentage'].unique())

    # Process each algorithm separately
    for percentage in percentages:
        percentage_df = filtered_df[filtered_df['Percentage'] == percentage]
        for index, row in percentage_df.iterrows():
            plt.plot(percentage, row['Min RMSE'], 'o', label=f"{row['Algorithm']} ({row['FeatureSet Removal Scenario']})")
            plt.text(percentage, row['Min RMSE'], f"{row['FeatureSet Removal Scenario']}", 
                     fontsize=9, ha='center', va='bottom')
            
    for algorithm in algorithms:
        algorithm_df = filtered_df[filtered_df['Algorithm'] == algorithm]
        percentage_df = filtered_df[filtered_df['Percentage'] == percentage]
        for index, row in percentage_df.iterrows():
            plt.plot(percentage, row['Min RMSE'], 'o', label=f"{row['Algorithm']} ({row['FeatureSet Removal Scenario']})")
            plt.text(percentage, row['Min RMSE'], f"{row['FeatureSet Removal Scenario']}", 
                     fontsize=9, ha='center', va='bottom')
        rmse_values = [algorithm_df[algorithm_df['Percentage'] == perc]['Min RMSE'].mean() for perc in percentages]

        # Plot the line connecting the RMSE values for this algorithm
        plt.plot(percentages, rmse_values, '-o', label=f"{algorithm}")

        # # Optional: Add text labels for each point
        # for perc, rmse in zip(percentages, rmse_values):
        #     scenario = algorithm_df[algorithm_df['Percentage'] == perc]['FeatureSet Removal Scenario'].iloc[0]
        #     plt.text(perc, rmse, f"{scenario}", fontsize=9, ha='center', va='bottom')

    #plt.title(f'Comparison of RMSE for {feature_label} in {combination_names[combination]}')
    plt.xlabel('Percentage of Data Removed')
    plt.ylabel('Min RMSE')
    plt.ylim(0, 1)
    plt.legend(loc='upper right', fontsize='small')
    plt.grid(True)

    plot_filename = f'{feature_label}_{combination}.png'
    plot_path = os.path.join(output_dir, plot_filename)
    plt.savefig(plot_path)
    plt.close()
    print(f"Comparison plot saved: {plot_path}")
# Path settings
data_path = 'data_impute_project/error_metrics/min_error_analysis_with_feature_combination.csv'  # Adjust the path to your CSV file
output_dir = 'data_impute_project/graphs/rmse/plots3/terrestrial_mammals'  # Adjust the path to your output directory
ensure_dir(output_dir)

# Load data
df = pd.read_csv(data_path)

# Generate plots for each combination and feature
for combination in combination_names:
    for feature in feature_names:
        plot_comparison(df, feature, combination, output_dir)