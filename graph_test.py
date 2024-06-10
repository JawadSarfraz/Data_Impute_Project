import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Load the results from the CSV file
input_file_path = 'data_impute_project/error_metrics/error_analysis_with_all_featureset.csv'
df = pd.read_csv(input_file_path)

# Ensure output directory exists
output_graph_dir = 'data_impute_project/graphs'
os.makedirs(output_graph_dir, exist_ok=True)

# Function to plot MAE for a single feature of one combination
def plot_mae_for_feature(df, combination, feature):
    # Filter the DataFrame for the specified combination and feature
    df_filtered = df[(df['Combination'] == combination) & (df['Feature'] == feature)]
    
    # Check if df_filtered is empty
    if df_filtered.empty:
        print(f"No data available for combination {combination} and feature {feature}")
        return
    
    # Create a new figure for the plot
    plt.figure(figsize=(14, 8))
    
    # Loop through each algorithm to plot their points with different colors and markers
    markers = ['o', 's', '^', 'D', 'x', 'v', '<', '>', 'p', '*']
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'orange', 'purple', 'brown']
    
    for i, algo in enumerate(df_filtered['Algorithm'].unique()):
        df_algo = df_filtered[df_filtered['Algorithm'] == algo]
        # Add some jitter to the x-axis to separate overlapping points
        jitter = np.random.uniform(-0.5, 0.5, size=len(df_algo))
        plt.scatter(df_algo['Percentage'] + jitter, df_algo['MAE'], label=algo, marker=markers[i % len(markers)], color=colors[i % len(colors)])
        
        # Annotate each point with the FeatureSet abbreviation
        for idx in range(len(df_algo)):
            row = df_algo.iloc[idx]
            plt.annotate(row['FeatureSet'], 
                         (row['Percentage'] + jitter[idx], row['MAE']), 
                         textcoords="offset points", 
                         xytext=(0, 5), 
                         ha='center', 
                         fontsize=8,  # Smaller font size to reduce clutter
                         rotation=30)  # Rotate text to reduce overlap
    
    # Set x-axis to only show 10, 15, and 20
    plt.xticks([10, 15, 20])
    
    # Check if there are valid MAE values to set y-ticks
    max_mae = df_filtered['MAE'].max()
    if not np.isnan(max_mae):
        plt.yticks(np.arange(0, max_mae + 0.10, 0.10))
    else:
        plt.yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5])  # Default y-ticks if no valid MAE

    # Add plot details
    plt.title(f'MAE for Feature {feature} in Combination {combination}', fontsize=14)
    plt.xlabel('Percentage', fontsize=12)
    plt.ylabel('MAE', fontsize=12)
    plt.legend(title='Algorithm', fontsize=10)
    plt.grid(True)
    
    # Save the plot to a file
    output_file_path = os.path.join(output_graph_dir, f'{combination}_{feature}_mae_plot.png')
    plt.savefig(output_file_path, bbox_inches='tight')
    plt.close()
    print(f'Plot saved to: {output_file_path}')

# Get unique combinations and features from the DataFrame
combinations = df['Combination'].unique()
features = df['Feature'].unique()

# Loop through each combination and feature to generate plots
for combination in combinations:
    for feature in features:
        plot_mae_for_feature(df, combination, feature)