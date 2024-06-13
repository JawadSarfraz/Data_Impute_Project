import pandas as pd
import os

# Load the Excel file
file_path = 'modified_dataset.xlsx'
xls = pd.ExcelFile(file_path)

# Base directory where the individual datasets will be stored
base_dir = 'data_impute_project/data/'
os.makedirs(base_dir, exist_ok=True)

# Loop & Load through each sheet in Excel file
for sheet_name in xls.sheet_names:
    # Load the sheet into a dataframe
    df = pd.read_excel(xls, sheet_name=sheet_name)

    # Rename columns to 'A', 'B', 'C' ...
    alphabet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    df.columns = alphabet[:len(df.columns)]
    
    # Create valid filename for each category
    filename = f"{sheet_name.replace(' ', '_').replace('(', '').replace(')', '')}.xlsx"
    full_path = os.path.join(base_dir, filename) # path to save
    
    df.to_excel(full_path, index=False) # Save dataframe to Excel
    print(f"Saved {sheet_name} data to {full_path}")