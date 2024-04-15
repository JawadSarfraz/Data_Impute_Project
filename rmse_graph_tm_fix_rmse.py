import pandas as pd
import matplotlib.pyplot as plt
import os

def ensure_dir(directory):
    """Create Dir if not exist"""
    if not os.path.exists(directory):
        os.makedirs(directory)

def plot_comparison(df, feature, combination, output_dir):
    """Generate and save comparison plots for each feature across different percentages."""
    plt.figure(figsize=(12, 8))
    percentages = sorted(df['Percentage'].unique())
    algorithms = df['Algorithm'].unique()

    # Plot each algorithm's performance across different percentages
    for algorithm in algorithms:
        means = []
        for percentage in percentages:
            subset = df[(df['Feature'] == feature) & 
                        (df['Combination'] == combination) & 
                        (df['Percentage'] == percentage) & 
                        (df['Algorithm'] == algorithm)]
            means.append(subset['Min RMSE'].mean())

        plt.plot(percentages, means, marker='o', label=f'{algorithm} - {feature}')

    plt.title(f'Comparison of RMSE across Percentages for Feature {feature} in {combination}')
    plt.xlabel('Percentage of Data Removed')
    plt.ylabel('Average Min RMSE')
    plt.xticks(percentages)
    plt.legend()
    plt.grid(True)

    # For good comparison, set y-axis limits from 0 to 1
    plt.ylim(0, 1)

    # Save the plot
    plot_filename = f'Comparison_{feature}_{combination}.png'
    plot_path = os.path.join(output_dir, plot_filename)
    plt.savefig(plot_path)
    plt.close()
    print(f"Comparison plot saved: {plot_path}")

# Set file path and output directory
data_path = 'data_impute_project/error_metrics/min_error_analysis_with_feature_combination.csv'
output_dir = 'data_impute_project/error_metrics/comparison_plots_fix_rmseaxis'
ensure_dir(output_dir)

# Load data
df = pd.read_csv(data_path)

# Unique combinations and features
combinations = df['Combination'].unique()
features = df['Feature'].unique()

# Generate comparison plots
for combination in combinations:
    for feature in features:
        plot_comparison(df, feature, combination, output_dir)