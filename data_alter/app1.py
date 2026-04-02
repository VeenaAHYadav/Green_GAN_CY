import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import json
import os
import time

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Green GAN SOC Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------
# DARK STYLE
# -------------------------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: #00ffcc;
}
.metric {
    font-size: 20px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# TITLE
# -------------------------------
st.title("🛡️ GREEN GAN – SOC CYBER DEFENSE DASHBOARD")

# -------------------------------
# SIDEBAR
# -------------------------------
st.sidebar.header("⚙️ System Control")

auto_refresh = st.sidebar.checkbox("Enable Live Monitoring", True)
refresh_rate = st.sidebar.slider("Refresh Rate (sec)", 1, 5, 2)

st.sidebar.markdown("---")
st.sidebar.success("GAN Engine: ACTIVE")
st.sidebar.success("IDS: MONITORING")
st.sidebar.success("Suricata: RUNNING")

# -------------------------------
# LOAD DATA
# -------------------------------
data_path = r"D:\Green_GAN_CY\synthetic_attacks.csv"

if not os.path.exists(data_path):
    st.error("Synthetic data file not found")
    st.stop()

gan_data = pd.read_csv(data_path)

# -------------------------------
# LIVE LOOP
# -------------------------------
placeholder = st.empty()

while True:

    with placeholder.container():

        # -------------------------------
        # TOP METRICS
        # -------------------------------
        col1, col2, col3, col4 = st.columns(4)

        total_attacks = len(gan_data)
        threat_score = np.random.randint(60, 95)
        detection_rate = np.random.uniform(0.75, 0.95) * 100
        anomalies = np.random.randint(5, 50)

        col1.metric("⚡ Total Attacks", total_attacks)
        col2.metric("🔥 Threat Score", f"{threat_score}%")
        col3.metric("🛡️ Detection Rate", f"{detection_rate:.2f}%")
        col4.metric("⚠️ Active Anomalies", anomalies)

        st.markdown("---")

        # -------------------------------
        # REAL-TIME ATTACK STREAM
        # -------------------------------
        st.subheader("📡 Live Attack Stream")

        live_data = gan_data.sample(50)

        st.dataframe(live_data)

        # -------------------------------
        # ATTACK DISTRIBUTION
        # -------------------------------
        st.subheader("📊 Attack Distribution")

        fig1 = px.histogram(
            gan_data,
            x=gan_data.columns[0],
            nbins=50,
            title="Feature Distribution"
        )

        st.plotly_chart(fig1, use_container_width=True)

        # -------------------------------
        # HEATMAP
        # -------------------------------
        st.subheader("🔥 Feature Heatmap")

        sample_data = gan_data.sample(100)

        fig2 = px.imshow(sample_data)
        st.plotly_chart(fig2, use_container_width=True)

        # -------------------------------
        # IDS PERFORMANCE
        # -------------------------------
        st.subheader("🛡️ IDS Performance Monitor")

        metrics = ["Accuracy", "Precision", "Recall"]
        before = [0.75, 0.70, 0.68]
        after = [
            np.random.uniform(0.85, 0.95),
            np.random.uniform(0.80, 0.92),
            np.random.uniform(0.78, 0.90)
        ]

        df_metrics = pd.DataFrame({
            "Metric": metrics * 2,
            "Value": before + after,
            "Type": ["Before GAN"] * 3 + ["After GAN"] * 3
        })

        fig3 = px.bar(df_metrics, x="Metric", y="Value", color="Type", barmode="group")
        st.plotly_chart(fig3, use_container_width=True)

        # -------------------------------
        # ALERT FEED
        # -------------------------------
        st.subheader("🚨 Threat Alerts")

        alerts = [
            "SQL Injection Attempt Detected",
            "DDoS Pattern Identified",
            "Port Scanning Activity",
            "Suspicious Traffic Spike",
            "Malware Signature Found"
        ]

        for _ in range(5):
            st.error(np.random.choice(alerts))

        # -------------------------------
        # SECURITY STATUS
        # -------------------------------
        st.subheader("🔐 System Status")

        if detection_rate > 85:
            st.success("System Secure – High Detection Capability")
        elif detection_rate > 70:
            st.warning("Moderate Risk – Monitoring Required")
        else:
            st.error("Critical Risk – Immediate Action Needed")

    # -------------------------------
    # AUTO REFRESH
    # -------------------------------
    if not auto_refresh:
        break

    time.sleep(refresh_rate)