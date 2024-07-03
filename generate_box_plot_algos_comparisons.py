# import pandas as pd
# import os
# import matplotlib.pyplot as plt
# import seaborn as sns

# def ensure_dir(directory):
#     """
#     Ensure the specified directory exists; create it if it does not.
    
#     Parameters:
#     directory (str): The path to the directory to check/create.
#     """
#     if not os.path.exists(directory):
#         os.makedirs(directory)

# def plot_box_plots(imputed_values_df, combination, feature_combination, feature_labels, percentage, seed, output_dir):
#     """
#     Plot box plots for the original and imputed values.
    
#     Parameters:
#     imputed_values_df (pd.DataFrame): DataFrame containing original and imputed values.
#     combination (str): Name of the combination for the plot titles.
#     feature_combination (str): Combination of feature names for the plot titles.
#     feature_labels (str): The descriptive labels of the features.
#     percentage (str): The percentage of data removed, used in the plot title.
#     seed (str): Seed used for the imputation, used in the plot title.
#     output_dir (str): Directory to save the plots.
#     """
#     plt.figure(figsize=(10, 6))
    
#     # Box plot
#     sns.boxplot(data=imputed_values_df[['OriginalDataValue', 'KNN', 'SVM', 'RF']])
#     plt.title(f'Combination {combination} of Feature {feature_combination} ({feature_labels}) ({percentage}%, {seed})')
#     plt.ylabel('Value')
    
#     # Save the plot
#     plot_output_path = os.path.join(output_dir, f"{seed}_box_plot_{percentage}.png")
#     plt.savefig(plot_output_path)
#     plt.close()
#     print(f"Saved plot: {plot_output_path}")

# # Ensure the output directory exists
# base_input_dir = 'data_impute_project/imputation_comparison'
# output_plot_dir = 'data_impute_project/plotsTest2'
# ensure_dir(output_plot_dir)

# # Column name mapping
# column_map = {
#     'A': 'δ13C coll',
#     'B': 'δ15N coll',
#     'C': 'δ13C carb',
#     'D': 'δ18O carb',
#     'E': 'δ34S coll',
#     'F': 'δ18O phos',
#     'G': '87Sr/86Sr bone',
#     'H': '87Sr/86Sr enamel'
# }

# # Iterate through the directory structure
# for root, dirs, files in os.walk(base_input_dir):
#     for file in files:
#         if file.endswith('_imputed_comparison.xlsx'):
#             file_path = os.path.join(root, file)
#             imputed_values_df = pd.read_excel(file_path)
            
#             # Extract combination, feature combination, percentage, and seed from the directory structure and filename
#             path_parts = root.split(os.sep)
#             combination = path_parts[-3]
#             feature_combination = path_parts[-2]
#             percentage = path_parts[-1]
#             seed = file.split('_')[0]
            
#             # Get the descriptive labels of the features from the column_map
#             feature_labels = "_".join(column_map.get(feat, feat) for feat in feature_combination)
            
#             # Create output directory for plots
#             plot_output_dir = os.path.join(output_plot_dir, *path_parts[1:-2], feature_combination, percentage)
#             ensure_dir(plot_output_dir)
            
#             # Plot and save the box plot
#             plot_box_plots(imputed_values_df, combination, feature_combination, feature_labels, percentage, seed, plot_output_dir)


# import pandas as pd
# import os
# import matplotlib.pyplot as plt
# import seaborn as sns

# def ensure_dir(directory):
#     """
#     Ensure the specified directory exists; create it if it does not.
    
#     Parameters:
#     directory (str): The path to the directory to check/create.
#     """
#     if not os.path.exists(directory):
#         os.makedirs(directory)

# def plot_box_plots(imputed_values_df, combination, target_feature, feature_combination, percentage, seed, output_dir):
#     """
#     Plot box plots for the original and imputed values.
    
#     Parameters:
#     imputed_values_df (pd.DataFrame): DataFrame containing original and imputed values.
#     combination (str): Name of the combination for the plot titles.
#     target_feature (str): Target feature name for the plot titles.
#     feature_combination (str): Combination of feature names for the plot titles.
#     percentage (str): The percentage of data removed, used in the plot title.
#     seed (str): Seed used for the imputation, used in the plot title.
#     output_dir (str): Directory to save the plots.
#     """
#     plt.figure(figsize=(10, 6))
    
