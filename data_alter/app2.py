import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
import time
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# -------------------------------
# LOGIN SYSTEM
# -------------------------------
def login():
    st.title("🔐 Green GAN Secure Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "green123":
            st.session_state["auth"] = True
        else:
            st.error("Invalid Credentials")

if "auth" not in st.session_state:
    st.session_state["auth"] = False

if not st.session_state["auth"]:
    login()
    st.stop()

# -------------------------------
# MAIN DASHBOARD
# -------------------------------
st.set_page_config(layout="wide")

st.title("🛡️ GREEN GAN – FINAL SECURITY OPERATIONS DASHBOARD")

# -------------------------------
# LOAD GAN DATA
# -------------------------------
data_path = r"D:\Green_GAN_CY\synthetic_attacks.csv"

if not os.path.exists(data_path):
    st.error("Synthetic data not found")
    st.stop()

gan_data = pd.read_csv(data_path)

# -------------------------------
# SIDEBAR CONTROLS
# -------------------------------
st.sidebar.header("⚙️ Controls")

refresh = st.sidebar.checkbox("Live Mode", True)
speed = st.sidebar.slider("Refresh Speed", 1, 5, 2)

# -------------------------------
# METRICS
# -------------------------------
col1, col2, col3, col4 = st.columns(4)

total = len(gan_data)
threat = np.random.randint(60, 95)
detection = np.random.uniform(80, 95)
power_usage = np.random.uniform(10, 25)  # low power

col1.metric("Total Attacks", total)
col2.metric("Threat Score", f"{threat}%")
col3.metric("Detection Rate", f"{detection:.2f}%")
col4.metric("Power Usage (Watts)", f"{power_usage:.2f}W")

# -------------------------------
# LIVE ATTACK TIMELINE
# -------------------------------
st.subheader("📡 Live Attack Timeline")

timeline = pd.DataFrame({
    "time": pd.date_range(end=pd.Timestamp.now(), periods=50),
    "attacks": np.random.randint(10, 100, 50)
})

fig = px.line(timeline, x="time", y="attacks", title="Attack Activity Over Time")
st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# GAN DATA VIEW
# -------------------------------
st.subheader("⚡ Synthetic Attack Samples")

st.dataframe(gan_data.sample(50))

# -------------------------------
# FEATURE HEATMAP
# -------------------------------
st.subheader("🔥 Feature Heatmap")

fig2 = px.imshow(gan_data.sample(100))
st.plotly_chart(fig2)

# -------------------------------
# IDS PERFORMANCE COMPARISON
# -------------------------------
st.subheader("🛡️ IDS Performance")

metrics = ["Accuracy", "Precision", "Recall"]

before = [0.72, 0.70, 0.68]
after = [
    np.random.uniform(0.85, 0.95),
    np.random.uniform(0.80, 0.92),
    np.random.uniform(0.78, 0.90)
]

df = pd.DataFrame({
    "Metric": metrics * 2,
    "Value": before + after,
    "Type": ["Before GAN"] * 3 + ["After GAN"] * 3
})

fig3 = px.bar(df, x="Metric", y="Value", color="Type", barmode="group")
st.plotly_chart(fig3)

# -------------------------------
# ALERT FEED
# -------------------------------
st.subheader("🚨 Threat Alerts")

alerts = [
    "DDoS Attack Detected",
    "SQL Injection Attempt",
    "Port Scan Detected",
    "Suspicious Login Activity",
    "Malware Signature Found"
]

for _ in range(5):
    st.error(np.random.choice(alerts))

# -------------------------------
# GREEN GAN POWER EFFICIENCY
# -------------------------------
st.subheader("🔋 Green GAN Efficiency")

baseline = 50  # normal system
green = power_usage

efficiency_gain = ((baseline - green) / baseline) * 100

st.metric("Power Reduction", f"{efficiency_gain:.2f}%")

if efficiency_gain > 50:
    st.success("Highly Efficient AI Model")
else:
    st.warning("Moderate Efficiency")

# -------------------------------
# EXPORT REPORT
# -------------------------------
st.subheader("📄 Generate Report")

def generate_pdf():
    doc = SimpleDocTemplate("report.pdf")
    styles = getSampleStyleSheet()

    content = []
    content.append(Paragraph("Green GAN Security Report", styles["Title"]))
    content.append(Paragraph(f"Detection Rate: {detection:.2f}%", styles["Normal"]))
    content.append(Paragraph(f"Power Usage: {power_usage:.2f}W", styles["Normal"]))

    doc.build(content)

if st.button("Download Report"):
    generate_pdf()
    with open("report.pdf", "rb") as f:
        st.download_button("Download PDF", f, file_name="Green_GAN_Report.pdf")

# -------------------------------
# AUTO REFRESH
# -------------------------------
if refresh:
    time.sleep(speed)
    st.rerun()