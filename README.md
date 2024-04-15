"Correlation between differnet features"

corr_all_comb find correlation in all files and corr_human find correlation in human file

create_multipl_corr_combinations files produce the Corr Factor and P values of all the combination of istope dataset

We produced file min_error_analysis_with_feature_combination to get result of feature A/B or any which combination of removal gives us min of (RMSE and NRMSE). append that with column name "FeatureSet Removal Scenario" 

- Also calculate runtime of script error_combinations.py which outputs 67.5 seconds on system
2x AMD Epyc 7313 (Milan), 32 cores (3.0GHz), 512GB main memory
NVIDIA GPU: Quadro RTX 4000
144 tensor cores, 2304 CUDA cores, 8GB GPU memory
416Gb/s memory bandwidth

- The folder error_metrics/comparison_plots includes files that feature a dynamic RMSE (Root Mean Square Error) Y-axis for comparisons.
- The folder error_metrics/comparison_plots_fix_rmseaxis includes files that have a standardized RMSE (Root Mean Square Error) Y-axis, which allows for more detailed and comparative analysis of the data. 