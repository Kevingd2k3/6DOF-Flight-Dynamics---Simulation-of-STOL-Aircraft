import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import pandas as pd
from aircraft import STOL_Aircraft

# Initialize the aircraft object
my_plane = STOL_Aircraft()

# THE 6-DOF EQUATIONS OF MOTION
def equations_of_motion(t, state):
    # Unpack State
    x_e, y_e, z_e = state[0:3]
    u, v, w = state[3:6]
    phi, theta, psi = state[6:9]
    p, q, r = state[9:12]

    # CONTROL INPUTS (STABILIZED)
    # Fix for "Fluttering": We use smooth, constant inputs.
    throttle = 1.0   
    # elevator = -0.1  <-- OLD
    elevator = -0.15   # NEW: Pull back harder (Tighter loop)
    controls = [throttle, elevator]

    # Get Forces & Moments
    forces_moments = my_plane.calculate_forces_and_moments(state, controls)
    Fx, Fy, Fz = forces_moments[0:3]
    L, M, N = forces_moments[3:6]

    # Gravity (Body Frame)
    g = 9.81
    m = my_plane.mass
    gx = -g * np.sin(theta)
    gy = g * np.cos(theta) * np.sin(phi)
    gz = g * np.cos(theta) * np.cos(phi)

    # Dynamics (F=ma)
    u_dot = (Fx / m) + (v*r - w*q) + gx
    v_dot = (Fy / m) + (w*p - u*r) + gy
    w_dot = (Fz / m) + (u*q - v*p) + gz

    # Angular Dynamics
    Ix, Iy, Iz = my_plane.Ix, my_plane.Iy, my_plane.Iz
    p_dot = (L - (Iz - Iy) * q * r) / Ix
    q_dot = (M - (Ix - Iz) * p * r) / Iy
    r_dot = (N - (Iy - Ix) * p * q) / Iz

    # Kinematics
    phi_dot = p + (q * np.sin(phi) + r * np.cos(phi)) * np.tan(theta)
    theta_dot = q * np.cos(phi) - r * np.sin(phi)
    psi_dot = (q * np.sin(phi) + r * np.cos(phi)) / np.cos(theta)

    # Navigation
    x_dot = u * np.cos(theta) + w * np.sin(theta)
    y_dot = v
    z_dot = -u * np.sin(theta) + w * np.cos(theta)

    return [x_dot, y_dot, z_dot, u_dot, v_dot, w_dot, phi_dot, theta_dot, psi_dot, p_dot, q_dot, r_dot]

# SIMULATION SETUP 
# Start on GROUND (z=-1000), Moving fast enough to fly (u=60 m/s)
# State: [x, y, z, u, v, w, phi, theta, psi, p, q, r]
# init_state = [0, 0, 0, 40, 0, 0, 0, 0.05, 0, 0, 0, 0] <-- OLD
# NEW: Z = -1000 (1000m Altitude), Speed = 60 m/s (Faster start)
init_state = [0, 0, -1000, 60, 0, 0, 0, 0, 0, 0, 0, 0]
t_span = [0, 60] 

print("Simulating Smooth Climb...")
sol = solve_ivp(equations_of_motion, t_span, init_state, t_eval=np.linspace(0, 60, 1200))

# DATA EXPORT FOR SIL 
print("Saving flight logs...")
data = {
    'Time': sol.t,
    'X_Pos': sol.y[0],      # <--- CRITICAL: Actual distance traveled
    'Altitude': -sol.y[2],  # Invert Z (Down is positive in math, Up is positive in Log)
    'Velocity': sol.y[3],
    'Pitch': sol.y[7],
    'Roll': sol.y[6]
}
df = pd.DataFrame(data)
df.to_csv('flight_log.csv', index=False)
print("Success! Run sil_interface.py now.")


# Plot 1: Altitude
plt.subplot(2, 2, 1)
plt.plot(sol.t, -sol.y[2])
plt.title("Altitude (m)")
plt.grid(True)

# Plot 2: Velocity
plt.subplot(2, 2, 2)
plt.plot(sol.t, sol.y[3])
plt.title("Speed (m/s)")
plt.grid(True)

# Plot 3: Pitch Angle
plt.subplot(2, 2, 3)
plt.plot(sol.t, np.degrees(sol.y[7]))
plt.title("Pitch (deg)")
plt.grid(True)

# Plot 4: Flight Path
plt.subplot(2, 2, 4)
plt.plot(sol.y[0], -sol.y[2])
plt.title("Flight Path (Side View)")
plt.xlabel("Distance")
plt.ylabel("Altitude")
plt.grid(True)

plt.tight_layout()
plt.show()