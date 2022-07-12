import matplotlib.pyplot as plt
import numpy as np

"""
IMPROVEMENT IDEAS
We could try and make the x, y, z translation start at 0 and be relative to its initial position. That wouldn't be too much work and may be helpful later.
"""
class flightControlObject:
    def __init__(self, m, r):
        """Notes about initialization
        r = distance from center of mass to motors (m)
        """
        self.M1 = 0.0
        self.M2 = 0.0
        self.M3 = 0.0
        self.M4 = 0.0
        self.A_matrix = np.array([[1, 1, 1, 1], [0, -r, 0, r], [-r, 0, r, 0],
                      [0, 0, 0, 0]])
        # CAlculate the inverse of the matrix (singular systems will be handled with np.linalg.pinv (pseudoinverse calculation using Singular-Value Decomposition
        self.PWM_VoltageToForceArray = [] # Waiting on values from Rebecca



        # Create A Matrix for Attitude control
        try: # Accounts for normal inverses, will throw an exception if nonsingular A Matrix
            self.A_matrix_in = np.linalg.inv(A_matrix)
            print("A is a nonsingular matrix")
        except:
            self.A_matrix_inv = np.linalg.pinv(self.A_matrix) #Note, this will calulcate the pseudo inverse if system is underactuated (singular)
            # https://numpy.org/doc/stable/reference/generated/numpy.linalg.pinv.html
            print("A is a singular matrix")


        print("A matrix: ", self.A_matrix)
        print("A Matrix inv: ", self.A_matrix_inv)
        print("A Matrix units are [N]")

    def findDesiredTorques(self, poseCurrent, obs_Orientation, desOrientation, timeStep, gainVals):
        deltaT = self.t[-1] - self.t[-2]
        # omega = obs_orientation
        [Kp, Kd, Ki] = gainVals
        [roll_obs, pitch_obs, yaw_obs] = obs_Orientation
        [roll_des, pitch_des, yaw_des] = desOrientation
        Tau_x_des = Kp* (roll_des - roll_obs)
        Tau_y_des = Kp*(pitch_des - pitch_obs)
        Tau_z_des = 0
        T_sum_des = m*9.81
    def writeThrustVals(self, desTauVec, currentTauVec):
        # timeStep, gainVals
        # print('desTauVec: ', desTauVec)
        # print('currentTauVec: ', currentTauVec)
        self.Thrust_Vals = np.dot(self.A_matrix_inv, desTauVec)




if __name__ == '__main__':
    obj1 = flightControlObject(.001, .002)
    obj1.writeThrustVals(np.ones(4), np.zeros(4))