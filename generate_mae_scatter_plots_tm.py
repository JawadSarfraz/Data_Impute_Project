import pandas as pd
import matplotlib.pyplot as plt
import os

# Load CSV file
file_path = 'data_impute_project/error_metrics/error_analysis_with_all_featuresets.csv'
data = pd.read_csv(file_path)

# Output directory for plots
output_dir = 'data_impute_project/mae_scatter_plots/terrestrial_mammals_MAE_all_features'
os.makedirs(output_dir, exist_ok=True)

# Define markers and colors
markers = ['o', 's', 'D']
colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

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

            plot_filename = f'{combination}_{feature}.png'.replace(' ', '_').replace('(', '').replace(')', '').replace(',', '')
            plt.savefig(os.path.join(output_dir, plot_filename), bbox_inches='tight')
            plt.close()

generate_scatter_plots(data, output_dir)
print("Scatter plots have been created for all features of all combinations.")
