import pandas as pd
import os
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# -----------------------------
# Step 1: Load all CSV datasets
# -----------------------------

dataset_path = "D:\Green_GAN_CY\dataset"

csv_files = [f for f in os.listdir(dataset_path) if f.endswith(".csv")]

print("CSV files found:", csv_files)

dataframes = []

for file in csv_files:

    file_path = os.path.join(dataset_path, file)

    print("Loading:", file)

    df = pd.read_csv(file_path)

    dataframes.append(df)

# merge all datasets
data = pd.concat(dataframes, ignore_index=True)

# remove spaces in column names
data.columns = data.columns.str.strip()

print("\nDatasets merged successfully")
print("Dataset shape:", data.shape)

print("\nColumns in dataset:")
print(data.columns)


# -----------------------------
# Step 2: Remove infinite values
# -----------------------------

data = data.replace([np.inf, -np.inf], np.nan)


# -----------------------------
# Step 3: Remove missing values
# -----------------------------

print("\nMissing values before cleaning:", data.isnull().sum().sum())

data = data.dropna()

print("Dataset shape after removing missing values:", data.shape)


# -----------------------------
# Step 4: Convert attack labels
# -----------------------------

# BENIGN = 0 (normal)
# other attacks = 1

data['Label'] = data['Label'].apply(lambda x: 0 if x == 'BENIGN' else 1)

print("\nLabel distribution:")
print(data['Label'].value_counts())


# -----------------------------
# Step 5: Separate features and labels
# -----------------------------

X = data.drop("Label", axis=1)

y = data["Label"]

print("\nFeature shape:", X.shape)
print("Label shape:", y.shape)


# -----------------------------
# Step 6: Normalize features
# -----------------------------

scaler = MinMaxScaler()

X_scaled = scaler.fit_transform(X)

print("\nFeature normalization complete")


# -----------------------------
# Step 7: Save processed dataset
# -----------------------------

np.save("dataset/processed_features.npy", X_scaled)
np.save("dataset/processed_labels.npy", y)

print("\nProcessed dataset saved successfully")

print("\nPreprocessing completed!")