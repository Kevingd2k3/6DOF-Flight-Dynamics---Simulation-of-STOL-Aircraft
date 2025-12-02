import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# 1. LOAD THE FLIGHT DATA
print("Loading Flight Recorder Data...")
df = pd.read_csv('flight_log.csv')

# 2. DEFINE THE PHYSICS MODEL WE EXPECT
# We know Lift Coefficient Cl = Cl_0 + Cl_alpha * alpha
# We want to ask the computer: "Based on the data, what is Cl_alpha?"
def linear_lift_model(alpha, cl_alpha, cl_0):
    return cl_alpha * alpha + cl_0

# 3. EXTRACT RELEVANT DATA
# In a real test, we measure Lift Force (Fz). 
# Here, we will estimate Lift based on the Normal Acceleration (approximate for this demo)
# Force ~ Mass * Acceleration. 
# For this demo, we will check if the Loop Logic held up:
# We want to see if Alpha (Angle of Attack) correlates with the "G-Force" (Turn rate)

# Let's plot Alpha vs Time to see what the wing was doing during the loops
plt.figure(figsize=(10, 6))
plt.plot(df['Time'], np.degrees(df['Alpha']), label='Angle of Attack (deg)', color='orange')
plt.title("Parameter Estimation: Angle of Attack History")
plt.xlabel("Time (s)")
plt.ylabel("Alpha (degrees)")
plt.grid(True)
plt.legend()

# 4. OUTPUT VALIDATION METRICS
print("-" * 30)
print("FLIGHT TEST VALIDATION REPORT")
print("-" * 30)
max_alpha = np.degrees(df['Alpha'].max())
print(f"Max Angle of Attack: {max_alpha:.2f} deg")

if max_alpha > 15:
    print("STATUS: STALL REGIME ENCOUNTERED")
else:
    print("STATUS: NOMINAL FLIGHT ENVELOPE")
    
print(f"Total Flight Time: {df['Time'].iloc[-1]:.1f} s")
print("-" * 30)

plt.show()