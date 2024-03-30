import pandas as pd
import numpy as np
import os
from sklearn.impute import KNNImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

# Imputation functions
def impute_with_knn(df):
    imputer = KNNImputer(n_neighbors=5)
    imputed_data = imputer.fit_transform(df)
    return pd.DataFrame(imputed_data, columns=df.columns)

def impute_with_random_forest(df):
    rf_imputer = IterativeImputer(estimator=RandomForestRegressor(), max_iter=25, tol=0.05, random_state=0)
    imputed_data = rf_imputer.fit_transform(df)
    return pd.DataFrame(imputed_data, columns=df.columns)

def impute_with_mice(df):
    mice_imputer = IterativeImputer(max_iter=15, random_state=0)
    imputed_data = mice_imputer.fit_transform(df)
    return pd.DataFrame(imputed_data, columns=df.columns)

# Function to apply imputation and save the results
def impute_and_save(input_dir, base_output_dir, df, current_subdir):
    algorithms = {
        'KNN': impute_with_knn, 
        'RandomForest': impute_with_random_forest, 
        'MICE': impute_with_mice
    }
    
    # Modify the output directory to match the required structure
    modified_output_dir = current_subdir.replace('removed_data', 'algorithm_result')
    
    for name, func in algorithms.items():
        imputed_df = func(df.select_dtypes(include=[np.number]))  # Impute numeric columns
        result_file = f'result_data_{name}.xlsx'
        result_path = os.path.join(modified_output_dir, result_file)
        # Ensure the output directory exists
        os.makedirs(modified_output_dir, exist_ok=True)
        imputed_df.to_excel(result_path, index=False)
        print(f"Saved: {result_path}")

# Initial directory setup
base_dir = 'data_impute_project/removed_data/terrestrial_mammals'
output_base_dir = 'data_impute_project/algorithm_result/terrestrial_mammals'  # Base directory for output

# Iterate through each directory and file for imputation
for subdir, _, files in os.walk(base_dir):
    for file in files:
        if file.endswith("missing_data.xlsx"):
            file_path = os.path.join(subdir, file)
            df = pd.read_excel(file_path)
            
            # Exclude non-numeric columns before imputation
            if not df.select_dtypes(include=[np.number]).empty:
                # Pass the base output directory and current subdir to the imputation function
                impute_and_save(subdir, output_base_dir, df, subdir)
