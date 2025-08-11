import joblib

# Load the trained model
model = joblib.load("models/risk_model.joblib")
print("✅ Model loaded successfully!")

# Optional: test a sample prediction
sample_data = [[72, 130, 95]]  # hr, bp_sys, spo2
prediction = model.predict(sample_data)
print(f"Sample prediction: {prediction[0]}")


