# This is a sample Python script.
from __future__ import print_function
from vicon_dssdk import ViconDataStream
import numpy as np
from flightObjectGrapher import flightObjectGrapher
from flightControlObject import flightControlObject
import time

# Load constants
g = 9.81 # [m/s**2]
N = 4 # number of rotors

# Inertia Tensor Matrix for Ionocraft
g = 9.8      # [m/s**2], acceleration of gravity
m = 60e-6      # [kg], body mass  Changed from 10e-6 9/5/2017    5-e-6 is with IMU + flexboard
r = 1e-3 #[m]


roll_AttitudeGains = [0.5, .005, 0]  # Kp, Kd, Ki
pitch_AttitudeGains = [0.5, .005, 0]  # Kp, Kd, Ki Good starting point
yaw_AttitudeGains = [0, 0, 0]  # Kp, Kd, Ki NO YAW CONTROL IN THIS LOOP
attitudeGains = np.vstack((roll_AttitudeGains, pitch_AttitudeGains, yaw_AttitudeGains))

t_duration = 6
orientation_des = np.array([0, 0, 0])
if __name__ == '__main__':
    # Create instance of python objects, and custom flight object stuff
    client = ViconDataStream.RetimingClient()
    # client.UpdateFrame()
    print('Program begin')
    try:
        client.Connect("localhost:801",250)
        print("Vicon is connected...", client.IsConnected())
        # Check the version
        print('Version #: ', client.GetVersion())
        client.SetAxisMapping(ViconDataStream.Client.AxisMapping.EForward, ViconDataStream.Client.AxisMapping.ELeft,
                              ViconDataStream.Client.AxisMapping.EUp)
        xAxis, yAxis, zAxis = client.GetAxisMapping()
        print('X Axis', xAxis, 'Y Axis', yAxis, 'Z Axis', zAxis)
        cf1 = flightControlObject(m, r, attitudeGains)
        cf1_grapher = flightObjectGrapher()
        time.sleep(1)
        t_begin = cf1.setTimeBegin()
        while (time.time() < t_begin + t_duration):
            frame = client.WaitForFrame()

            # iterate over subjects and segments and obtain the joint positions and rotations as above.
            # Create flight control objects, and begin testing time
            try:
                subjectNames = client.GetSubjectNames()
                for subjectName in subjectNames:
                    segmentNames = client.GetSegmentNames(subjectName)
                    for segmentName in segmentNames:
                        print(segmentName)
                        # print('current time = ', t_current)

                        ''' Get data from VICON'''
                        [(X,Y,Z), occlusion2] = client.GetSegmentGlobalTranslation(subjectName, segmentName)
                        [(roll, pitch, yaw), occlusion1] = client.GetSegmentGlobalRotationEulerXYZ(subjectName,
                                                                                                   segmentName)
                        XYZ = (X, Y, Z)
                        orientation = (roll, pitch, yaw)

                        ''' Update Pose/attitude stuff'''
                        cf1.getCurrentPose(orientation)
                        cf1.findAndWriteDesiredTorques(orientation_des)
                        cf1.updateVals()
                        cf1_grapher.addPoseVals(XYZ, orientation, cf1.omega, frame, cf1.t)
                        cf1_grapher.addThrusterVals(cf1.Thrust)

                        # cf1_grapher.addPoseVals()
                        # cf1.attitudeControl(orientation, desOrientation, timeStep, gainVals)
                        # print('Added')
            except ViconDataStream.DataStreamException as e:
                print('Handled data stream error (Nested)... ERROR:', e)
                # print('cf1 t', cf1.t)
                # print('cf1 omemga_pitch', cf1.omega_pitch)
        # t_last = time.time()
        cf1_grapher.showGraphs()
    except ViconDataStream.DataStreamException as e:
        print('Handled data stream error (Global)... ERROR:', e)
