import sys
import os
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.linear_model import BayesianRidge
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import time

# Add relative path to hybrid_KNN_RF_Impute.py
module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'hybrid_KNN_RF_Impute.py'))
sys.path.append(os.path.dirname(module_path))

from hybrid_KNN_RF_Impute import HybridKNNRandomForestImputer


# Imputation functions
def impute_with_knn(df):
    imputer = KNNImputer(n_neighbors=10)
    imputed_data = imputer.fit_transform(df)
    return pd.DataFrame(imputed_data, columns=df.columns)

def impute_with_random_forest_MICE(df):
    rf_imputer = IterativeImputer(estimator=RandomForestRegressor(), max_iter=25, tol=0.05, random_state=0)
    imputed_data = rf_imputer.fit_transform(df)
    return pd.DataFrame(imputed_data, columns=df.columns)

def impute_with_random_forest(df, n_estimators=100, max_depth=None, random_state=None):
    df_numeric = df.select_dtypes(include=[np.number])
    for column in df_numeric.columns:
        not_missing = df_numeric[df_numeric[column].notna()]
        features = not_missing.drop(columns=[column])
        target = not_missing[column]
        
        model = RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth, random_state=random_state)
        model.fit(features, target)
        
        missing = df_numeric[df_numeric[column].isna()]
        if not missing.empty:
            missing_features = missing.drop(columns=[column])
            predicted_values = model.predict(missing_features)
            df.loc[missing.index, column] = predicted_values
    return df

def impute_with_svm(df):
    df_numeric = df.select_dtypes(include=[np.number])
    scaler = StandardScaler()
    imputer = SimpleImputer(strategy='mean')
    
    for column in df_numeric.columns:
        not_missing = df_numeric[df_numeric[column].notna()]
        features = not_missing.drop(columns=[column])
        target = not_missing[column]
        
        features_imputed = imputer.fit_transform(features)
        features_scaled = scaler.fit_transform(features_imputed)
        
        model = SVR()
        model.fit(features_scaled, target)
        
        missing = df_numeric[df_numeric[column].isna()]
        if not missing.empty:
            missing_features = missing.drop(columns=[column])
            missing_features_imputed = imputer.transform(missing_features)
            missing_features_scaled = scaler.transform(missing_features_imputed)
            predicted_values = model.predict(missing_features_scaled)
            df.loc[missing.index, column] = predicted_values
    return df

def impute_with_hybrid_knn_rf(df):
    df_numeric = df.select_dtypes(include=[np.number])
    imputer = HybridKNNRandomForestImputer(n_neighbors=5, n_estimators=100, max_iterations=10, threshold=1e-4)
    imputed_data = imputer.fit_transform(df_numeric.values)
    return pd.DataFrame(imputed_data, columns=df_numeric.columns)

def impute_and_save(input_dir, base_output_dir, df, current_subdir):
    algorithms = {
        'KNN': impute_with_knn, 
        'RandomForest': lambda df: impute_with_random_forest(df, n_estimators=200, max_depth=10, random_state=20),
        'SVM': impute_with_svm,
        'RandomForest_MICE': impute_with_random_forest_MICE,
        'HybridKNN_RF': impute_with_hybrid_knn_rf
    }
    
    modified_output_dir = current_subdir.replace('removed_data', 'impute_algos_result')
    id_col = df[['ID']]
    df_numeric = df.drop(columns=['ID'])
    
    for name, func in algorithms.items():
        imputed_df = func(df_numeric.select_dtypes(include=[np.number]))
        imputed_df = pd.concat([id_col, imputed_df], axis=1)
        result_file = f'result_data_{name}.xlsx'
        result_path = os.path.join(modified_output_dir, result_file)
        os.makedirs(modified_output_dir, exist_ok=True)
        imputed_df.to_excel(result_path, index=False)
        print(f"Saved: {result_path}")

# Prompt user for dataset type
dataset_type = input("Enter the dataset type (e.g., bird, fish, human, etc.): ").strip()

# Verify if entered dataset type is valid
datasets = ["bird", "fish", "human", "mammals_without_humans", "marine_mammals", 
            "terr_herb_and_marine_mammals", "terrestrial_herbivorous_mammals", "terrestrial_mammals"]
if dataset_type not in datasets:
    raise ValueError("Invalid dataset type entered. Please try again.")

# Set base paths
base_dir = os.path.join("..", f"data_impute_project/removed_data/{dataset_type}")
output_base_dir = os.path.join("..", f"data_impute_project/impute_algos_result/{dataset_type}")

# Start the timer
start_time = time.time()

# Iterate through each dir and file for imputation in the `base_dir` directory using `os.walk()`
for subdir, _, files in os.walk(base_dir):
    for file in files:
        if file.endswith("missing_data.xlsx"):
            file_path = os.path.join(subdir, file)
            df = pd.read_excel(file_path)
            
            if not df.select_dtypes(include=[np.number]).empty:
                impute_and_save(subdir, output_base_dir, df, subdir)

# Stop the timer
end_time = time.time()
elapsed_time = end_time - start_time

# Total execution time
print(f"Total execution time for processing the {dataset_type} dataset: {elapsed_time:.2f} seconds")