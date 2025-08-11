import streamlit as st
import pandas as pd
import joblib
import time
import os

# Define the model path relative to project root
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'risk_model.joblib')

try:
    model = joblib.load(MODEL_PATH)
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ Failed to load model: {e}")
    model = None

# Load trained model
model = joblib.load("../models/risk_model.joblib")

st.set_page_config(page_title="Patient Risk Monitor", layout="wide")
st.title("🏥 Real-Time Patient Risk Monitoring")

DATA_PATH = "data/live_stream.csv"

# Live update loop
placeholder = st.empty()

while True:
    if os.path.exists(DATA_PATH):
        # Load latest vitals
        df = pd.read_csv(DATA_PATH)

        if not df.empty:
            # Keep only latest reading per patient
            latest = df.groupby("patient_id").tail(1)


            # Prepare features for prediction
            features = latest[["hr", "bp_sys", "spo2"]]
            risk_probs = model.predict_proba(features)[:, 1]
            latest["risk_score"] = risk_probs
            latest["risk_level"] = (latest["risk_score"] > 0.5).astype(int)

            # Display in dashboard
            with placeholder.container():
                col1, col2 = st.columns([2, 1])

                with col1:
                    st.subheader("📊 Live Patient Data")
                    st.dataframe(latest[["patient_id", "hr", "bp_sys", "spo2", "risk_score", "risk_level"]])

                with col2:
                    st.subheader("🚨 Alerts")
                    high_risk = latest[latest["risk_level"] == 1]
                    if high_risk.empty:
                        st.success("✅ No high-risk patients right now")
                    else:
                        for _, row in high_risk.iterrows():
                            st.error(f"⚠️ Patient {row['patient_id']} is HIGH RISK (score: {row['risk_score']:.2f})")
    else:
        st.warning("Waiting for live data...")

    time.sleep(5)  # refresh every 5 seconds
