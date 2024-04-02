import pandas as pd
import numpy as np

# Load the data
file_path_human = 'data_impute_project/data/human.xlsx'
data_human = pd.read_excel(file_path_human)

# Replace spaces with NaN
data_human.replace(' ', np.nan, inplace=True)

# Convert all columns to numeric, coercing any errors into NaNs
data_human = data_human.apply(pd.to_numeric, errors='coerce')

# Now you can calculate correlations without encountering the previous error
correlation_matrix_human = data_human.corr()

# Define the output file path
output_path = 'data_impute_project/corr_factor/human.xlsx'

# Write the correlation matrix to Excel
correlation_matrix_human.to_excel(output_path)

print("Correlation matrix has been saved to:", output_path)