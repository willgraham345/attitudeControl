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
        self.Thrust = np.zeros(4)
        self.A_matrix = np.array([[1, 1, 1, 1], [0, -r, 0, r], [-r, 0, r, 0],
                      [0, 0, 0, 0]])
        # Calculate the inverse of the matrix (singular systems will be handled with np.linalg.pinv (pseudo-inverse calculation using Singular-Value Decomposition
        self.PWM_VoltageToForceArray = [] # Waiting on values from Rebecca
        self.roll_gains = attitudeGains[0] # [Kp, Kd, Ki]
        self.pitch_gains = attitudeGains[1] # [Kp, Kd, Ki]
        self.yaw_gains = attitudeGains[2] # Kp, Kd, Ki NO YAW CONTROL IN THIS LOOP

        self.orientation = np.zeros(3) # [rad]
        self.orientation_new = np.zeros(3) # [rad]
        self.omega = np.zeros(3) # Angular speed for roll/pitch/yaw [rad/s]
        self.omega_new = np.zeros(3)
        self.t = time.time() #[s]
        self.t_new = time.time() #[s]
        self.frame = []

        self.torquesDes = np.zeros(4)

        # Create A Matrix for Attitude control
        try: # Accounts for normal inverses, will throw an exception if nonsingular A Matrix
            self.A_matrix_inv = np.linalg.inv(self.A_matrix)
            # print("A is a nonsingular matrix")f
        except:
            self.A_matrix_inv = np.linalg.pinv(self.A_matrix) #Note, this will calulcate the pseudo inverse if system is underactuated (singular)
            # https://numpy.org/doc/stable/reference/generated/numpy.linalg.pinv.html
            # print("A is a singular matrix")


        # print("A matrix: ", self.A_matrix)
        # print("A Matrix inv: ", self.A_matrix_inv)
        # print("A Matrix units are [N]")
    def updateFrame(self, frame):
        self.frame = frame
        print('selfFrame = ', self.frame, type(self.frame))
    def setTimeBegin(self):
        self.t = time.time()
        a = time.time()
        return a

    def getCurrentPose(self, orientation):
        """Pass in orientation to update flightControlObject"""
        self.t_new = time.time()  #updates time
        timeStep = self.t_new - self.t # Calculates difference in time between last step and this step
        self.orientation_new = orientation
        # print("omegas:", self.omega, type(self.omega))
        # print("timeStep:", timeStep, type(timeStep))
        # print('orientation:', self.orientation, type(self.orientation))
        # print('orientation_new:', self.orientation_new, type(self.orientation_new))
        self.omega_new = np.subtract(self.orientation_new,self.orientation) / timeStep #[rad/s] #uses np.subtract to handle tuple generation from vicon

    def findAndWriteDesiredTorques(self, orientation_des):
        """Use this after using getCurrentPose (otherwise orientation will not be correctly set)"""
        roll_obs, pitch_obs, yaw_obs = self.orientation
        roll_des, pitch_des, yaw_des = orientation_des
        # print('self.orientation', self.orientation, type(self.orientation))
        # print('rollgains: ', self.roll_gains, type(self.roll_gains))
        # print('rollgains[0]: ', self.roll_gains[0], type(self.roll_gains[0]))
        # print('pitchgains: ', self.pitch_gains, type(self.pitch_gains))
        # print(self.yaw_gains)

        Tau_x_des = self.roll_gains[0]*(roll_des - roll_obs) + self.roll_gains[1]*(self.omega_new[1])
        Tau_y_des = self.pitch_gains[0]*(pitch_des - pitch_obs) + self.pitch_gains[2]*(self.omega_new[2])
        Tau_z_des = 0
        T_sum_des = self.m*9.81 # Hover input
        self.torquesDes = np.array([T_sum_des, Tau_x_des, Tau_y_des, Tau_z_des])
        print('timestep stuff ', self.t, self.t_new, self.t_new - self.t)
        print("torquesDes: ", self.torquesDes, type(self.torquesDes))
        print('A Matrix: ', self.A_matrix, type(self.A_matrix))
        print('A Matrix_inv: ', self.A_matrix_inv, type(self.A_matrix))
        self.Thrust = np.dot(self.A_matrix_inv, self.torquesDes)
        print('Thrust: ', self.Thrust)
    def updateVals(self):
        self.orientation = self.orientation_new
        self.t = self.t_new
        self.omega = self.omega_new

        # print('torques_desVec = ', torques_desVec)




if __name__ == '__main__':
    roll_gains = [0.5, .0525, 0]  # Kp, Kd, Ki
    pitch_gains = [0.5, .0525, 0]  # Kp, Kd, Ki
    yaw_gains = [0, 0, 0]  # Kp, Kd, Ki NO YAW CONTROL IN THIS LOOP
    attitudeGains = np.vstack((roll_gains, pitch_gains, yaw_gains))
    obj1 = flightControlObject(.1, .1, attitudeGains)
    obj1.getCurrentPose([.01, .01, .01])
    obj1.findAndWriteDesiredTorques(np.zeros(3))
    # obj1.writeThrustVals(np.ones(4), np.zeros(4))
    # obs_Orientation = np.array([10, 30, 0])
    # des_Orientation = np.array([0, 0, 0])
    # timeStep = 1 / 250
    # gainVals = [1, 1, 1]
    # print("obs_Orientation", obs_Orientation)
    # print("des_Orientation", des_Orientation)
    # obj1.findDesiredTorques(obs_Orientation, des_Orientation, timeStep, gainVals)
