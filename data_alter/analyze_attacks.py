import pandas as pd

data = pd.read_csv(r"D:\Green_GAN_CY\synthetic_attacks.csv")

print("Total samples:", len(data))

print("\nFeature Statistics\n")

print(data.describe())