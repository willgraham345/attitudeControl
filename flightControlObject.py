import matplotlib.pyplot as plt
import numpy as np
import time

"""
IMPROVEMENT IDEAS
We could try and make the x, y, z translation start at 0 and be relative to its initial position. That wouldn't be too much work and may be helpful later.
"""
class flightControlObject:
    def __init__(self, m, r, attitudeGains):
        """Notes about initialization
        m = mass of object (kg)
        r = distance from center of mass to motors (m)
        attitudeGains = 3x3 matrix of gain values for attitude controller
            (row 1 = roll, row2, = pitch, row3 = yaw)
        """
        self.m = m
        self.M1 = 0.0
        self.M2 = 0.0
        self.M3 = 0.0
        self.M4 = 0.0
        self.A_matrix = np.array([[1, 1, 1, 1], [0, -r, 0, r], [-r, 0, r, 0],
                      [0, 0, 0, 0]])
        # Calculate the inverse of the matrix (singular systems will be handled with np.linalg.pinv (pseudo-inverse calculation using Singular-Value Decomposition
        self.PWM_VoltageToForceArray = [] # Waiting on values from Rebecca
        self.roll_AttitudeGains = attitudeGains[0] # Kp, Kd, Ki
        self.pitch_AttitudeGains = attitudeGains[1] # Kp, Kd, Ki
        self.yaw_AttitudeGains = attitudeGains[2] # Kp, Kd, Ki NO YAW CONTROL IN THIS LOOP
        self.orientation = np.array([.001, .001, .001]) # [rad]
        self.orientation_old = np.array([.001, .001, .001]) # [rad]
        self.omega = np.array([0, 0, 0]) # Angular speed for roll/pitch/yaw [rad/s]
        self.timeVal = time.time() #[s]
        self.timeVal_last = time.time() #[s]

        # Create A Matrix for Attitude control
        try: # Accounts for normal inverses, will throw an exception if nonsingular A Matrix
            self.A_matrix_in = np.linalg.inv(self.A_matrix)
            # print("A is a nonsingular matrix")
        except:
            self.A_matrix_inv = np.linalg.pinv(self.A_matrix) #Note, this will calulcate the pseudo inverse if system is underactuated (singular)
            # https://numpy.org/doc/stable/reference/generated/numpy.linalg.pinv.html
            # print("A is a singular matrix")


        # print("A matrix: ", self.A_matrix)
        # print("A Matrix inv: ", self.A_matrix_inv)
        # print("A Matrix units are [N]")

    def getCurrentPose(self, orientation, timeVal):
        self.timeVal = timeVal  #updates time
        timeStep = timeVal - self.timeVal_last # Calculates difference in time between last step and this step
        self.orientation = orientation
        print(type(self.orientation), type(self.orientation_old))
        for i in range(2):
            self.omega = (self.orientation - self.orientation_old) / timeStep #[rad/s]
        self.orientation_old = self.orientation
        print("omegas:", self.omega)
    def findDesiredTorques(self, orientation_des):
        """Use this after using getCurrentPose (otherwise orientation will not be correctly set)"""
        roll_obs, pitch_obs, yaw_obs = orientation_obs
        roll_des, pitch_des, yaw_des = orientation_des

        Tau_x_des = self.roll_AttitudeGains[0]*(roll_des - roll_obs) + self.roll_AttitudeGains[1]*(self.omega)
        Tau_y_des = Kp*(pitch_des - pitch_obs)
        Tau_z_des = 0
        T_sum_des = self.m*9.81
        torques_desVec = [T_sum_des, Tau_x_des, Tau_y_des, Tau_z_des]
        print('torques_desVec = ', torques_desVec)
    def writeThrustVals(self, desTauVec, currentTauVec):
        # timeStep, gainVals
        # print('desTauVec: ', desTauVec)
        # print('currentTauVec: ', currentTauVec)
        self.Thrust_Vals = np.dot(self.A_matrix_inv, desTauVec)
        print('Thrust_vals = ', self.Thrust_Vals)




if __name__ == '__main__':
    roll_AttitudeGains = [0.5, .0525, 0]  # Kp, Kd, Ki
    pitch_AttitudeGains = [0.5, .0525, 0]  # Kp, Kd, Ki
    yaw_AttitudeGains = [0, 0, 0]  # Kp, Kd, Ki NO YAW CONTROL IN THIS LOOP
    attitudeGains = np.vstack((roll_AttitudeGains, pitch_AttitudeGains, yaw_AttitudeGains))
    obj1 = flightControlObject(.1, .1, attitudeGains)
    obj1.getCurrentPose([.01, .01, .01], time.time())
    obj1.writeThrustVals(np.ones(4), np.zeros(4))
    # obs_Orientation = np.array([10, 30, 0])
    # des_Orientation = np.array([0, 0, 0])
    # timeStep = 1 / 250
    # gainVals = [1, 1, 1]
    # print("obs_Orientation", obs_Orientation)
    # print("des_Orientation", des_Orientation)
    # obj1.findDesiredTorques(obs_Orientation, des_Orientation, timeStep, gainVals)
