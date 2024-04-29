import pandas as pd

# Define the file paths
input_file_path = 'data_impute_project/corr_test/terrestrial_mammals/imputation_summary.xlsx'
output_file_path = 'data_impute_project/corr_test/terrestrial_mammals/imputation_summary_rename.xlsx'

# Load the data
data = pd.read_excel(input_file_path)

# Column mapping as provided
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

# Function to rename the 'Combination' column values
def rename_combination(combination):
    for key in column_map:
        combination = combination.replace(key, column_map[key].replace(' ', ''))
    return combination

# Apply the mapping to the 'Combination', 'Feature', and 'FeatureRelation' columns
data['Combination'] = data['Combination'].apply(rename_combination)
data['Feature'] = data['Feature'].map(column_map)
data['FeatureRelation'] = data['FeatureRelation'].map(column_map)

# Save the modified DataFrame to a new Excel file
data.to_excel(output_file_path, index=False)

print(f"File saved successfully to {output_file_path}")