import pandas as pd
import numpy as np
import os
from sklearn.impute import KNNImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.linear_model import BayesianRidge
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer


# Imputation functions

def impute_with_knn(df):
    """
    The function impute_with_knn imputes missing values in a DataFrame using the K-Nearest Neighbors
    algorithm.
    
    :param df: The `df` parameter in the `impute_with_knn` function is expected to be a pandas DataFrame
    containing the data that you want to impute missing values for using the KNNImputer algorithm
    :return: The function `impute_with_knn` returns a pandas DataFrame containing the imputed data after
    applying K-Nearest Neighbors (KNN) imputation on the input DataFrame `df`.
    """
    # The line `imputer = KNNImputer(n_neighbors=10)` is creating an instance of the K-Nearest
    # Neighbors (KNN) imputer object with a parameter `n_neighbors=10`. This means that the KNN
    # imputer will use the 10 nearest neighbors to impute missing values in the dataset based on the
    # values of the nearest neighbors.
    imputer = KNNImputer(n_neighbors=10)
    imputed_data = imputer.fit_transform(df)
    return pd.DataFrame(imputed_data, columns=df.columns)

def impute_with_random_forest(df):
    """
    The function impute_with_random_forest uses a Random Forest regressor to impute missing values in a
    DataFrame.
    
    :param df: It seems like you were about to provide the DataFrame `df` as an input to the
    `impute_with_random_forest` function. If you provide me with the DataFrame `df`, I can help you
    further with imputing missing values using the Random Forest algorithm. Please provide the DataFrame
    `
    :return: The function `impute_with_random_forest` returns a pandas DataFrame containing the imputed
    data after applying the Random Forest-based imputation technique using the IterativeImputer with
    specified parameters.
    """
    rf_imputer = IterativeImputer(estimator=RandomForestRegressor(), max_iter=25, tol=0.05, random_state=0)
    imputed_data = rf_imputer.fit_transform(df)
    return pd.DataFrame(imputed_data, columns=df.columns)


# def impute_with_bayesian_ridge(df):
#     br_imputer = IterativeImputer(estimator=BayesianRidge(), max_iter=25, tol=0.05, random_state=0)
#     imputed_data = br_imputer.fit_transform(df)
#     return pd.DataFrame(imputed_data, columns=df.columns)



def impute_with_svm(df):
    """
    The function `impute_with_svm` uses Support Vector Regression (SVR) to impute missing values in a
    DataFrame by predicting them based on the other numerical features after scaling and imputing.
    
    :param df: It looks like the code you provided is a function that imputes missing values in a
    DataFrame using Support Vector Regression (SVR) with the help of StandardScaler and SimpleImputer
    :return: The function `impute_with_svm` returns the input DataFrame `df` with missing values imputed
    using Support Vector Regression (SVR) based on the other numerical features in the DataFrame.
    """
    df_numeric = df.select_dtypes(include=[np.number])
    scaler = StandardScaler()
    imputer = SimpleImputer(strategy='mean')
    
    for column in df_numeric.columns:
        not_missing = df_numeric[df_numeric[column].notna()]
        features = not_missing.drop(columns=[column])
        target = not_missing[column]
        
        # Impute missing values in the features
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

# def impute_with_mice(df):
#     mice_imputer = IterativeImputer(max_iter=15, random_state=0)
#     imputed_data = mice_imputer.fit_transform(df)
#     return pd.DataFrame(imputed_data, columns=df.columns)

# Function to apply imputation and save the results
def impute_and_save(input_dir, base_output_dir, df, current_subdir):
    algorithms = {
        'KNN': impute_with_knn, 
        'RandomForest': impute_with_random_forest,
        # 'BayesianRidge': impute_with_bayesian_ridge,
        'SVM': impute_with_svm
        #'MICE': impute_with_mice
    }
    
    # Modify the output directory to match the required structure
    modified_output_dir = current_subdir.replace('removed_data', 'algorithm_result')
    
    # Iterating over a dictionary called `algorithms`, where the keys are
    # algorithm names ('KNN', 'RandomForest', 'SVM') and the values are the corresponding imputation
    # functions (`impute_with_knn`, `impute_with_random_forest`, `impute_with_svm`).
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

# Iterating through each directory and file for imputation in the `base_dir` directory using `os.walk()`
for subdir, _, files in os.walk(base_dir):
    for file in files:
        if file.endswith("missing_data.xlsx"):
            file_path = os.path.join(subdir, file)
            df = pd.read_excel(file_path)
            
            # Exclude non-numeric columns before imputation
            if not df.select_dtypes(include=[np.number]).empty:
                # Pass the base output directory and current subdir to the imputation function
                impute_and_save(subdir, output_base_dir, df, subdir)
