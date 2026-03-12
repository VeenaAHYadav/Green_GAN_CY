import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv(r"D:\Green_GAN_CY\synthetic_attacks.csv")

plt.figure()
plt.hist(data.iloc[:,0], bins=50)

plt.title("Distribution of GAN Generated Network Features")
plt.xlabel("Feature Value")
plt.ylabel("Frequency")

plt.savefig("gan_distribution.png")
plt.show()