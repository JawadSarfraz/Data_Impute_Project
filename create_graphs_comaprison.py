import pandas as pd
import matplotlib.pyplot as plt
import os

def ensure_dir(directory):
    """Ensure directory exists, if not, create it."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def plot_results(df, feature, combination, output_dir):
    """Generate and save plots for each percentage of data removal for a given feature and combination."""
    percentages = df['Percentage'].unique()
    algorithms = df['Algorithm'].unique()

    for percentage in percentages:
        plt.figure(figsize=(10, 6))
        for algorithm in algorithms:
            # Filter data for current settings
            subset = df[(df['Feature'] == feature) & 
                        (df['Combination'] == combination) & 
                        (df['Percentage'] == percentage) & 
                        (df['Algorithm'] == algorithm)]
            if not subset.empty:
                plt.plot(subset['FeatureSet Removal Scenario'], subset['Min RMSE'], marker='o', label=f'{algorithm}')

        plt.title(f'RMSE for Feature {feature} at {percentage}% Removal in {combination}')
        plt.xlabel('Feature Set Removal Scenario')
        plt.ylabel('Min RMSE')
        plt.xticks(rotation=45)
        plt.legend(title='Algorithm')
        plt.grid(True)

        # Save the plot in the specified directory
        plot_filename = f'RMSE_{feature}_{percentage}_{combination}.png'
        plot_path = os.path.join(output_dir, plot_filename)
        plt.savefig(plot_path)
        plt.close()
        print(f"Plot saved: {plot_path}")

# Set file path and output directory
data_path = 'data_impute_project/error_metrics/min_error_analysis_with_feature_combination.csv'
output_dir = 'data_impute_project/graphs/plots'
ensure_dir(output_dir)

# Load data
df = pd.read_csv(data_path)

# Unique combinations and features
combinations = df['Combination'].unique()
features = df['Feature'].unique()

# Generate plots
for combination in combinations:
    for feature in features:
        plot_results(df, feature, combination, output_dir)