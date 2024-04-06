import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Ensure directory existence function
def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Setup
input_file = 'data_impute_project/min_error_summary/min_errors_summary.csv'
output_dir = 'data_impute_project/visualizations'
ensure_dir(output_dir)  # Ensure the visualization directory is created

# Load the summary of minimal errors
df_min_errors = pd.read_csv(input_file)

# Plotting setup with Seaborn for better aesthetics
sns.set(style="whitegrid")

def plot_min_errors(df, error_type, output_dir):
    """
    Generates and saves plots for the minimal RMSE or NRMSE values across percentages for each combination and feature.
    """
    if error_type not in ['RMSE', 'NRMSE']:
        print("Error type must be 'RMSE' or 'NRMSE'.")
        return
    
    # Filter based on error type
    df_error = df[df['Min Error Type'] == error_type]
    
    # Unique combinations and features for plotting
    combinations = df_error['Combination'].unique()
    features = df_error['Feature'].unique()
    
    for combination in combinations:
        for feature in features:
            df_plot = df_error[(df_error['Combination'] == combination) & (df_error['Feature'] == feature)]
            if df_plot.empty:
                continue
            
            plt.figure(figsize=(10, 6))
            sns.lineplot(data=df_plot, x='Percentage', y='Min Mean Error', hue='Min Algorithm', marker='o', linestyle='-', linewidth=2.5, markersize=10)
            plt.title(f'Minimal {error_type} across Percentages\n{combination} - Feature: {feature}')
            plt.xlabel('Percentage of Missing Data')
            plt.ylabel(f'Minimal Mean {error_type}')
            plt.tight_layout()
            
            # Save the plot
            plot_file = f"{output_dir}/{combination}_{feature}_min_{error_type.lower()}.png"
            plt.savefig(plot_file)
            plt.close()
            print(f"Plot saved: {plot_file}")

# Generate and save the plots for both RMSE and NRMSE
plot_min_errors(df_min_errors, 'RMSE', output_dir)
plot_min_errors(df_min_errors, 'NRMSE', output_dir)