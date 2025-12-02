# PySTOL: Nonlinear 6-DOF Flight Dynamics Simulation of a Distributed Propulsion STOL Aircraft

![Python](https://img.shields.io/badge/Code-Python_3.11-blue?logo=python&logoColor=white)
![CFD](https://img.shields.io/badge/Validation-FlightGear-blue?logo=flightgear&logoColor=white)
![CAD](https://img.shields.io/badge/Design-Numpy-blue)
![CAD](https://img.shields.io/badge/Design-Scipy-blue)
![Status](https://img.shields.io/badge/Status-Complete-success)

## Abstract
[cite_start]This project involves the design, development, and validation of a nonlinear 6-Degrees-of-Freedom (6-DOF) flight dynamics simulator tailored for a Short Take-off and Landing (STOL) aircraft[cite: 4]. [cite_start]The simulation models rigid body dynamics, inertial coupling, and the specific aerodynamic effects of distributed propulsion ("blown wing")[cite: 5]. [cite_start]The system was implemented in Python using NumPy and SciPy, validated through post-flight parameter estimation, and visualized via a Software-in-the-Loop (SIL) interface with FlightGear[cite: 6].

## Objectives
[cite_start]The main objectives of this project are[cite: 10]:
1.  [cite_start]**Model** the nonlinear equations of motion for a rigid body aircraft[cite: 11].
2.  [cite_start]**Simulate** the "Blown Wing" effect where propeller wash augments lift[cite: 12].
3.  [cite_start]**Validate** the physics using System Identification techniques[cite: 13].
4.  [cite_start]**Visualize** the trajectory using UDP streaming to FlightGear[cite: 14].

## Theoretical Framework

### Coordinate Systems
* [cite_start]**Inertial Frame ($F_E$):** Fixed to the Earth (North-East-Down), used for navigation ($X_e, y_e, Z_e$)[cite: 17].
* [cite_start]**Body Frame ($F_B$):** Fixed to the aircraft Center of Gravity (CG), used for forces and moments ($u, v, w$)[cite: 18].

### Aerodynamic Model: The "Blown Wing"
[cite_start]To model distributed propulsion, the Lift Coefficient ($C_L$) is a function of both Angle of Attack ($\alpha$) and Throttle ($\delta_t$)[cite: 32].

$$C_L(\alpha, \delta_t) = C_{L_{basic}}(\alpha) + C_{L_{blown}}(\delta_t, \alpha)$$

[cite_start]Where the blown effect is approximated as[cite: 36]:
$$C_{L_{blown}} = k_{blown} \cdot \delta_t \cdot \sin(\alpha + \epsilon)$$

## Technology Stack
* [cite_start]**Language:** Python 3.9 [cite: 40]
* [cite_start]**Physics Engine:** NumPy (Vectorized matrix operations) [cite: 41]
* [cite_start]**Solver:** SciPy `solve_ivp` (Runge-Kutta 4/5 method) [cite: 42]
* [cite_start]**Visualization:** Matplotlib (Static analysis) and FlightGear (Real-time SIL) [cite: 43]

## 📂 Architecture
[cite_start]The project is structured into three distinct modules[cite: 45]:
* [cite_start]`aircraft.py` **(The Plant):** Contains mass properties, inertia tensors, and aerodynamic lookup tables[cite: 46].
* [cite_start]`main.py` **(The Solver):** Integrates the differential equations over time steps ($dt$)[cite: 47].
* [cite_start]`sil_interface.py` **(The Interface):** A UDP socket bridge that streams state vectors to external visualization tools[cite: 48].
* [cite_start]`validate.py`: Validation script for post-flight parameter estimation[cite: 142].

## 📊 Results

### Phase 1: 1-DOF Verification
Validated the integration scheme and drag modeling logic by simulating a falling mass. [cite_start]The velocity approached an asymptote where Drag = Weight[cite: 52, 53].

![1-DOF Verification](Pictures/Figure_1%201-DOF%20flight%20physics%20Terminal%20Velocity.png)
[cite_start]*Figure 1: 1-DOF Flight Physics Falling Rock Simulation [cite: 54]*

### Phase 2: 6-DOF Nonlinear Maneuvers
Tested energy conservation and coupling using a "Loop-the-Loop" control input. [cite_start]The simulation produced stable, repeating loops where potential and kinetic energy exchanged correctly[cite: 74, 75, 76].

![6-DOF Nonlinear Maneuvers](Pictures/NonLinear%20Coupling%20Results.png)
[cite_start]*Figure 2: Nonlinear Coupling Results [cite: 77]*

### Phase 3: System Identification
[cite_start]Used a "Digital Twin" approach to reconstruct Angle of Attack history from velocity vector components ($u, w$), verifying that simulated forces were consistent with the aerodynamic database[cite: 143, 145].

![System ID](Pictures/Angle%20of%20Taack%20history.png)
[cite_start]*Figure 3: Angle of Attack History [cite: 146]*

### Phase 4: SIL Visualisation
SIL Implementation, visualizing the behaviour of the flight path to study and verify other characteristics like flight path, properties using Cessna 172P on FlightGear. Download and watch the video.

![SIL Visualisation](Pictures/Nonlinear%206-DOF%20Flight%20Dynamics%20Simulator_Cessna%20172P.mp4)

## Future Work
* [cite_start]**HIL Implementation:** Deploying the Python code to an embedded Raspberry Pi to drive servos[cite: 178].
* [cite_start]**Control Laws:** Implementing a PID Stability Augmentation System (SAS) for the pitch axis[cite: 179].
