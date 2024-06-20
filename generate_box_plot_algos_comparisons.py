import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

def ensure_dir(directory):
    """
    Ensure specified directory exists; create it if it does not.
    
    Params:
    directory (str): path to dir to check/create.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

def plot_box_plots(imputed_values_df, feature_name, percentage, seed, output_dir):
    """
    Plot box plots for the original and imputed values.
    
    Params:
    imputed_values_df (pd.DataFrame): DataFrame containing original and imputed values.
    feature_name (str): Name of the feature for the plot titles.
    percentage (str): The percentage of data removed, used in the plot title.
    seed (str): Seed used for the imputation, used in the plot title.
    output_dir (str): Directory to save the plots.
    """
    plt.figure(figsize=(10, 6))
    
    # Box plot
    sns.boxplot(data=imputed_values_df[['OriginalDataValue', 'KNN', 'SVM', 'RF']])
    plt.title(f'Box Plot of {feature_name} ({percentage}%, Seed: {seed})')
    # Labels x and y axis
    plt.xlabel('Imputation Algos & Orignial Data')
    plt.ylabel('Feature Value')
    
    
    # Save the plot
    plot_output_path = os.path.join(output_dir, f"{seed}_box_plot_{percentage}.png")
    plt.savefig(plot_output_path)
    plt.close()
    print(f"Saved plot: {plot_output_path}")

# Ensure output directory exists
base_input_dir = 'data_impute_project/imputation_comparison'
output_plot_dir = 'data_impute_project/plots'
ensure_dir(output_plot_dir)

# Iterate through the directory structure
for root, dirs, files in os.walk(base_input_dir):
    for file in files:
        if file.endswith('_imputed_comparison.xlsx'):
            file_path = os.path.join(root, file)
            imputed_values_df = pd.read_excel(file_path)
            
            # Extract feature name, percentage, and seed from the directory structure and filename
            path_parts = root.split(os.sep)
            feature_name = path_parts[-2]
            percentage = path_parts[-1]
            seed = file.split('_')[0]
            
            # Create output directory for plots
            plot_output_dir = os.path.join(output_plot_dir, *path_parts[1:-2], feature_name, percentage)
            ensure_dir(plot_output_dir)
            
            # Plot and save the box plot
            plot_box_plots(imputed_values_df, feature_name, percentage, seed, plot_output_dir)