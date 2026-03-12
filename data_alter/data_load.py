import pandas as pd
import os

# path to dataset folder
dataset_path = "D:\Green_GAN_CY\dataset"

# list all csv files
csv_files = [f for f in os.listdir(dataset_path) if f.endswith(".csv")]

print("\nCSV files found:", csv_files)

# store datasets
dataframes = []

for file in csv_files:
    
    file_path = os.path.join(dataset_path, file)
    
    print("Loading:", file)
    
    df = pd.read_csv(file_path)
    
    dataframes.append(df)

# combine all datasets
combined_data = pd.concat(dataframes, ignore_index=True)

print("\nAll datasets merged successfully!")

print("Final dataset shape:", combined_data.shape)

print("\nFirst 5 rows:")
print(combined_data.head())

print("\nColumns:")
print(combined_data.columns)