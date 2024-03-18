import pandas as pd

# Reload the original file and process all sheets regardless of their names
xls = pd.ExcelFile('subdatasets.xlsx')

# Prepare to store processed DataFrames for all sheets
processed_dfs_generic = {}

for sheet_name in xls.sheet_names:
    # Load the sheet into a DataFrame
    df_sheet = pd.read_excel(xls, sheet_name=sheet_name)

    # Round off all numeric columns to two decimal places
    numeric_cols = df_sheet.select_dtypes(include=['float64', 'int64']).columns
    df_sheet[numeric_cols] = df_sheet[numeric_cols].apply(lambda x: x.round(2))

    # Remove columns from A to E without renaming the rest
    df_sheet_modified = df_sheet.iloc[:, 5:]
    
    # Store the processed DataFrame with the original sheet name
    processed_dfs_generic[sheet_name] = df_sheet_modified

# Save the processed DataFrames to a new Excel file with multiple sheets, applying changes to all sheets
output_file_path_all_sheets_generic = 'modifield_dataset.xlsx'
with pd.ExcelWriter(output_file_path_all_sheets_generic) as writer:
    for sheet_name, df_proc in processed_dfs_generic.items():
        df_proc.to_excel(writer, sheet_name=sheet_name, index=False)

output_file_path_all_sheets_generic