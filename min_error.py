import pandas as pd
import glob
import os

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

input_dir = 'data_impute_project/error_metrics'
output_dir = 'data_impute_project/min_error_summary'
ensure_dir(output_dir)

file_pattern = os.path.join(input_dir, "combination_*_*_*_mean_errors.csv")
files = glob.glob(file_pattern)

# List to collect all rows before creating the summary DataFrame
all_rows = []

for file_path in files:
    parts = os.path.basename(file_path).split('_')
    combination, feature, percentage = parts[1], parts[2], parts[3]
    
    df = pd.read_csv(file_path)
    
    min_rmse_row = df.loc[df['Mean RMSE'].idxmin()]
    min_nrmse_row = df.loc[df['Mean NRMSE'].idxmin()]
    
    summary_row_rmse = {
        'Combination': combination,
        'Feature': feature,
        'Percentage': percentage,
        'Min Error Type': 'RMSE',
        'Min Algorithm': min_rmse_row['Algorithm'],
        'Min Mean Error': min_rmse_row['Mean RMSE']
    }
    
    summary_row_nrmse = {
        'Combination': combination,
        'Feature': feature,
        'Percentage': percentage,
        'Min Error Type': 'NRMSE',
        'Min Algorithm': min_nrmse_row['Algorithm'],
        'Min Mean Error': min_nrmse_row['Mean NRMSE']
    }
    
    all_rows.append(summary_row_rmse)
    all_rows.append(summary_row_nrmse)

# Create the summary DataFrame from the list of rows
min_errors_summary = pd.DataFrame(all_rows)

output_file_path = os.path.join(output_dir, 'min_errors_summary.csv')
min_errors_summary.to_csv(output_file_path, index=False)
print(f"Summary of minimal errors saved to: {output_file_path}")