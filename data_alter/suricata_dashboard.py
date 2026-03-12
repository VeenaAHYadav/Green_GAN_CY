import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px
import joblib
from datetime import datetime

st.set_page_config(page_title="AI SOC Dashboard", layout="wide")

st.title("🛡️ AI-Powered SOC Security Dashboard")

# ---------------------------------------------------
# FILE PATHS (EDIT IF YOUR PROJECT STRUCTURE DIFFERS)
# ---------------------------------------------------

SURICATA_LOG = "/var/log/suricata/eve.json"
WAZUH_LOG = "/var/ossec/logs/alerts/alerts.json"

DATASET_FILE = "data/training_dataset.csv"
SYNTHETIC_FILE = r"D:\Green_GAN_CY\synthetic_attacks.csv"

MODEL_FILE = r"D:\Green_GAN_CY\ids_model.pkl"
EVAL_FILE = "evaluation/evaluation.json"


# ---------------------------------------------------
# LOAD TRAINING DATASET
# ---------------------------------------------------

@st.cache_data
def load_dataset():
    if os.path.exists(DATASET_FILE):
        return pd.read_csv(DATASET_FILE)
    return pd.DataFrame()

dataset = load_dataset()


# ---------------------------------------------------
# LOAD SYNTHETIC ATTACKS
# ---------------------------------------------------

@st.cache_data
def load_synthetic():
    if os.path.exists(SYNTHETIC_FILE):
        return pd.read_csv(SYNTHETIC_FILE)
    return pd.DataFrame()

synthetic = load_synthetic()


# ---------------------------------------------------
# LOAD MODEL EVALUATION
# ---------------------------------------------------

def load_eval():
    if os.path.exists(EVAL_FILE):
        with open(EVAL_FILE) as f:
            return json.load(f)
    return None

evaluation = load_eval()


# ---------------------------------------------------
# LOAD SURICATA ALERTS
# ---------------------------------------------------

def load_suricata():
    alerts = []

    if not os.path.exists(SURICATA_LOG):
        return pd.DataFrame()

    with open(SURICATA_LOG) as f:
        for line in f:
            try:
                log = json.loads(line)

                if log.get("event_type") == "alert":

                    alerts.append({
                        "timestamp": log.get("timestamp"),
                        "src_ip": log.get("src_ip"),
                        "dst_ip": log.get("dest_ip"),
                        "protocol": log.get("proto"),
                        "attack": log.get("alert", {}).get("signature"),
                        "severity": log.get("alert", {}).get("severity")
                    })

            except:
                continue

    return pd.DataFrame(alerts)


alerts_df = load_suricata()


# ---------------------------------------------------
# LOAD WAZUH ALERTS
# ---------------------------------------------------

def load_wazuh():
    alerts = []

    if not os.path.exists(WAZUH_LOG):
        return pd.DataFrame()

    with open(WAZUH_LOG) as f:
        for line in f:
            try:
                log = json.loads(line)

                alerts.append({
                    "timestamp": log.get("@timestamp"),
                    "rule": log.get("rule", {}).get("description"),
                    "level": log.get("rule", {}).get("level"),
                    "agent": log.get("agent", {}).get("name")
                })

            except:
                continue

    return pd.DataFrame(alerts)


wazuh_df = load_wazuh()


# ---------------------------------------------------
# LOAD TRAINED MODEL
# ---------------------------------------------------

def load_model():
    if os.path.exists(MODEL_FILE):
        return joblib.load(MODEL_FILE)
    return None

model = load_model()


# ===================================================
# SECTION 1 : MODEL PERFORMANCE
# ===================================================

st.header("📊 Model Performance")

if evaluation:

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Accuracy", evaluation.get("accuracy"))
    col2.metric("Precision", evaluation.get("precision"))
    col3.metric("Recall", evaluation.get("recall"))
    col4.metric("F1 Score", evaluation.get("f1_score"))

else:
    st.warning("Evaluation file not found")


# ===================================================
# SECTION 2 : DATASET ANALYSIS
# ===================================================

st.header("📚 Training Dataset Analysis")

