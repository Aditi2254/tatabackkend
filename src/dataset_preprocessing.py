import json
import pandas as pd
import numpy as np
import os

def load_material_data():
    # Load the materials data from the JSON file
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Path to the dataset in the 'data' folder outside 'src'
    DATASET_PATH = os.path.join(BASE_DIR, 'data', 'recommendation_dataset.json')
    with open(DATASET_PATH) as f:
        data = json.load(f)
    
    materials = data['materials']
    material_list = []
    
    # Convert JSON structure into a list of dictionaries
    for material, properties in materials.items():
        material_info = properties.copy()
        material_info['Material'] = material  # Add the material name as a new column
        material_list.append(material_info)
    
    # Create a pandas DataFrame from the list
    df = pd.DataFrame(material_list)
    return df

def preprocess_data(df):
    # Select only numeric columns for mean imputation
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    # Fill missing values for numeric columns with their mean
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

    # Handle non-numeric columns (e.g., 'Recommended Parts')
    if 'recommended_parts' in df.columns:
        # Ensure the 'Recommended Parts' column is a list and handle missing values
        df['Recommended Parts'] = df['recommended_parts'].apply(lambda x: x if isinstance(x, list) else [])

    return df

if __name__ == "__main__":
    file_path = r"Ecomaterial-Advisor-Backend\data\datasettt.json"   # Path to your JSON dataset
    
    df = load_material_data(file_path)  # Load the data into a DataFrame
    df = preprocess_data(df)  # Preprocess the data (handle missing values)
    
    print(df.head())  # Display the first few rows of the DataFrame