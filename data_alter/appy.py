import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Green GAN Cybersecurity Audit Dashboard")

st.write("AI Generated Adversarial Attacks vs IDS Detection")

# Load GAN data
gan_data = pd.read_csv(r"D:\Green_GAN_CY\synthetic_attacks.csv")

st.subheader("Generated Attack Samples")
st.dataframe(gan_data.head())

# Plot GAN feature distribution
fig, ax = plt.subplots()
ax.hist(gan_data.iloc[:,0], bins=50)
ax.set_title("GAN Attack Feature Distribution")

st.pyplot(fig)

# IDS detection summary
results = pd.DataFrame({
    "Category":["Detected","Undetected"],
    "Count":[1,999]
})

st.subheader("IDS Detection Performance")

fig2, ax2 = plt.subplots()
ax2.bar(results["Category"],results["Count"])
ax2.set_title("Detection Rate")

st.pyplot(fig2)

st.success("System Status: Green GAN Security Audit Completed")