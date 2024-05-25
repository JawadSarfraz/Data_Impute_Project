import pandas as pd
import os

base_data_dir = 'data_impute_project/data'
base_combination_dir = 'data_impute_project/combinations'

# Mapping of files to their required combinations
combinations_map = {
    'mammals_without_humans': [list('ABCDEFGHI'), list('ABCDEFGHIJ')],
    'terrestrial_mammals': [list('ABCDEFGHI'), list('ABCDEFGHIJ'), list('ABCDEFGHIK')],
    'marine_mammals': [list('ABCDEFGHI'), list('ABCDEFGHIJ'), list('ABCDEFGHIK')],
    'terrestrial_herbivorous_mammals': [list('ABCDEFGHI'), list('ABCDEFGHIJ'), list('ABCDEFGHIK')],
    'terr_herb_and_marine_mammals': [list('ABCDEFGHI'), list('ABCDEFGHIJ'), list('ABCDEFGHIK')],
    'fish': [list('ABCDEFGHI')],  # Fish and bird have only one combination, A to I
    'bird': [list('ABCDEFGHI')],
    'human': [
        list('ABCDEFGHI'), 
        list('ABCDEFGHIJ'), 
        list('ABCDEFGHIK'), 
        list('ABCDEFGHIL'), 
        list('ABCDEFGHIM')
    ]
}
# Remove rows with missing values in specified columns
def remove_missing_values(df, cols):
    """
    Removes rows from a DataFrame where any of the specified columns have missing values (NaN).

    Params:
    df: The DataFrame from which to remove missing values.
    cols (list): A list of column names in DataFrame where missing values are to be checked.

    Returns:
    pandas.DataFrame: DataFrame with rows containing missing values in the specified columns removed.

    Explanation:
    - `df.dropna(subset=cols)`: This method is called on DataFrame 'df'. The `dropna` function is used to drop rows that contain missing values.
        - The `subset` parameter specifies in which columns to look for missing values. Only rows that have NaNs in these specified columns are removed.
    - The function then returns DataFrame after specified rows with missing values have been removed.
    """
    return df.dropna(subset=cols)

# Iterating over each file in the `combinations_map` dictionary and its corresponding combinations.
for file_name, combos in combinations_map.items():
    # Read the dataset
    file_path = os.path.join(base_data_dir, f"{file_name}.xlsx")
    df = pd.read_excel(file_path)

    # Iterate through each combination for the current file
    for idx, combination in enumerate(combos, start=1):
        # Create the directory for this category if it does not exist
        category_dir = os.path.join(base_combination_dir, file_name)
        os.makedirs(category_dir, exist_ok=True)
        
        # Create combination DataFrame and remove rows with missing values
        combo_df = remove_missing_values(df[combination], combination)
        
        # Construct the combination filename with column labels
        cols_in_filename = '_'.join(combination)
        combo_filename = f"combination_{idx}_{cols_in_filename}.xlsx"  # Updated filename
        combo_filepath = os.path.join(category_dir, combo_filename)
        
        combo_df.to_excel(combo_filepath, index=False)

print("Combs created and saved successfully...:)")