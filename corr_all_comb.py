import pandas as pd
import os

def calculate_and_save_correlation_matrices(files, input_base_path, output_base_path):
    """
    Processes list of files, calculates correlation matrices from Excel data, and saves each matrix to new Excel file.
    
    Params:
    files: list of filenames to process
    input_base_path:Base path where the input Excel files are located. This function takes list of filenames (`files`),
    reads Excel files from `input_base_path`, calculates the correlation matrices for each file, and saves the resulting
    correlation matrices as new Excel files.
    output_base_path: Base path where output files will be saved. It is directory where newly created Excel files 
    containing correlation matrices will be stored
    """
    for file in files:
        try:
            # Construct paths for input/output
            input_file_path = os.path.join(input_base_path, file)
            output_file_path = os.path.join(output_base_path, file)
            
            os.makedirs(output_base_path, exist_ok=True)
            
            # Load Excel file
            df = pd.read_excel(input_file_path)
            
            # Calc corr matrix
            correlation_matrix = df.corr()
            
            # Save corr matrix to new Excel file
            correlation_matrix.to_excel(output_file_path)
            
            print(f"Correlation matrix for {file} saved to {output_file_path}")
        except Exception as e:
            print(f"Error occurred while processing {file}: {e}")

if __name__ == "__main__":
    # Base path for input Excel files
    input_base_path = "data_impute_project/data"
    
    # Base path for output Excel files to save
    output_base_path = "data_impute_project/corr_factor"
    
    # List of Files to process
    # List contains filenames of Excel files to be processed. These filenames represent different datasets 
    # related to mammals, fish, and birds etc.
    files = [
        'terrestrial_mammals.xlsx',
        'marine_mammals.xlsx',
        'terrestrial_herbivorous_mammals.xlsx',
        'terr_herb_and_marine_mammals.xlsx',
        'fish.xlsx',
        'mammals_without_humans.xlsx',
        'bird.xlsx',
    ]
    
    # Calculate corr matrices and save them to new Excel files
    calculate_and_save_correlation_matrices(files, input_base_path, output_base_path)