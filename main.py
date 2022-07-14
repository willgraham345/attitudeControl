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


roll_AttitudeGains = [0.5, .0525, 0]  # Kp, Kd, Ki
pitch_AttitudeGains = [0.5, .0525, 0]  # Kp, Kd, Ki
yaw_AttitudeGains = [0, 0, 0]  # Kp, Kd, Ki NO YAW CONTROL IN THIS LOOP
attitudeGains = np.vstack((roll_AttitudeGains, pitch_AttitudeGains, yaw_AttitudeGains))

t_duration = 60
if __name__ == '__main__':
    # Create instance of python objects, and custom flight object stuff
    client = ViconDataStream.RetimingClient()
    try:
        client.Connect("localhost:801")
        print("Vicon is connected...", client.IsConnected())
        # Check the version
        print('Version #: ', client.GetVersion())
        client.SetAxisMapping(ViconDataStream.Client.AxisMapping.EForward, ViconDataStream.Client.AxisMapping.ELeft,
                              ViconDataStream.Client.AxisMapping.EUp)
        xAxis, yAxis, zAxis = client.GetAxisMapping()
        print('X Axis', xAxis, 'Y Axis', yAxis, 'Z Axis', zAxis)

        # Create flight control objects, and begin testing time
        cf2 = flightControlObject(m, r, attitudeGains)
        t_begin = time.time()

        while(time.time() < t_begin + t_duration):
            try:
                frame = client.UpdateFrame()
                # print('frame = ', frame)
                subjectNames = client.GetSubjectNames()
                for subjectName in subjectNames:
                    segmentNames = client.GetSegmentNames(subjectName)
                    for segmentName in segmentNames:
                        # print('current time = ', t_current)

                        ''' Get data from VICON'''
                        if orientationMode == 'euler':
                            [(X,Y,Z), occlusion2] = client.GetSegmentGlobalTranslation(subjectName, segmentName)
                            [(roll, pitch, yaw), occlusion1] = client.GetSegmentGlobalRotationEulerXYZ(subjectName,
                                                                                                       segmentName)
                            XYZ = (X, Y, Z)
                            orientation = (roll, pitch, yaw)
                        elif orientationMode == 'quaternion':
                            [(X,Y,Z), occlusion2] = client.GetSegmentGlobalTranslation(subjectName, segmentName)
                            [(q_x, q_y, q_z, q_w), occlusion3] = client.GetSegmentGlobalRotationQuaternion(subjectName, segmentName)
                            XYZ = (X, Y, Z)
                            orientation = (roll, pitch, yaw)

                        ''' Update Pose/attitude stuff'''
                        t_current = time.time()
                        cf2.getCurrentPose(orientation, time.time()-t_begin)
                        # cf1.attitudeControl(orientation, desOrientation, timeStep, gainVals)
                        print('Added')


            except ViconDataStream.DataStreamException as e:
                print('Handled data stream error (Nested)... ERROR:', e)
                print('cf1 t', cf1.t)
                print('cf1 omemga_pitch', cf1.omega_pitch)
        t_last = time.time()
        cf1.graphPoseVals()



    except ViconDataStream.DataStreamException as e:
        print('Handled data stream error (Global)... ERROR:', e)