import pandas as pd
import matplotlib.pyplot as plt
import os

# List of valid datasets
datasets = ["bird", "fish", "human", "mammals_without_humans", "marine_mammals", 
            "terr_herb_and_marine_mammals", "terrestrial_herbivorous_mammals", "terrestrial_mammals"]

# Prompt user for dataset type
dataset_type = input("Enter the dataset type (e.g., bird, fish, human, etc.): ").strip()

# Verify if entered dataset type is valid
if dataset_type not in datasets:
    raise ValueError("Invalid dataset type entered. Please try again.")

# Construct file path based on dataset type
file_path = os.path.join("..", "data_impute_project", "error_metrics", dataset_type, 'error_analysis_with_all_featuresets.csv')

# Check if the file exists
if not os.path.exists(file_path):
    raise FileNotFoundError(f"No error metrics file found for {dataset_type}. Please check the file path or select another dataset.")

# Load CSV file
data = pd.read_csv(file_path)

# Output directory for plots
output_dir = os.path.join("..", "data_impute_project", "mae_scatter_plots", dataset_type)
os.makedirs(output_dir, exist_ok=True)

# Define markers and colors
markers = ['o', 's', 'D', '^', 'v', '<', '>']
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']

def generate_scatter_plots(data, output_dir):
    for combination in data['Combination'].unique():
        for feature in data[data['Combination'] == combination]['Feature'].unique():
            filtered_data = data[(data['Combination'] == combination) & (data['Feature'] == feature)]
            plt.figure(figsize=(14, 8))

            for i, algorithm in enumerate(filtered_data['Algorithm'].unique()):
                color = colors[i % len(colors)]
                for j, percentage in enumerate(filtered_data['Percentage'].unique()):
                    marker = markers[j % len(markers)]
                    algo_data = filtered_data[(filtered_data['Algorithm'] == algorithm) & (filtered_data['Percentage'] == percentage)]
                    plt.scatter(algo_data['FeatureSet'], algo_data['MAE'], color=color, marker=marker, label=f'{algorithm} at {percentage}%', zorder=3)

            plt.title(f'MAE for Feature "{feature}" in {combination}')
            plt.xlabel('FeatureSet')
            plt.ylabel('MAE')
            plt.xticks(rotation=90)
            plt.grid(True, zorder=1)

            # Create legend without duplicate labels
            handles, labels = plt.gca().get_legend_handles_labels()
            by_label = dict(zip(labels, handles))
            plt.legend(by_label.values(), by_label.keys(), title='Algorithms and Percentages', bbox_to_anchor=(1.05, 1), loc='upper left')

            plot_filename = f'{combination}___{feature}.png'.replace(' ', '_').replace('(', '').replace(')', '').replace(',', '')
            plt.savefig(os.path.join(output_dir, plot_filename), bbox_inches='tight')
            plt.close()

# Generate scatter plots for the selected dataset
generate_scatter_plots(data, output_dir)
print(f"Scatter plots have been created for all features of all combinations in the {dataset_type} dataset.")
