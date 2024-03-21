import pandas as pd
import numpy as np
import os
from sklearn.impute import KNNImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.experimental import enable_iterative_imputer  # noqa
from sklearn.impute import IterativeImputer

# Imputation functions
def impute_with_knn(df):
    imputer = KNNImputer(n_neighbors=5)
    imputed_data = imputer.fit_transform(df)
    return pd.DataFrame(imputed_data, columns=df.columns)

def impute_with_random_forest(df):
    rf_imputer = IterativeImputer(estimator=RandomForestRegressor(), max_iter=25,tol=0.05, random_state=0)
    imputed_data = rf_imputer.fit_transform(df)
    return pd.DataFrame(imputed_data, columns=df.columns)

def impute_with_mice(df):
    mice_imputer = IterativeImputer(max_iter=15, random_state=0)
    imputed_data = mice_imputer.fit_transform(df)
    return pd.DataFrame(imputed_data, columns=df.columns)

# Function to apply imputation and save the results
def impute_and_save(input_dir, output_dir, df):
    algorithms = {
        'KNN': impute_with_knn, 
        'RandomForest': impute_with_random_forest, 
        'MICE': impute_with_mice
    }
    
    for name, func in algorithms.items():
        imputed_df = func(df.select_dtypes(include=[np.number]))  # Impute numeric columns
        result_file = f'result_data_{name}.xlsx'
        result_path = os.path.join(output_dir, result_file)
        imputed_df.to_excel(result_path, index=False)
        print(f"Saved: {result_path}")

# Directory setup
base_dir = 'data_impute_project/removed_data/terrestrial_mammals/combination_1_ABCD'
output_base_dir = base_dir  # Assuming output in the same base directory for simplicity

# Iterate through each directory and file for imputation
for subdir, _, files in os.walk(base_dir):
    for file in files:
        if file.endswith("missing_data.xlsx"):
            file_path = os.path.join(subdir, file)
            df = pd.read_excel(file_path)
            
            # Exclude non-numeric columns before imputation
            if not df.select_dtypes(include=[np.number]).empty:
                impute_and_save(subdir, subdir, df)