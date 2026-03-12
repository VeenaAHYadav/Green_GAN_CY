import pandas as pd
import joblib
import numpy as np

print("Loading IDS model...")

model = joblib.load(r"D:\Green_GAN_CY\ids_model.pkl")

print("Loading GAN generated attacks...")

data = pd.read_csv(r"D:\Green_GAN_CY\synthetic_attacks.csv")

X = data.values

print("Total generated samples:", len(X))

print("Running IDS detection...")

predictions = model.predict(X)

attack_detected = np.sum(predictions == 1)
normal_detected = np.sum(predictions == 0)

print("\nSecurity Audit Results\n")

print("Detected as ATTACK:", attack_detected)
print("Detected as NORMAL:", normal_detected)

detection_rate = attack_detected / len(X)

print("\nDetection Rate:", detection_rate * 100, "%")