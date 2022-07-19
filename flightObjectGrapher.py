import matplotlib.pyplot as plt
import numpy as np

"""
IMPROVEMENT IDEAS
We could try and make the x, y, z translation start at 0 and be relative to its initial position. That wouldn't be too much work and may be helpful later.
"""
class flightObjectGrapher:

    def __init__(self):
        self.x = []
        self.y = []
        self.z = []
        self.roll = []
        self.pitch = []
        self.yaw = []
        self.omega_roll = []
        self.omega_pitch = []
        self.omega_yaw = []
        self.qx = []
        self.qy = []
        self.qz = []
        self.qw = []
        self.frame = []
        self.t = []
        self.sampleTime = []
        self.T1 = []
        self.T2 = []
        self.T3 = []
        self.T4 = []
    def addThrusterVals(self, ThrustVals):
        [T1, T2, T3, T4] = ThrustVals
        self.T1.append(T1)
        self.T2.append(T2)
        self.T3.append(T3)
        self.T4.append(T4)
    def addPoseVals(self, XYZ, orientation, omega, frame, t_current):
        X, Y, Z = XYZ
        roll, pitch, yaw = orientation
        omega_roll, omega_pitch, omega_yaw = omega
        self.x.append(X)
        self.y.append(Y)
        self.z.append(Z)
        self.frame.append(frame)
        self.t.append(t_current)
        self.roll.append(roll)
        self.pitch.append(pitch)
        self.yaw.append(yaw)
        self.omega_roll.append(omega_roll)
        self.omega_pitch.append(omega_pitch)
        self.omega_yaw.append(omega_yaw)

    def showGraphs(self):
        fig, axs = plt.subplots(2,3)
        axs[0,0].plot(self.t,self.x)
        axs[0,0].set_title('X')
        axs[0,0].set_xlabel('time')
        axs[0,0].set_ylabel('displacement (mm)')

        axs[0,1].plot(self.t,self.y)
        axs[0,1].set_title('Y')
        axs[0,1].set_xlabel('time')
        axs[0,1].set_ylabel('displacement (mm)')

        axs[0,2].plot(self.t,self.z)
        axs[0,2].set_title('Z')
        axs[0,2].set_xlabel('time')
        axs[0,2].set_ylabel('displacement (mm)')
        axs[1, 0].plot(self.t, self.roll)
        axs[1, 0].set_title('Roll')
        axs[1, 0].set_xlabel('time')
        axs[1, 0].set_ylabel('displacement (rad)')

        axs[1, 1].plot(self.t, self.pitch)
        axs[1, 1].set_title('Pitch')
        axs[1, 1].set_xlabel('time')
        axs[1, 1].set_ylabel('displacement (rad)')

        axs[1, 2].plot(self.t, self.yaw)
        axs[1, 2].set_title('Yaw')
        axs[1, 1].set_xlabel('time')
        axs[1, 2].set_ylabel('displacement (rad)')

        fig1, axs1 = plt.subplots(2, 2)
        axs1[0, 0].plot(self.t, self.T1)
        axs1[0, 0].set_title('Thruster 1 Vals')
        axs1[0, 0].set_xlabel('Time')
        axs1[0, 0].set_ylabel('Force?')

        axs1[0, 1].plot(self.t, self.T2)
        axs1[0, 1].set_title('Thruster 2 Vals')
        axs1[0, 1].set_xlabel('Time')
        axs1[0, 1].set_ylabel('Force?')

        axs1[1, 0].plot(self.t, self.T3)
        axs1[1, 0].set_title('Thruster 3 Vals')
        axs1[1, 0].set_xlabel('Time')
        axs1[1, 0].set_ylabel('Force?')

        axs1[1, 1].plot(self.t, self.T4)
        axs1[1, 1].set_title('Thruster 4 Vals')
        axs1[1, 1].set_xlabel('Time')
        axs1[1, 1].set_ylabel('Force?')

        fig2 = plt.figure()
        ax2 = fig2.gca(projection = '3d')
        ax2.set_title('XYZ 3d Projection')
        ax2.set_xlabel('x [mm]')
        ax2.set_ylabel('y [mm]')
        ax2.set_zlabel('z [mm]')
        ax2.plot(self.x, self.y, self.z)
        print('length of t', len(self.t))
        for i in range(0, len(self.t) - 2):
            self.sampleTime.append(np.subtract(self.t[i + 1], self.t[i]))
        fig4, ax4 = plt.subplots()
        ax4.plot(range(0, len(self.t)-2), self.sampleTime)
        ax4.set_title('Sampling Rate vs Time')
        ax4.set_xlabel('Time')
        ax4.set_ylabel('Sampling Rate')
        plt.show()