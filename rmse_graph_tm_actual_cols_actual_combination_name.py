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

def translate_features(scenario):
    """Translate single character features to their full names based on feature_names."""
    translated = []
    for char in scenario:
        if char in feature_names:
            translated.append(feature_names[char])
    return '_'.join(translated)

def plot_comparison(df, feature, combination, output_dir):
    plt.figure(figsize=(12, 8))
    feature_label = feature_names.get(feature, feature)
    filtered_df = df[(df['Combination'] == combination) & (df['Feature'] == feature)]
    algorithms = filtered_df['Algorithm'].unique()

    for algorithm in algorithms:
        algorithm_df = filtered_df[filtered_df['Algorithm'] == algorithm]
        percentages = sorted(algorithm_df['Percentage'].unique())
        rmse_values = []
        scenario_labels = []

        for perc in percentages:
            perc_df = algorithm_df[algorithm_df['Percentage'] == perc]
            rmse_values.append(perc_df['Min RMSE'].mean())
            scenario_translated = translate_features(perc_df['FeatureSet Removal Scenario'].iloc[0])
            scenario_labels.append(f"{scenario_translated} - {perc}%")
            #scenario_labels.append(perc_df['FeatureSet Removal Scenario'].iloc[0] + f" - {perc}")

        # Plot the line for the algorithm
        plt.plot(percentages, rmse_values, '-o', label=f"{algorithm} ({', '.join(scenario_labels)})")

    plt.title(f'Comparison of RMSE for {feature_label} in {combination_names[combination]}')
    plt.xlabel('Percentage of Data Removed')
    plt.ylabel('Min RMSE')
    plt.ylim(0, 1)
    plt.legend(loc='upper right', fontsize='small', title='Algorithms and Feature Sets')
    plt.grid(True)
# Setting custom x-axis tick marks
    plt.xticks([10, 15, 20])
    plot_filename = f'{feature_label}_{combination}.png'
    plot_path = os.path.join(output_dir, plot_filename)
    plt.savefig(plot_path)
    plt.close()
    print(f"Comparison plot saved: {plot_path}")

# Path settings
data_path = 'data_impute_project/error_metrics/min_error_analysis_with_feature_combination.csv'  # Adjust the path to your CSV file
output_dir = 'data_impute_project/graphs/rmse/plots/terrestrial_mammals'  # Adjust the path to your output directory
ensure_dir(output_dir)

# Load data
df = pd.read_csv(data_path)

# Generate plots for each combination and feature
for combination in combination_names:
    for feature in feature_names:
        plot_comparison(df, feature, combination, output_dir)