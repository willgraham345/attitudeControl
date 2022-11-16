import matplotlib.pyplot as plt
import numpy as np
import time
# from arduinoControl import PWMController
import serial
import datetime

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

        # not sure if this is a good idea to implement
        self.error = []
        self.errorDt = []
        self.error_new = []

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
        # print('selfFrame = ', self.frame, type(self.frame))
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
        timeStep = self.t_new - self.t # Calculates difference in time between last step and this step

        self.error_roll_new = roll_des - roll_obs # Proportional error
        self.error_pitch_new = pitch_des - pitch_obs
        self.error_yaw_new = pitch_des - pitch_obs


        self.error_new = orientation_des - self.orientation
        self.errorDt = np.subtract(self.error_new, self.error) / (self.t_new - self.t)



        # Kept in case the above errors don't compile correctly
        # self.errorDt_roll = (error_roll_new - error_roll) / (self.t_new - self.t) # Rate of change of the error (derivative portion)
        # self.errorDt_pitch = (error_pitch_new - error_pitch) / (self.t_new - self.t)
        # self.errorDt_yaw = (error_yaw_new - error_yaw) / (self.t_new - self.t)

        Tau_x_des = self.roll_gains[0]*(self.error_new[0]) + self.roll_gains[1]*(self.errorDt[0])
        Tau_y_des = self.pitch_gains[0]*(self.error_new[1]) + self.pitch_gains[2]*(self.errorDt[0])
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
        self.error = self.error_new

    def initPWM(self):
        self.tied_device = None # I'm REALLY confused with this part of it. No idea what's going on here.
        com = self.tied_device.serial_port
        self.port = serial.Serial(com, 115200, timeout=1)
        self.tied_device.port = self.port
        self.pwm_cntrl = PWMController(self.port)
        # print('torques_desVec = ', torques_desVec)
    def zeroPWM(self):
        self.pwm_cntrl.setPWM(0)
    def fullPWM(self):
        self.pwm_cntrl.setPWM(100)






if __name__ == '__main__':
    roll_gains = [0.5, .0525, 0]  # Kp, Kd, Ki
    pitch_gains = [0.5, .0525, 0]  # Kp, Kd, Ki
    yaw_gains = [0, 0, 0]  # Kp, Kd, Ki NO YAW CONTROL IN THIS LOOP
    attitudeGains = np.vstack((roll_gains, pitch_gains, yaw_gains))
    obj1 = flightControlObject(.1, .1, attitudeGains)
    # obj1.getCurrentPose([.01, .01, .01])
    # obj1.findAndWriteDesiredTorques(np.zeros(3))
    # obj1.writeThrustVals(np.ones(4), np.zeros(4))
    # obs_Orientation = np.array([10, 30, 0])
    # des_Orientation = np.array([0, 0, 0])
    # timeStep = 1 / 250
    # gainVals = [1, 1, 1]
    # print("obs_Orientation", obs_Orientation)
    # print("des_Orientation", des_Orientation)
    # obj1.findDesiredTorques(obs_Orientation, des_Orientation, timeStep, gainVals)
    obj1.initPWM()

