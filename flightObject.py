import matplotlib.pyplot as plt
import numpy as np
class flightObject:
    def __init__(self):
        self.xVals = [];
        self.yVals = [];
        self.zVals = [];
        self.roll = [];
        self.pitch = [];
        self.yaw = [];
        self.frame = [];
        self.time = [];
    def addVals(self, X,Y,Z,roll,pitch,yaw, frame, time):
        self.xVals.append(X)
        self.yVals.append(Y)
        self.ZVals.append(Z)
        self.rollVals.append(roll)
        self.pitchVals.append(pitch)
        self.yawVals.append(yaw)
        self.frameVals.append(frame)
        self.tVals.append(time)
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
