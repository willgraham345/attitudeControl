# This is a sample Python script.
from __future__ import print_function
from vicon_dssdk import ViconDataStream
from initialize import initializeParameters
from customViconFNs import connectToVicon, viconLoop
import time

if __name__ == '__main__':
    thruster1, thruster1_grapher, t_duration, orientation_des = initializeParameters()
    # Create instance of python objects, and custom flight object stuff
    client = ViconDataStream.RetimingClient() # initializing vicon connection
    try:
        connectToVicon(client)
        print("Program begin")
        t_begin = thruster1.setTimeBegin()
        while (time.time() < t_begin + t_duration):
            frame = client.WaitForFrame()
            # iterate over subjects and segments and obtain the joint positions and rotations as above.
            # Create flight control objects, and begin testing time
            XYZ, orientation, success = viconLoop(client)
            if (success == False):
                pass# do nothign
            else:
                ''' Update Pose/attitude stuff'''
                thruster1.getCurrentPose(orientation)
                thruster1.findAndWriteDesiredTorques(orientation_des)
                thruster1.updateVals()
                thruster1_grapher.addPoseVals(XYZ, orientation, thruster1.omega, frame, thruster1.t)
                thruster1_grapher.addThrusterVals(thruster1.Thrust)
                # thruster1_grapher.addPoseVals()
                # thruster1.attitudeControl(orientation, desOrientation, timeStep, gainVals)
                # print('Added')
        # t_last = time.time()
        thruster1_grapher.showGraphs()
    except ViconDataStream.DataStreamException as e:
        print('Handled data stream error (Global)... ERROR:', e)
