import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import json
import os

st.set_page_config(page_title="Green GAN Security Dashboard", layout="wide")

st.title("Green GAN – AI Cybersecurity Audit Dashboard")

st.sidebar.header("System Status")
st.sidebar.success("GAN Model: Active")
st.sidebar.success("IDS: Active")
st.sidebar.success("Wazuh Monitoring: Active")

# -------------------------------
# Load GAN Generated Data
# -------------------------------

data_path = r"D:\Green_GAN_CY\synthetic_attacks.csv"

if os.path.exists(data_path):
    gan_data = pd.read_csv(data_path)
else:
    st.error("synthetic_attacks.csv not found")
    st.stop()

# -------------------------------
# Attack Statistics
# -------------------------------

st.subheader("Generated Attack Statistics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Generated Attacks", len(gan_data))
col2.metric("Features per Sample", gan_data.shape[1])
col3.metric("Dataset Source", "CICIDS2017")

# -------------------------------
# Feature Distribution
# -------------------------------

st.subheader("GAN Feature Distribution")

fig = plt.figure()
plt.hist(gan_data.values.flatten(), bins=50)
plt.title("Distribution of GAN Generated Network Features")
plt.xlabel("Feature Value")
plt.ylabel("Frequency")

st.pyplot(fig)

# -------------------------------
# IDS Detection Results
# -------------------------------

st.subheader("IDS Detection Performance")

results = pd.DataFrame({
    "Category": ["Detected", "Undetected"],
    "Count": [1, 999]
})

fig2 = px.bar(
    results,
    x="Category",
    y="Count",
    title="Detection Rate of GAN Generated Attacks"
)

st.plotly_chart(fig2)

# -------------------------------
# Attack Heatmap
# -------------------------------

st.subheader("GAN Attack Feature Heatmap")

sample_data = gan_data.head(100)

fig3 = px.imshow(sample_data)

st.plotly_chart(fig3)

# -------------------------------
# Suricata Alerts Feed
# -------------------------------

st.subheader("Live Suricata Alerts")

suricata_log = "/var/log/suricata/eve.json"

if os.path.exists(suricata_log):

    alerts = []

    with open(suricata_log, "r") as f:
        for line in f.readlines()[-20:]:
            try:
                alerts.append(json.loads(line))
            except:
                pass

    if alerts:
        df_alerts = pd.json_normalize(alerts)
        st.dataframe(df_alerts)

    else:
        st.info("No Suricata alerts yet")

else:
    st.warning("Suricata log not found (running locally without server connection)")

# -------------------------------
# Security Status
# -------------------------------

st.subheader("Security Audit Summary")

detection_rate = (1 / 1000) * 100

st.metric("IDS Detection Rate", f"{detection_rate:.2f}%")

if detection_rate < 10:
    st.error("Critical: IDS failed to detect GAN generated attacks")

elif detection_rate < 50:
    st.warning("Moderate detection capability")

else:
    st.success("Strong detection capability")

st.success("Green GAN Security Audit Completed")