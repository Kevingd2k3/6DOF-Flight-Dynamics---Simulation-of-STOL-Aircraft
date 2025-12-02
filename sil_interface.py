import socket
import time
import pandas as pd
import numpy as np

# CONFIGURATION
FG_IP = "127.0.0.1"
FG_PORT = 5500

print(f"SIL INTERFACE")
print(f"Target IP: {FG_IP}:{FG_PORT}")

# 1. SETUP UDP SOCKET
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 2. LOAD DATA
try:
    df = pd.read_csv('flight_log.csv')
    print(f"Loaded {len(df)} simulation frames.")
except FileNotFoundError:
    print("Error: flight_log.csv not found. Run main.py first!")
    exit()

# 3. AUTO-CALCULATE PLAYBACK SPEED 
# We look at the time difference between the first two rows to find 'dt'
dt_physics = df['Time'].iloc[1] - df['Time'].iloc[0]
print(f"Detected Physics Step: {dt_physics:.4f} seconds")
print(f"Playback Speed: 1.0x Real Time")

# 4. RUNWAY SETUP (KSFO 28R)
start_lat = 37.618817
start_lon = -122.375427
meters_per_deg = 111000.0 

print("Starting Stream in 3 seconds...")
time.sleep(3)

for index, row in df.iterrows():
    # MAPPING 
    dist_north = row['X_Pos']
    
    lat = start_lat + (dist_north / meters_per_deg)
    lon = start_lon 
    
    # Altitude: Add 1000ft buffer to ensure we don't hit ground
    # (Since we start at -1000m in math, this puts us at ~3300ft visual)
    alt_ft = (row['Altitude'] * 3.28084) + 1000 
    
    # Angles
    roll = np.degrees(row['Roll'])
    pitch = np.degrees(row['Pitch'])
    yaw = 280 

    # PACKET 
    msg = f"{lat},{lon},{alt_ft},{roll},{pitch},{yaw}\n"
    sock.sendto(bytes(msg, "utf-8"), (FG_IP, FG_PORT))
    
    # DYNAMIC SLEEP 
    # Sleep exactly as long as the physics engine intended
    time.sleep(dt_physics)

print("Simulation Complete.")