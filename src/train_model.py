import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, classification_report, confusion_matrix
import os

# Ensure models folder exists
os.makedirs("../models", exist_ok=True)

# 1) Generate synthetic dataset (matching simulator features)
np.random.seed(42)
n_samples = 1000
data = pd.DataFrame({
    "hr": np.random.randint(55, 120, size=n_samples),
    "bp_sys": np.random.randint(95, 180, size=n_samples),
    "spo2": np.random.randint(80, 100, size=n_samples)
})

# Label high risk
data["high_risk"] = (
    (data["hr"] < 60) | (data["hr"] > 100) |
    (data["bp_sys"] > 140) |
    (data["spo2"] < 92)
).astype(int)

# 2) Split
X = data[["hr", "bp_sys", "spo2"]]
y = data["high_risk"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 3) Train
model = GradientBoostingClassifier(
    n_estimators=200,
    learning_rate=0.05,
    max_depth=3,
    random_state=42
)
model.fit(X_train, y_train)

# 4) Evaluate
y_pred_prob = model.predict_proba(X_test)[:, 1]
y_pred = (y_pred_prob > 0.7).astype(int)
roc_auc = roc_auc_score(y_test, y_pred_prob)
print("ROC AUC:", roc_auc)
print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))

# 5) Save model
joblib.dump(model, "../models/risk_model.joblib")
print("✅ Model saved to ../models/risk_model.joblib")

