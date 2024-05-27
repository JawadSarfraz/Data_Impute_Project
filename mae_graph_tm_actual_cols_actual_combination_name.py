import pandas as pd
import matplotlib.pyplot as plt
import os

def ensure_dir(directory):
    """Ensure directory exists, if not, create it.

    Param:
        directory (str): The path of directory to check and ensure its existence.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

# Mapping of combinations to their descriptive names for better readability in plots.
combination_names = {
    'combination_1_ABCD': 'Combination 1: δ13C coll, δ15N coll, δ13C carb, δ18O carb',
    'combination_2_ABCDE': 'Combination 2: δ13C coll, δ15N coll, δ13C carb, δ18O carb, δ18O phos',
    'combination_3_ABCDF': 'Combination 3: δ13C coll, δ15N coll, δ13C carb, δ18O carb, δ34S coll'
}

# Mapping of feature into its acutal names for use in plots.
feature_names = {
    'A': 'δ13C coll',
    'B': 'δ15N coll',
    'C': 'δ13C carb',
    'D': 'δ18O carb',
    'E': 'δ18O phos',
    'F': 'δ34S coll'
}

def translate_features(scenario):
    """Translate single character features to their full names based on feature_names.

    Param:
        scenario (str): string of feature names/codes.

    Returns:
        str: concatenated string of full feature names separated by underscores.
    """
    translated = []
    for char in scenario:
        if char in feature_names:
            translated.append(feature_names[char])
    return '_'.join(translated)

def plot_comparison(df, feature, combination, output_dir):
    """Generate plot comparing algorithms for given feature and combination, and save plot to a file.

    Params:
        df (DataFrame): dataframe containing error metrics.
        feature (str): feature to plot.
        combination (str): combination category of the feature.
        output_dir (str): dir where plot will be saved.
    """
    plt.figure(figsize=(12, 8))
    feature_label = feature_names.get(feature, feature)
    filtered_df = df[(df['Combination'] == combination) & (df['Feature'] == feature)]
    algorithms = filtered_df['Algorithm'].unique()

    # Iterate through each algo to plot its curve.
    for algorithm in algorithms:
        algorithm_df = filtered_df[filtered_df['Algorithm'] == algorithm]
        percentages = sorted(algorithm_df['Percentage'].unique())
        mae_values = []
        scenario_labels = []

        # Collect MAE values and scenarios for each percentages.
        for perc in percentages:
            perc_df = algorithm_df[algorithm_df['Percentage'] == perc]
            mae_values.append(perc_df['Min MAE'].mean())
            scenario_translated = translate_features(perc_df['FeatureSet Removal Scenario'].iloc[0])
            scenario_labels.append(f"{scenario_translated} - {perc}%")
            #scenario_labels.append(perc_df['FeatureSet Removal Scenario'].iloc[0] + f" - {perc}")

        # Plot the line for the algorithm
        plt.plot(percentages, mae_values, '-o', label=f"{algorithm} ({', '.join(scenario_labels)})")
    
    # Setting up plot labels and saving the file.
    plt.title(f'Comparison of MAE for {feature_label} in {combination_names[combination]}')
    plt.xlabel('Percentage of Data Removed')
    plt.ylabel('Min MAE')
    plt.ylim(0, 3) # set scale...
    plt.legend(loc='upper right', fontsize='small', title='Algorithms and Feature Sets')
    plt.grid(True)
    # Setting custom x-axis tick marks
    plt.xticks([10, 15, 20])
    plot_filename = f'{feature_label}_{combination}.png'
    plot_path = os.path.join(output_dir, plot_filename)
    plt.savefig(plot_path)
    plt.close()
    print(f"Comparison plot saved: {plot_path}")

# Main execution block
# Path settings, load data, generate plots for each combinations and features
data_path = 'data_impute_project/error_metrics/min_error_analysis_with_feature_combinations.csv'
output_dir = 'data_impute_project/graphs/mae/plots/terrestrial_mammals' 
ensure_dir(output_dir)

# Load data
df = pd.read_csv(data_path)

# Generate plots for each combination and feature
for combination in combination_names:
    for feature in feature_names:
        plot_comparison(df, feature, combination, output_dir)