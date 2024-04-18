"Correlation between differnet features"

corr_all_comb find correlation in all files and corr_human find correlation in human file

multiple_corr_test_combinations_rename.py files produce the Corr Factor and P values with actual feature names of all the combination of istope dataset

We produced file min_error_analysis_with_feature_combination to get result of feature A/B or any which combination of removal gives us min of (RMSE and NRMSE). append that with column name "FeatureSet Removal Scenario" 

- Also calculate runtime of script error_combinations.py which outputs 67.5 seconds on system
2x AMD Epyc 7313 (Milan), 32 cores (3.0GHz), 512GB main memory
NVIDIA GPU: Quadro RTX 4000
144 tensor cores, 2304 CUDA cores, 8GB GPU memory
416Gb/s memory bandwidth

- The folder error_metrics/comparison_plots includes files that feature a dynamic RMSE (Root Mean Square Error) Y-axis for comparisons.
- The folder error_metrics/comparison_plots_fix_rmseaxis includes files that have a standardized RMSE (Root Mean Square Error) Y-axis, which allows for more detailed and comparative analysis of the data. 

-The file "rmse_graph_with_actual_cols_name.py" is designed to generate RMSE (Root Mean Square Error) graphs for comparing features, and replace column labels like A, B, etc with specific names such as "δ13C coll, δ15N coll." These graphs are stored in the directory "data_impute_project/graphs/rmse/plots/terrestrial_mammals".