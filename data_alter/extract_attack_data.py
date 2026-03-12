import numpy as np

print("Loading dataset...")

X = np.load(r"D:\Green_GAN_CY\dataset\processed_features.npy")
y = np.load(r"D:\Green_GAN_CY\dataset\processed_labels.npy")

print("Dataset loaded")

print("Total samples:", len(X))

# Extract only attack samples
attack_data = X[y == 1]

print("Attack samples:", attack_data.shape)

# Save attack features
np.save("dataset/attack_features.npy", attack_data)

print("Attack dataset saved as attack_features.npy")