if not dataset.empty:

    col1, col2 = st.columns(2)

    # Attack distribution
    attack_counts = dataset["attack_type"].value_counts()

    fig = px.pie(
        values=attack_counts.values,
        names=attack_counts.index,
        title="Attack Type Distribution"
    )

    col1.plotly_chart(fig, use_container_width=True)

    # Protocol distribution
    proto_counts = dataset["protocol"].value_counts()

    fig2 = px.bar(
        x=proto_counts.index,
        y=proto_counts.values,
        labels={"x": "Protocol", "y": "Count"},
        title="Protocol Distribution"
    )

    col2.plotly_chart(fig2, use_container_width=True)

else:
    st.warning("Training dataset not found")


# ===================================================
# SECTION 3 : SYNTHETIC ATTACK COMPARISON
# ===================================================

st.header("🧬 Real vs Synthetic Attacks")

if not dataset.empty and not synthetic.empty:

    dataset["type"] = "Real"
    synthetic["type"] = "Synthetic"

    combined = pd.concat([dataset, synthetic])

    fig = px.histogram(
        combined,
        x="attack_type",
        color="type",
        barmode="group",
        title="Real vs Synthetic Attack Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("Synthetic attack dataset missing")


# ===================================================
# SECTION 4 : SURICATA NETWORK MONITORING
# ===================================================

st.header("🌐 Network IDS Monitoring (Suricata)")

if not alerts_df.empty:

    alerts_df["timestamp"] = pd.to_datetime(alerts_df["timestamp"])

    col1, col2 = st.columns(2)

    # Alerts over time
    timeline = alerts_df.groupby(
        alerts_df["timestamp"].dt.floor("min")
    ).size()

    fig = px.line(
        x=timeline.index,
        y=timeline.values,
        labels={"x": "Time", "y": "Alerts"},
        title="Alerts Over Time"
    )

    col1.plotly_chart(fig, use_container_width=True)

    # Protocol distribution
    proto_counts = alerts_df["protocol"].value_counts()

    fig2 = px.bar(
        x=proto_counts.index,
        y=proto_counts.values,
        title="Protocol Distribution"
    )

    col2.plotly_chart(fig2, use_container_width=True)

    # Top attacker IPs
    st.subheader("🚨 Top Attacker IPs")

    top_ips = alerts_df["src_ip"].value_counts().head(10)

    fig3 = px.bar(
        x=top_ips.index,
        y=top_ips.values,
        labels={"x": "Source IP", "y": "Alerts"}
    )

    st.plotly_chart(fig3, use_container_width=True)

    # Live alerts
    st.subheader("📡 Live Suricata Alerts")

    st.dataframe(
        alerts_df.sort_values("timestamp", ascending=False),
        use_container_width=True
    )

else:
    st.warning("No Suricata alerts detected")


# ===================================================
# SECTION 5 : WAZUH SECURITY EVENTS
# ===================================================

st.header("🧠 Wazuh SIEM Alerts")

if not wazuh_df.empty:

    st.dataframe(
        wazuh_df.tail(50),
        use_container_width=True
    )

else:
    st.warning("No Wazuh alerts detected")


# ===================================================
# SECTION 6 : AI THREAT DETECTION
# ===================================================

st.header("🤖 AI Threat Detection")

if model and not alerts_df.empty:

    try:

        features = alerts_df[["severity"]]

        predictions = model.predict(features)

        alerts_df["prediction"] = predictions

        st.dataframe(
            alerts_df[[
                "src_ip",
                "dst_ip",
                "protocol",
                "attack",
                "prediction"
            ]].head(20)
        )

    except:
        st.warning("Model prediction failed. Feature mismatch.")

else:
    st.warning("Model file missing")


# ===================================================
# SECTION 7 : RAW LOG VIEWER
# ===================================================

st.header("📜 Raw Suricata Log Viewer")

if os.path.exists(SURICATA_LOG):

    with open(SURICATA_LOG) as f:
        lines = f.readlines()[-20:]

    for line in lines:
        st.code(line)

else:
    st.warning("Suricata log file not found")


st.success("Dashboard loaded successfully")