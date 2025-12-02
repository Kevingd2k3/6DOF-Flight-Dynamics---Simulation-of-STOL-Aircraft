import numpy as np

class STOL_Aircraft:
    def __init__(self):
        # MASS & GEOMETRY
        self.mass = 1200.0          # kg (Light aircraft)
        self.wing_area = 15.0       # m^2
        self.span = 10.0            # m
        self.chord = 1.5            # m
        
        # Inertia Tensor (J) - How hard it is to rotate
        # (Simplified diagonal matrix for a symmetric aircraft)
        self.Ix = 1000.0            # Roll inertia
        self.Iy = 2500.0            # Pitch inertia
        self.Iz = 3000.0            # Yaw inertia
        self.Ixz = 100.0            # Coupling term (important for nonlinear dynamics!)

        # AERODYNAMIC PARAMETERS 
        # The "Gradient": How much Lift increases per degree of Angle of Attack
        self.CL_alpha = 2.0 * np.pi # Theoretical max for thin airfoils
        self.CD_0 = 0.05            # Drag at zero lift
        
        # This factor represents how much the propeller wash increases lift
        self.blown_lift_factor = 2.5 

    def calculate_forces_and_moments(self, state, controls, rho=1.225):
        """
        Calculates the Forces (Fx, Fy, Fz) and Moments (L, M, N) 
        acting on the aircraft based on current state and inputs.
        """
        # 1. Unpack State
        # Velocity in body frame (u=forward, v=side, w=down)
        u, v, w = state[3], state[4], state[5]
        
        # 2. Calculate Airspeed & Angles
        V_total = np.sqrt(u**2 + v**2 + w**2)
        if V_total < 0.1: V_total = 0.1 # Avoid divide by zero
        
        # Angle of Attack (alpha) = atan(w/u)
        alpha = np.arctan2(w, u)
        
        # Dynamic Pressure (q) = 0.5 * rho * V^2
        q_bar = 0.5 * rho * V_total**2
        
        # 3. UNPACK CONTROLS
        # throttle (0 to 1), elevator (radians)
        throttle = controls[0]
        elevator = controls[1]

        # PHYSICS ENGINE CORE
        
        # LIFT CALCULATION (Nonlinear Blown Wing)
        # Lift = q * S * (CL_basic + CL_blown)
        # We add "throttle * blown_lift_factor" to simulate the prop blowing air over wings
        cl_basic = self.CL_alpha * alpha
        cl_blown = self.blown_lift_factor * throttle * np.sin(alpha + 0.2) # High lift at high throttle
        
        CL_total = cl_basic + cl_blown
        
        Lift = q_bar * self.wing_area * CL_total
        
        # DRAG CALCULATION
        # Drag increases with Lift squared (Induced Drag)
        CD_total = self.CD_0 + 0.04 * (CL_total**2)
        Drag = q_bar * self.wing_area * CD_total
        
        # PITCHING MOMENT (Stability)
        # Simple linear model: M = q * S * c * Cm
        Cm = -0.5 * alpha - 1.2 * elevator # Stable aircraft tries to nose down if alpha is high
        Pitch_Moment = q_bar * self.wing_area * self.chord * Cm
        
        # THRUST
        max_thrust = 5000.0 # Newtons
        Thrust = throttle * max_thrust

        # 4. CONVERT TO BODY FORCES (Aerodynamic Frame -> Body Frame)
        # Lift acts perpendicular to wind, Drag acts parallel to wind
        # We need components aligned with the fuselage (X and Z axes)
        
        Fx_aero = -Drag * np.cos(alpha) + Lift * np.sin(alpha)
        Fz_aero = -Drag * np.sin(alpha) - Lift * np.cos(alpha)
        
        # Total Forces
        Fx = Fx_aero + Thrust
        Fy = 0.0 # Ignoring side force for this step
        Fz = Fz_aero # Note: Gravity is added in the main loop, not here
        
        # Total Moments
        L = 0.0 # Roll
        M = Pitch_Moment
        N = 0.0 # Yaw
        
        return np.array([Fx, Fy, Fz, L, M, N]) 