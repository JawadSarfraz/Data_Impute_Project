"Correlation between differnet features"

corr_all_comb find correlation in all files and corr_human find correlation in human file

multiple_corr_test_combinations_rename.py files produce the Corr Factor and P values with actual feature names of all the combination of istope dataset

We produced file min_error_analysis_with_feature_combination to get result of feature A/B or any which combination of removal gives us min of (RMSE and NRMSE). append that with column name "FeatureSet Removal Scenario"

- Also calculate runtime of script error_combinations.py which outputs 67.5 seconds on system
  2x AMD Epyc 7313 (Milan), 32 cores (3.0GHz), 512GB main memory
  NVIDIA GPU: Quadro RTX 4000
  144 tensor cores, 2304 CUDA cores, 8GB GPU memory
  416Gb/s memory bandwidth

-The file "rmse_graph_with_actual_cols_name.py" is designed to generate RMSE (Root Mean Square Error) graphs for comparing features, and replace column labels like A, B, etc with specific names such as "δ13C coll, δ15N coll." These graphs are stored in the directory "data_impute_project/graphs/rmse/plots/terrestrial_mammals".

- "corr_relation_test_terr_mammals.py" file execute the script to carried out Corr Tests for terr mammals against all combinations, all percentages for all features present in combinations. It first check significant of the feature if its there then we train model in which no missing entries and predict it and produce its result in folder --> "data_impute_project/corr_test/terrestrial_mammals".
- imputation_summary.xlsx contains the RMSE of feature against the significant features. The remamed to orginal feature version can be found "data_impute_project/corr_test/terrestrial_mammals/imputation_summary_rename.xlsx".

--- New

corr_relation_test_terr_mammals_rename_cols.py deals to rename Cols produce file imputation_summary_rename
corr_relation_test_terr_mammals.py runs to conduct CORR_TEST of teRR_MAM produce output corr_test/terrestrial_mammals

GRAPH--ss

rmse_graph_tm_actual_cols_actual_combination_name.py contains code to create Plots for RMSE against all combinations for each feature of all percentages. Also display the names of feature set which creates plots against percentages. Output lies in data_impute_project/graphs/rmse/plots/terrestrial_mammals

rmse_graph_tm_actual_cols_diff_combination_name.py works similar above but have modified version of Cols Name. Its output lies in data_impute_project/graphs/rmse/plots2/terrestrial_mammals

MAE calculated only those whose value changed, to get accurate and right error result for further analysis and draw plots.
Removed RMSE cz it gives more priority to outliers, which alters results. It misleads the results

Integrate SVM implementation and produce the resulted files for Terr Mammals

-- modified_dataset contains updated ID's of each species so this would be utilize for further calculations

-- graphs are being tested initially but its need more working to finalize it...

-- split_dataset script updates to work for the modified file so that it update file to consider ID's of species as well.

-- combination_generation is being modified so it produce combinations along with ID embed in it.

-- percentage_removal_data_from_features is being implementated to cater the ID values, it ignore the ID while removing data.

-- Scripts are being Updated so that it works with new Dataset contains ID's of every Rows

-- All plot of median with outliers of each algos with every combinations of every featureSets are present in plots dir for terr mammals - scripts for it is --> generate_box_plot_algos_comparisons

-- Scatter plots of MAE being created contains all features of all combinations in which all featureSet, algos and FeatureSet are present of terr mammals

-- find_min_mae_tm script generate file contains min MAE of all features of all combinations for particular algo, it process file --> error_analysis_with_all_featureset.csv to determine it..

-- Well some scripts gives quite bad err--> NEED UPDATES to imputatioan_comparison, imp_test,imputatioan_comparison_with_outliers, generate_box_plot_algos_comparison

-- generate_mae_scatter_plots_tm --> Script use to generate Scatter Plots for Feature against all Feature Set in all combinations of **Terr Mammals,** output is present in **mae_scatter_plots** dir

-- impute_algorithms --> Script updated so that **RandomForest** algorithm embed with **MICE** algorithm so that both work together to get better result
