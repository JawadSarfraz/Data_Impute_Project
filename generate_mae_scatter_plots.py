import pandas as pd
import matplotlib.pyplot as plt
import os

# Load CSV file
file_path = 'data_impute_project/error_metrics/error_analysis_with_all_featureset.csv'
data = pd.read_csv(file_path)

# Create output directory for the plots
output_dir = 'data_impute_project/mae_scatter_plots/terrestrial_mammals'
os.makedirs(output_dir, exist_ok=True)

# Iterate through each combination and feature
combinations = data['Combination'].unique()
for combination in combinations:
    features = data[data['Combination'] == combination]['Feature'].unique()
    for feature in features:
        # Filter the data for the specific combination and feature
        filtered_data = data[(data['Combination'] == combination) & (data['Feature'] == feature)]
        
        # Create the scatter plot
        plt.figure(figsize=(14, 8))
        markers = ['o', 's', 'D', '^', 'v']
        percentages = filtered_data['Percentage'].unique()
        algorithms = filtered_data['Algorithm'].unique()
        for marker, algorithm in zip(markers, algorithms):
            for percentage in percentages:
                algo_data = filtered_data[(filtered_data['Algorithm'] == algorithm) & (filtered_data['Percentage'] == percentage)]
                plt.scatter(algo_data['FeatureSet'], algo_data['MAE'], marker=marker, label=f'{algorithm} at {percentage}%', zorder=3)
        
        # Add title and labels
        plt.title(f'MAE for Feature "{feature}" in {combination}')
        plt.xlabel('FeatureSet')
        plt.ylabel('MAE')
        plt.xticks(rotation=90)
        plt.grid(True, zorder=1)
        
        # Adjust legend to be outside the plot area
        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        plt.legend(by_label.values(), by_label.keys(), title='Algorithms and Percentages', bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # Save plot to a file
        plot_filename = f'{combination}_{feature}.png'.replace(' ', '_').replace('(', '').replace(')', '').replace(',', '')
        plt.savefig(os.path.join(output_dir, plot_filename), bbox_inches='tight')
        plt.close()

print("Scatter plots have been created for all features of all combinations.")
