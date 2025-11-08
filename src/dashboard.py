import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os


# Load the trained model safely

model_path = os.path.join("models", "risk_model.joblib")

if not os.path.exists(model_path):
    st.error("❌ Model file not found. Please ensure 'risk_model.joblib' is in the 'models' folder.")
    st.stop()

model = joblib.load(model_path)


# App Title and Description

st.title("🩺 Real-Time Patient Health Risk Prediction")
st.markdown("""
This application allows healthcare professionals to **manually input patient vitals**  
and instantly predict whether the patient is at **High Risk** or **Normal** using a trained ML model.
""")

# Manual Input Section

st.markdown("### 📋 Enter Patient Vitals")

col1, col2, col3 = st.columns(3)

with col1:
    hr = st.number_input("Heart Rate (HR)", min_value=40, max_value=180, value=72, step=1)

with col2:
    bp_sys = st.number_input("Systolic Blood Pressure (BP_SYS)", min_value=80, max_value=200, value=120, step=1)

with col3:
    spo2 = st.number_input("Oxygen Saturation (SpO₂)", min_value=70, max_value=100, value=96, step=1)


# Prediction Section

if st.button("🔍 Predict Risk"):
    input_data = pd.DataFrame([[hr, bp_sys, spo2]], columns=["hr", "bp_sys", "spo2"])
    pred_prob = model.predict_proba(input_data)[0][1]
    prediction = "🚨 High Risk" if pred_prob > 0.7 else "✅ Normal"

    # --- Display Result ---
    st.subheader("Prediction Result:")
    if prediction == "🚨 High Risk":
        st.error(f"🚨 Patient Status: **HIGH RISK**\n\nProbability: **{pred_prob:.2f}**")
    else:
        st.success(f"✅ Patient Status: **NORMAL**\n\nProbability: **{pred_prob:.2f}**")

# Footer

st.markdown("---")
st.info("💡 Tip: You can also keep the simulator running in parallel for real-time updates.")
