import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import json
import os
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# ------------------- Page Config -------------------
st.set_page_config(page_title="Green GAN Live SOC Dashboard", layout="wide")
st.title("💻 Green GAN – Real-Time AI Cybersecurity SOC Dashboard")

# ------------------- Auto Refresh -------------------
# Refresh every 5 seconds
st_autorefresh(interval=5000, limit=None, key="live_refresh")

# ------------------- Load GAN Data -------------------
data_path = r"D:\Green_GAN_CY\synthetic_attacks.csv"
if os.path.exists(data_path):
    gan_data = pd.read_csv(data_path)
else:
    st.error(f"File not found at {data_path}")
    st.stop()

# ------------------- Suricata Logs -------------------
suricata_log = r"D:\Green_GAN_CY\data_alter\eve.json"

def get_last_suricata_alerts(log_path, last_lines=20):
    if not os.path.exists(log_path):
        return pd.DataFrame()
    alerts = []
    with open(log_path, "r") as f:
        lines = f.readlines()[-last_lines:]
        for line in lines:
            try:
                alerts.append(json.loads(line))
            except:
                pass
    if alerts:
        df = pd.json_normalize(alerts)
        # Add severity column for demo purposes
        if 'alert.signature' in df.columns:
            df['Severity'] = df['alert.signature'].apply(lambda x: 'High' if 'malware' in str(x).lower() else 'Medium')
        else:
            df['Severity'] = 'Low'
        df['Time'] = df.get('timestamp', pd.Timestamp.now())
        return df
    return pd.DataFrame()

# ------------------- Placeholders -------------------
attack_stats_ph = st.empty()
detection_chart_ph = st.empty()
trend_chart_ph = st.empty()
alerts_ph = st.empty()

# ------------------- Attack & IDS Stats -------------------
# Demo: replace with live IDS detection
total_attacks = len(gan_data)
detected = max(1, int(total_attacks * 0.05))
undetected = total_attacks - detected

attack_stats_ph.subheader("📊 GAN Attack Statistics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Generated Attacks", total_attacks)
col2.metric("Detected Attacks", detected)
col3.metric("Undetected Attacks", undetected)

# ------------------- Detection Rate Chart -------------------
detection_results = pd.DataFrame({
    "Category": ["Detected", "Undetected"],
    "Count": [detected, undetected]
})
fig = px.bar(detection_results, x="Category", y="Count",
             color="Category", color_discrete_map={"Detected":"green","Undetected":"red"},
             title="IDS Detection Status")
detection_chart_ph.plotly_chart(fig, use_container_width=True)

# ------------------- Detection Trend Over Time -------------------
st.subheader("📈 Detection Trend (Live)")

# Initialize trend data in session_state
if 'trend_data' not in st.session_state:
    st.session_state.trend_data = pd.DataFrame(columns=["Time", "Detected", "Undetected"])

# Create a proper new row DataFrame to avoid warnings
new_row = pd.DataFrame([{
    "Time": datetime.now(),
    "Detected": detected if detected is not None else 0,
    "Undetected": undetected if undetected is not None else 0
}])
st.session_state.trend_data = pd.concat([st.session_state.trend_data, new_row], ignore_index=True)

trend_fig = go.Figure()
trend_fig.add_trace(go.Scatter(x=st.session_state.trend_data["Time"],
                               y=st.session_state.trend_data["Detected"],
                               mode='lines+markers', name='Detected', line=dict(color='green')))
trend_fig.add_trace(go.Scatter(x=st.session_state.trend_data["Time"],
                               y=st.session_state.trend_data["Undetected"],
                               mode='lines+markers', name='Undetected', line=dict(color='red')))
trend_fig.update_layout(title="IDS Detection Trend", xaxis_title="Time", yaxis_title="Number of Attacks")
trend_chart_ph.plotly_chart(trend_fig, use_container_width=True)

# ------------------- GAN Feature Distribution -------------------
st.subheader("🧬 GAN Feature Distribution (Sample)")
fig2, ax2 = plt.subplots()
ax2.hist(gan_data.values.flatten(), bins=50)
ax2.set_title("GAN Generated Feature Distribution")
st.pyplot(fig2)

# ------------------- Live Suricata Alerts -------------------
st.subheader("🚨 Live Suricata Alerts")
alerts_df = get_last_suricata_alerts(suricata_log, last_lines=20)
if not alerts_df.empty:
    severity_colors = {"High":"#ff4c4c", "Medium":"#ffa500", "Low":"#00ccff"}
    def color_row(row):
        return [f'background-color: {severity_colors.get(row.Severity,"white")}' for _ in row]
    alerts_ph.dataframe(alerts_df.style.apply(color_row, axis=1))
else:
    alerts_ph.info("No new Suricata alerts yet")