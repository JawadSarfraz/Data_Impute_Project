import os
import pandas as pd

# Function to calculate outliers using IQR method
def find_iqr_outliers(df, columns):
    Q1 = df[columns].quantile(0.25)
    Q3 = df[columns].quantile(0.75)
    IQR = Q3 - Q1
    outliers = ((df[columns] < (Q1 - 1.5 * IQR)) | (df[columns] > (Q3 + 1.5 * IQR))).any(axis=1)
    return df[outliers]

# Function to process files with full paths
def process_file(file_path):
    print(f"Processing file: {file_path}")
    df = pd.read_excel(file_path)
    columns = df.columns[1:]  # First column is ID, rest are numeric
    
    # Find outliers
    outliers_df = find_iqr_outliers(df, columns)
    
    # Save outliers to new file
    outliers_file_path = file_path.replace(".xlsx", "_outliers.xlsx")
    outliers_df.to_excel(outliers_file_path, index=False)
    print(f"Outliers saved to: {outliers_file_path}")
    
    # Remove outliers from original DataFrame
    cleaned_df = df[~df.index.isin(outliers_df.index)]
    
    # Save cleaned DataFrame to new file
    cleaned_file_path = file_path.replace(".xlsx", "_cleaned.xlsx")
    cleaned_df.to_excel(cleaned_file_path, index=False)
    print(f"Cleaned data saved to: {cleaned_file_path}\n")

# Define paths
file_paths = [
    "data_impute_project/combinations/terrestrial_mammals/combination_1_ABCD.xlsx",
    "data_impute_project/combinations/terrestrial_mammals/combination_2_ABCDE.xlsx",
    "data_impute_project/combinations/terrestrial_mammals/combination_3_ABCDF.xlsx"
]

# Process each file
for file_path in file_paths:
    if os.path.exists(file_path):
        process_file(file_path)
    else:
        print(f"File not found: {file_path}")