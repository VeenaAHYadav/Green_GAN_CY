import pandas as pd
import matplotlib.pyplot as plt

# IDS results
data = {
    "Category": ["Detected Attacks", "Undetected Attacks"],
    "Count": [1, 999]   # replace with your results
}

df = pd.DataFrame(data)

plt.figure()
plt.bar(df["Category"], df["Count"])
plt.title("IDS Detection Performance Against GAN Attacks")
plt.ylabel("Number of Samples")
plt.xlabel("Detection Category")

plt.savefig("detection_results.png")
plt.show()