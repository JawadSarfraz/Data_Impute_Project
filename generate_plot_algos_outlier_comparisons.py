import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns

def ensure_dir(directory):
    """
    Ensure specified directory exists; create it if does not.
    
    Params:
    directory (str): Path to the directory to check/create.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

def detect_outliers_mad(data, threshold=3.0):
    """
    Detect outliers using Median Absolute Deviation (MAD) method.
    
    Params:
    data (pd.Series): Data values to check for outliers.
    threshold (float): Threshold to determine what is considered an outlier.
    
    Returns:
    pd.Series: boolean mask indicating which values are outliers.
    """
    median = np.median(data)
    abs_deviation = np.abs(data - median)
    mad = np.median(abs_deviation)
    modified_z_scores = 0.6745 * abs_deviation / mad
    outliers = modified_z_scores > threshold
    return outliers

def plot_box_plots(imputed_values_df, combination, target_feature, feature_combination, feature_labels, percentage, seed, output_dir):
    """
    Plot box plots for original and imputed values, highlighting MAD-detected outliers.
    
    Params:
    imputed_values_df (pd.DataFrame): DataFrame containing original and imputed values.
    combination (str): Name of combination for plot titles.
    target_feature (str): Target feature name for plot titles.
    feature_combination (str): Combination of feature names for plot titles.
    feature_labels (str): Descriptive labels of features.
    percentage (str): Percentage of data removed, used in plot title.
    seed (str): Seed used for imputation, used in plot title.
    output_dir (str): Directory to save plots.
    """
    plt.figure(figsize=(12, 8))
    
    # Set light background for plot
    sns.set(style="whitegrid")

    # Plot original and imputed values
    sns.boxplot(data=imputed_values_df[['OriginalDataValue']], showfliers=False, color='#1f77b4')  # Darker blue
    sns.boxplot(data=imputed_values_df[['KNN', 'SVM', 'RF']], showfliers=False, palette=['#ff7f0e', '#2ca02c', '#d62728'])  # Orange, Green, Red

    # Highlight MAD-detected outliers
    for column, color in zip(['KNN', 'SVM', 'RF'], ['#ff7f0e', '#2ca02c', '#d62728']):
        outliers = detect_outliers_mad(imputed_values_df[column])
        sns.scatterplot(x=[column] * sum(outliers), y=imputed_values_df.loc[outliers, column], color=color, marker='o', edgecolor='black', s=100, zorder=10)

    # Formatting title
    title = (f'Analysis of Imputation Methods for Feature {target_feature} ({feature_labels.split("_")[0]})\n'
             f'with FeatureSet {feature_combination} ({feature_labels})\n'
             f'of Combination: {combination}, at Seed: {seed}, with Missing Data: {percentage}%')
    plt.title(title, fontsize=12)
    plt.ylabel('Value')
    
    # Save plot
    plot_output_path = os.path.join(output_dir, f"{seed}_box_plot_{percentage}.png")
    ensure_dir(output_dir)
    plt.savefig(plot_output_path)
    plt.close()
    print(f"Saved plot: {plot_output_path}")

# Ensure output directory
base_input_dir = 'data_impute_project/imputation_comparison'
output_plot_dir = 'data_impute_project/plots/terrestrial_mammals'
ensure_dir(output_plot_dir)

# Column name mapping
column_map = {
    'A': 'δ13C coll',
    'B': 'δ15N coll',
    'C': 'δ13C carb',
    'D': 'δ18O carb',
    'E': 'δ34S coll',
    'F': 'δ18O phos',
    'G': '87Sr/86Sr bone',
    'H': '87Sr/86Sr enamel'
}

# Iterate through directory structure
for root, dirs, files in os.walk(base_input_dir):
    for file in files:
        if file.endswith('_imputed_comparison.xlsx'):
            file_path = os.path.join(root, file)
            imputed_values_df = pd.read_excel(file_path)
            
            # Extract combination, target feature, feature combination, percentage, and seed from directory structure and filename
            path_parts = root.split(os.sep)
            combination = path_parts[-4]
            target_feature = path_parts[-3]
            feature_combination = path_parts[-2]
            percentage = path_parts[-1]
            seed = file.split('_')[0]
            
            # Get descriptive labels of features from column_map
            feature_labels = "_".join(column_map.get(feat, feat) for feat in feature_combination)
            
            # Create output directory for plots
            plot_output_dir = os.path.join(output_plot_dir, *path_parts[1:-2], target_feature, feature_combination, percentage)
            ensure_dir(plot_output_dir)
            
            # Plot and save box plot
            plot_box_plots(imputed_values_df, combination, target_feature, feature_combination, feature_labels, percentage, seed, plot_output_dir)
