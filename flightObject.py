import matplotlib.pyplot as plt
import numpy as np
class flightObject:
    def __init__(self):
        self.x = [];
        self.y = [];
        self.z = [];
        self.roll = [];
        self.pitch = [];
        self.yaw = [];
        self.frame = [];
        self.time = [];
    def addVals(self, X,Y,Z,roll,pitch,yaw, frame, time):
        self.x.append(X)
        self.y.append(Y)
        self.z.append(Z)
        self.roll.append(roll)
        self.pitch.append(pitch)
        self.yaw.append(yaw)
        self.frame.append(frame)
        self.time.append(time)
    def graphVals(self):
        fig, axs = plt.subplots(2,3)
        axs[0,0].plot(tVals,xVals)
        axs[0,0].set_title('X')
        axs[0,0].set_ylabel('displacement (mm)')
        axs[0,1].plot(tVals,yVals)
        axs[0,1].set_title('Y')
        axs[0,1].set_ylabel('displacement (mm)')
        axs[0,2].plot(tVals,zVals)
        axs[0,2].set_title('Z')
        axs[0,2].set_ylabel('displacement (mm)')
        axs[1,0].plot(tVals,rollVals)
        axs[1,0].set_title('Roll')
        axs[1,0].set_ylabel('displacement (rad)')
        axs[1,1].plot(tVals,pitchVals)
        axs[1,1].set_title('Pitch')
        axs[1,1].set_ylabel('displacement (rad)')
        axs[1,2].plot(tVals,yawVals)
        axs[1,2].set_title('Yaw')
        axs[1,2].set_ylabel('displacement (rad)')
        for ax in axs:
            ax.set_xlabel('Time')
