import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report


print("Loading dataset...")

X = np.load(r"D:\Green_GAN_CY\dataset\processed_features.npy")
y = np.load(r"D:\Green_GAN_CY\dataset\processed_labels.npy")

print("Dataset loaded")
print("Feature shape:", X.shape)


# For faster training (recommended)
X = X[:300000]
y = y[:300000]

print("Using subset:", X.shape)


# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))


print("Training IDS model...")

model = RandomForestClassifier(
    n_estimators=100,
    n_jobs=-1,
    random_state=42
)

model.fit(X_train, y_train)

print("Training complete!")


# Evaluation
predictions = model.predict(X_test)

print("\nDetection Performance\n")

print(classification_report(y_test, predictions))


# Save IDS model
joblib.dump(model, "ids_model.pkl")

print("\nIDS model saved as ids_model.pkl")