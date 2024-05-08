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

- "corr_relation_test_terr_mammals.py" file execute the script to carried out Corr Tests for terr mammals against all combinations, all percentages for all features present in combinations. It first check significant of the feature if its there then we train model in which no missing entries and predict it and produce its result in folder --> "data_impute_project/corr_test/terrestrial_mammals". 

- imputation_summary.xlsx contains the RMSE of feature against the significant features. The remamed to orginal feature version can be found "data_impute_project/corr_test/terrestrial_mammals/imputation_summary_rename.xlsx".

data_impute_project/error_metrics/comparison_plots_fix_rmseaxis contains Rmse graphs for TMs of KNN, BR, RF for futher comparisons. Its renamed version present in  vai script rmse_graph_with_actual_cols_name.py





--- New

corr_relation_test_terr_mammals_rename_cols.py deals to rename Cols produce file imputation_summary_rename
corr_relation_test_terr_mammals.py runs to conduct CORR_TEST of teRR_MAM produce output corr_test/terrestrial_mammals


GRAPH--ss

rmse_graph_tm_actual_cols_actual_combination_name.py contains code to create Plots for RMSE against all combinations for each feature of all percentages. Also display the names of feature set which creates plots against percentages. Output lies in data_impute_project/graphs/rmse/plots/terrestrial_mammals


rmse_graph_tm_actual_cols_diff_combination_name.py works similar above but have modified version of Cols Name. Its output lies in data_impute_project/graphs/rmse/plots2/terrestrial_mammals