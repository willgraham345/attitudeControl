
import numpy as np
from flightObjectGrapher import flightObjectGrapher
from flightControlObject import flightControlObject


# Load constants
g = 9.81 # [m/s**2]
N = 4 # number of rotors

# Inertia Tensor Matrix for Ionocraft
g = 9.8      # [m/s**2], acceleration of gravity
m = 60e-6      # [kg], body mass  Changed from 10e-6 9/5/2017    5-e-6 is with IMU + flexboard
r = 1e-3 #[m]


roll_AttitudeGains = [0.5, .005, 0]  # Kp, Kd, Ki
pitch_AttitudeGains = [0.5, .005, 0]  # Kp, Kd, Ki Good starting point
yaw_AttitudeGains = [0, 0, 0]  # Kp, Kd, Ki NO YAW CONTROL IN THIS LOOP
attitudeGains = np.vstack((roll_AttitudeGains, pitch_AttitudeGains, yaw_AttitudeGains))

t_duration = 6
orientation_des = np.array([0, 0, 0])

def initializeFlightObjects():

    roll_AttitudeGains = [0.5, .005, 0]  # Kp, Kd, Ki
    pitch_AttitudeGains = [0.5, .005, 0]  # Kp, Kd, Ki Good starting point
    yaw_AttitudeGains = [0, 0, 0]  # Kp, Kd, Ki NO YAW CONTROL IN THIS LOOP
    attitudeGains = np.vstack((roll_AttitudeGains, pitch_AttitudeGains, yaw_AttitudeGains))

    t_duration = 6
    orientation_des = np.array([0, 0, 0])
    ## Initialize flight control objects
    cf1 = flightControlObject(m, r, attitudeGains)
    cf1_grapher = flightObjectGrapher()
    return cf1, cf1_grapher, t_duration, orientation_des