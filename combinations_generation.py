import pandas as pd
import os
import time

# Define base directories for data storage and combinations output
base_data_dir = 'data_impute_project/data'
base_combination_dir = 'data_impute_project/combinations'

# Define a dictionary mapping data file categories to their respective column combinations
# It makes simple and memory efficient way for further processessing it, cz we need need to save numerous combination after executing algos
combinations_map = {
    'mammals_without_humans': [list('ABCD'), list('ABCDE'), list('ABCDF')],
    'terrestrial_mammals': [list('ABCD'), list('ABCDE'), list('ABCDF')],
    'marine_mammals': [list('ABCD'), list('ABCDE'), list('ABCDF')],
    'terrestrial_herbivorous_mammals':[list('ABCD'), list('ABCDE'), list('ABCDF')],
    'terr_herb_and_marine_mammals':[list('ABCD'), list('ABCDE'), list('ABCDF')],
    'fish': [list('ABCD')],  # Fish and bird have only one combination, A to I
    'bird': [list('ABCD')],
    'human': [
        list('ABCD'), 
        list('ABCDE'), 
        list('ABCDF'), 
        list('ABCDG'), 
        list('ABCDH')
    ]
}

# Function to remove rows with missing values from specified columns in a dataframe
def remove_missing_values(df, cols):
    """
    Remove rows in the dataframe where any of the specified columns have missing values.

    Parameters:
    df (DataFrame): The pandas DataFrame to process.
    cols (list): List of columns to check for missing values.

    Returns:
    DataFrame: A DataFrame with rows containing missing values in 'cols' removed.
    """
    return df.dropna(subset=cols)

# Start timing the processing
start_time = time.time()

# Iterate through each category and its respective combinations of columns
for file_name, combos in combinations_map.items():
    file_path = os.path.join(base_data_dir, f"{file_name}.xlsx")
    df = pd.read_excel(file_path)

    # Iterate each set of column combinations for current category
    for idx, combination in enumerate(combos, start=1):
        # Create dir for this category if it does not exist
        category_dir = os.path.join(base_combination_dir, file_name)
        os.makedirs(category_dir, exist_ok=True)
        
        # Create subset of DataFrame with selected columns and remove rows with missing values
        combo_df = remove_missing_values(df[combination], combination)
        
        # Construct the combination filename with column labels
        cols_in_filename = ''.join(combination)
        combo_filename = f"combination_{idx}_{cols_in_filename}.xlsx"  # Updated filename
        combo_filepath = os.path.join(category_dir, combo_filename)
        
        # Save the cleaned DataFrame to an Excel file in the designated directory
        combo_df.to_excel(combo_filepath, index=False)
# Measure the end time to evaluate the duration of the process
end_time = time.time()

# Print the execution time and a success message
print(f"Running time for generating combinations: {end_time - start_time:.2f} seconds.")
print("Combs created and saved successfully...:)")