import pandas as pd
import os
import time

base_data_dir = 'data_impute_project/data'
base_combination_dir = 'data_impute_project/combinations'

# Mapping of files to their required combinations
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

# Remove rows with missing values in specified cols
def remove_missing_values(df, cols):
    return df.dropna(subset=cols)

# Iterate over each file and its combinations
start_time = time.time()
for file_name, combos in combinations_map.items():
    file_path = os.path.join(base_data_dir, f"{file_name}.xlsx")
    df = pd.read_excel(file_path)

    # Iterate through each combination for the current file
    for idx, combination in enumerate(combos, start=1):
        # Create dir for this category if it does not exist
        category_dir = os.path.join(base_combination_dir, file_name)
        os.makedirs(category_dir, exist_ok=True)
        
        # Create combination DataFrame and remove rows with missing values
        combo_df = remove_missing_values(df[combination], combination)
        
        # Construct the combination filename with column labels
        cols_in_filename = ''.join(combination)
        combo_filename = f"combination_{idx}_{cols_in_filename}.xlsx"  # Updated filename
        combo_filepath = os.path.join(category_dir, combo_filename)
        
        combo_df.to_excel(combo_filepath, index=False)
end_time = time.time()

print(f"Running time for generating combinations: {end_time - start_time:.2f} seconds.")
print("Combs created and saved successfully...:)")