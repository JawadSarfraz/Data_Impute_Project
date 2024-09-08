import numpy as np
from sklearn.impute import KNNImputer
from sklearn.ensemble import RandomForestRegressor

class HybridKNNRandomForestImputer:
    def __init__(self, n_neighbors=5, n_estimators=100, max_iterations=10, threshold=1e-4, random_state=20):
        """
        Initializes parameters for KNN imputer and Random Forest regressor with default values.
        
        Params:
        n_neighbors: it specifies number of neighboring samples to use for imputation in KNNImputer. 
        It determines how many nearest neighbors will be considered when imputing missing values in the dataset. in our case its 5.
        n_estimators: determine number of trees in random forest ensemble. In our case its 100.
        max_iterations: set 10 as maximum iteration. It tells maximum number of iterations that will be performed
        threshold: thresold is `0.0001`, its convergence criteria for algorithm
        random_state: set the random seed for reproducibility in algorithms.
        """
        self.n_neighbors = n_neighbors
        self.n_estimators = n_estimators
        self.max_iterations = max_iterations
        self.threshold = threshold
        self.random_state = random_state
        self.knn_imputer = KNNImputer(n_neighbors=self.n_neighbors)
        self.rf_regressor = RandomForestRegressor(n_estimators=self.n_estimators, random_state=self.random_state)

    def fit_transform(self, X):
        """
        Performs iterative imputation using KNN and Random Forest methods until convergence is reached.
        
        Params:
        X: Its input data which needs to be imputed using a combination of KNN imputation and
        Random Forest imputation techniques.


        return: returns the final imputed dataset after the iterative imputation process.
        """
        # Initial KNN Imputation
        X_imputed = self.knn_imputer.fit_transform(X)
        previous_imputation = np.copy(X_imputed)
        
        for iteration in range(self.max_iterations):
            # Random Forest Imputation
            X_rf_imputed = self._random_forest_impute(X, X_imputed)
            
            # KNN Refinement
            X_imputed = self.knn_imputer.fit_transform(X_rf_imputed)
            
            # Check for convergence
            change = np.abs(X_imputed - previous_imputation).mean()
            if change < self.threshold:
                print(f"Convergence reached after {iteration+1} iterations.")
                break
                
            previous_imputation = np.copy(X_imputed)
            
        return X_imputed
    
    def _random_forest_impute(self, X_original, X_imputed):
        """
        It impute missing values in dataset using random forest regressor.
        
        Params:
        X_original: X_original is original dataset with missing values
        X_imputed: X_imputed is input data with missing values
        
        return: returns the imputed dataset after filling in missing values using a random forest regressor.
        """
        X_rf_imputed = np.copy(X_imputed)
        
        for i in range(X_original.shape[1]):
            missing_mask = np.isnan(X_original[:, i])
            if missing_mask.any():
                X_train = np.delete(X_rf_imputed, i, axis=1)
                y_train = X_rf_imputed[:, i]
                
                self.rf_regressor.fit(X_train[~missing_mask], y_train[~missing_mask])
                X_rf_imputed[missing_mask, i] = self.rf_regressor.predict(X_train[missing_mask])
                
        return X_rf_imputed