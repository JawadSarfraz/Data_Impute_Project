import os
def create_project_structure(base_path):
    """
    Create the project directory structure at the specified base path.
    """
    data_categories = [
        'mammals (without humans)', 'terrestrial mammals', 'marine mammals',
        'terrestrial herbivorous mammals', 'terr herb and marine mammals',
        'fish', 'birds', 'humans'
    ]
    
    directories = []
    
    # Add data directories
    for category in data_categories:
        directories.extend([
            f'data/{category}',
            f'combinations/{category}',
            f'removed_data/{category}',
            f'graphs/{category}'
        ])
        
    # Add algorithm directories
    algorithms = ['KNN', 'SVM', 'MICE']
    for algo in algorithms:
        for category in data_categories:
            directories.append(f'algorithms/{algo}/{category}')
            
    # Add results directories
    metrics = ['RMSE', 'accuracy']
    for metric in metrics:
        for category in data_categories:
            directories.append(f'results/{metric}/{category}')

    for directory in directories:
        path = os.path.join(base_path, directory)
        os.makedirs(path, exist_ok=True)
        print(f"Created directory: {path}")

# Basease path of project structure.
base_path = 'Data_Impute_Project'

create_project_structure(base_path)

print("Project directory structure has been set up successfully.")