#     # Box plot
#     sns.boxplot(data=imputed_values_df[['OriginalDataValue', 'KNN', 'SVM', 'RF']])
#     plt.title(f'Combination {combination}, Feature {target_feature} with Feature Set {feature_combination} ({percentage}%, {seed})')
#     plt.ylabel('Value')
    
#     # Save the plot
#     plot_output_path = os.path.join(output_dir, f"{seed}_box_plot_{percentage}.png")
#     plt.savefig(plot_output_path)
#     plt.close()
#     print(f"Saved plot: {plot_output_path}")

# # Ensure the output directory exists
# base_input_dir = 'data_impute_project/imputation_comparison'
# output_plot_dir = 'data_impute_project/plotsTest3'
# ensure_dir(output_plot_dir)

# # Iterate through the directory structure
# for root, dirs, files in os.walk(base_input_dir):
#     for file in files:
#         if file.endswith('_imputed_comparison.xlsx'):
#             file_path = os.path.join(root, file)
#             imputed_values_df = pd.read_excel(file_path)
            
#             # Extract combination, target feature, feature combination, percentage, and seed from the directory structure and filename
#             path_parts = root.split(os.sep)
#             combination = path_parts[-4]
#             target_feature = path_parts[-3]
#             feature_combination = path_parts[-2]
#             percentage = path_parts[-1]
#             seed = file.split('_')[0]
            
#             # Create output directory for plots
#             plot_output_dir = os.path.join(output_plot_dir, *path_parts[1:-2], target_feature, feature_combination, percentage)
#             ensure_dir(plot_output_dir)
            
#             # Plot and save the box plot
#             plot_box_plots(imputed_values_df, combination, target_feature, feature_combination, percentage, seed, plot_output_dir)





import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

def ensure_dir(directory):
    """
    Ensure the specified directory exists; create it if it does not.
    
    Parameters:
    directory (str): The path to the directory to check/create.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

def plot_box_plots(imputed_values_df, combination, target_feature, feature_combination, percentage, seed, output_dir):
    """
    Plot box plots for the original and imputed values.
    
    Parameters:
    imputed_values_df (pd.DataFrame): DataFrame containing original and imputed values.
    combination (str): Name of the combination for the plot titles.
    target_feature (str): Target feature name for the plot titles.
    feature_combination (str): Combination of feature names for the plot titles.
    percentage (str): The percentage of data removed, used in the plot title.
    seed (str): Seed used for the imputation, used in the plot title.
    output_dir (str): Directory to save the plots.
    """
    plt.figure(figsize=(10, 6))
    
    # Box plot
    sns.boxplot(data=imputed_values_df[['OriginalDataValue', 'KNN', 'SVM', 'RF']])
    plt.title(f'Combination {combination}, Feature {target_feature} with Feature Set {feature_combination} ({percentage}%, {seed})')
    plt.ylabel('Value')
    
    # Save the plot
    plot_output_path = os.path.join(output_dir, f"{seed}_box_plot_{percentage}.png")
    plt.savefig(plot_output_path)
    plt.close()
    print(f"Saved plot: {plot_output_path}")

# Ensure the output directory exists
base_input_dir = 'data_impute_project/imputation_comparison'
output_plot_dir = 'data_impute_project/plotsTest3'
ensure_dir(output_plot_dir)

# Iterate through the directory structure
for root, dirs, files in os.walk(base_input_dir):
    for file in files:
        if file.endswith('_imputed_comparison.xlsx'):
            file_path = os.path.join(root, file)
            imputed_values_df = pd.read_excel(file_path)
            
            # Extract combination, target feature, feature combination, percentage, and seed from the directory structure and filename
            path_parts = root.split(os.sep)
            combination = path_parts[-4]
            target_feature = path_parts[-3]
            feature_combination = path_parts[-2]
            percentage = path_parts[-1]
            seed = file.split('_')[0]
            
            # Create output directory for plots
            plot_output_dir = os.path.join(output_plot_dir, *path_parts[1:-2], target_feature, feature_combination, percentage)
            ensure_dir(plot_output_dir)
            
            # Plot and save the box plot
            plot_box_plots(imputed_values_df, combination, target_feature, feature_combination, percentage, seed, plot_output_dir)