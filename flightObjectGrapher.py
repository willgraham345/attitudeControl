import matplotlib.pyplot as plt
import numpy as np

"""
IMPROVEMENT IDEAS
We could try and make the x, y, z translation start at 0 and be relative to its initial position. That wouldn't be too much work and may be helpful later.
"""
class flightObjectGrapher:
    def __init__(self, orientationMode):
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
        self.M1 = 0.0
        self.M2 = 0.0
        self.M3 = 0.0
        self.M4 = 0.0
        self.desOrientation = []
        if (type(orientationMode) != str):
            raise('orientationMode must be a string (either quaternion or euler)')
        self.orientationMode = orientationMode
        for i in range(0,2):
            self.x.append(0.0)
            self.y.append(0.0)
            self.z.append(0.0)
            self.roll.append(0.0)
            self.pitch.append(0.0)
            self.yaw.append(0.0)
            self.omega_roll.append(0.0)
            self.omega_pitch.append(0.0)
            self.omega_yaw.append(0.0)
            self.t.append(0.0)
            # self.qx.append(0.0) NEEDS SUPPORT FOR QUATERNIONS


    def addPoseVals(self, XYZ, orientation, frame, timeVal):
        X, Y, Z = XYZ
        self.x.append(X)
        self.y.append(Y)
        self.z.append(Z)
        if (self.orientationMode == 'euler'):
            roll, pitch, yaw = orientation
            self.roll.append(roll)
            self.pitch.append(pitch)
            self.yaw.append(yaw)
        elif(self.orientationMode == 'quaternion'):
            qx, qy, qz, qw = orientation
            self.qx.append(qx)
            self.qy.append(qy)
            self.qz.append(qz)
            self.qw.append(qw)
        else:
            raise('Errors with orientationMode entry')
        self.frame.append(frame)
        timeStep = timeVal - self.t[-1]
        self.t.append(timeStep)
        self.omega_pitch.append((self.pitch[-1] - self.pitch[-2]) / timeStep)
        print('pitch Velocity', ((self.pitch[-1] - self.pitch[-2]) / timeStep) )


    def graphPoseVals(self):
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
        if (self.orientationMode == 'euler'):
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
        elif(self.orientationMode == 'quaternion'):
            print("visualization for quaternions not yet supported (or understood) by our good friend Will")
        # for i in range(len(self.t)):
        #     samplingRate[i] = self.t(i) - self.t(i)

        # plt.show()
        fig2, ax2 = plt.subplots()
        ax2.plot(self.t, self.t)
        ax2.set_title('Sampling Rate vs Time')
        ax2.set_xlabel('Time')
        ax2.set_ylabel('Sampling Rate')


        fig3 = plt.figure()
        ax3 = fig3.gca(projection = '3d')
        ax3.set_xlabel('x [mm]')
        ax3.set_ylabel('y [mm]')
        ax3.set_zlabel('z [mm]')
        ax3.plot(self.x, self.y, self.z)
        plt.show()
