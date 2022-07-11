import matplotlib.pyplot as plt
import numpy as np

"""
IMPROVEMENT IDEAS
We could try and make the x, y, z translation start at 0 and be relative to its initial position. That wouldn't be too much work and may be helpful later.
"""
class flightObject:
    def __init__(self, orientationMode):
        self.x = []
        self.y = []
        self.z = []
        self.roll = []
        self.pitch = []
        self.yaw = []
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
        if (type(orientationMode) != str):
            raise('orientationMode must be a string (either quaternion or euler)')
        self.orientationMode = orientationMode
    def addPoseVals(self, XYZ, orientation, frame, t):
        X, Y, Z = XYZ
        self.x.append(X)
        self.y.append(Y)
        self.z.append(Z)
        if (self.orientationMode == 'euler'):
            roll, pitch, yaw = pose
            self.roll.append(roll)
            self.pitch.append(pitch)
            self.yaw.append(yaw)
        elif(self.orientationMode == 'quaternion'):
            qx, qy, qz, qw = pose
            self.qx.append(qx)
            self.qy.append(qy)
            self.qz.append(qz)
            self.qw.append(qw)
        else:
            raise('Errors with orientationMode entry')
        self.frame.append(frame)
        self.t.append(t)


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

        plt.show()
