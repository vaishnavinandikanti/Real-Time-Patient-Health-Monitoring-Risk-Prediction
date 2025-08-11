import csv
import time
import random
import datetime
import os

# Make sure data folder exists
os.makedirs("data", exist_ok=True)

# Path to the live stream CSV
csv_file = "data/live_stream.csv"

# Create CSV with header if it doesn't exist
if not os.path.exists(csv_file):
    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["patient_id", "timestamp", "hr", "bp_sys", "spo2"])

# Example patient IDs
patients = list(range(101, 111))  # 101 to 110


# Start simulation
print("Starting real-time patient vitals simulation...")
while True:
    pid = random.choice(patients)
    ts = datetime.datetime.utcnow().isoformat()
    
    # Random vitals within realistic ranges
    hr = random.randint(60, 110)       # Heart rate
    bp_sys = random.randint(100, 160)  # Systolic BP
    spo2 = random.randint(85, 99)      # Oxygen saturation
    
    # Append to CSV
    with open(csv_file, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([pid, ts, hr, bp_sys, spo2])
    
    print(f"[{ts}] Patient {pid} → HR: {hr}, BP_SYS: {bp_sys}, SpO2: {spo2}")
    time.sleep(5)  # New reading every 5 seconds
