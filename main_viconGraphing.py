# This is a sample Python script.
from __future__ import print_function
from vicon_dssdk import ViconDataStream
import numpy as np
from flightObjectGrapher import flightObjectGrapher
import time

# Load constants
g = 9.81 # [m/s**2]
XYZ_initial_condition = np.transpose([0, 0, 0])
N = 4 # number of rotors
# Inertia Tensor Matrix for Ionocraft
g = 9.8      # [m/s**2], acceleration of gravity
m = 60e-6      # [kg], body mass  Changed from 10e-6 9/5/2017    5-e-6 is with IMU + flexboard
lx = 1e-2      # [m], x distance to body center of mass
ly = 1e-2      # [m], y distance to body center of mass
lz = 20e-6     # [m], z distance to body center of mass
rho = 1.01     # [kg/m**3]
I_B_x = (1/12)*m*ly**2          #[kg*m**2], moment of inertia around x axis
I_B_y = (1/12)*m*lx**2          #[kg*m**2], moment of inertia around y axis
I_B_z = (1/12)*m*(lx**2 + ly**2) #[kg*m**2], moment of inertia around z axis
I_B = np.array([[I_B_x, 0, 0],
                [0, I_B_y, 0],
                [0, 0, I_B_z]]) # [kg*m**2], moment of inertia matrix
J = I_B

cT = 0 # Change this later
d = 0 # Change this later
cQ = 0 # Change this later
Gamma = np.array([[cT, cT, cT, cT], [0, d*cT, 0, -d*cT],
[-d*cT, 0, d*cT, 0], [-cQ, cQ, -cQ, cQ]])
theta = 10.0

psi = 20.0
phi = 70.0
del_theta = 0
del_phi = 0

C_psi = np.cos(psi)
S_psi = np.sin(psi)
C_phi = np.cos(phi)
S_phi = np.sin(phi)
C_theta = np.cos(theta)
S_theta = np.sin(theta)

R_AtoB = np.array([[np.cos(psi), -np.sin(psi), del_theta*np.cos(psi)+del_phi*np.sin(psi)],
                  [np.sin(psi), np.cos(psi), del_theta*np.sin(psi)-del_phi*np.cos(psi)],
                  [-del_theta, -del_phi, 1]])

R_BtoA = np.transpose(R_AtoB)

angularVelocity = np.transpose([0, 0, 0])

t_duration = 15;
orientationMode = 'euler'
if __name__ == '__main__':
    # Create instance of python objects, and custom flightobject stuff
    client = ViconDataStream.RetimingClient()
    cf1 = flightObjectGrapher(orientationMode)
    try:
        client.Connect("localhost:801")
        print("Vicon is connected...", client.IsConnected())
        # Check the version
        print('Version #: ', client.GetVersion())
        client.SetAxisMapping(ViconDataStream.Client.AxisMapping.EForward, ViconDataStream.Client.AxisMapping.ELeft,
                              ViconDataStream.Client.AxisMapping.EUp)
        xAxis, yAxis, zAxis = client .GetAxisMapping()
        print('X Axis', xAxis, 'Y Axis', yAxis, 'Z Axis', zAxis)
        t_begin = time.time()
        while(time.time() < t_begin + t_duration):
            t_current = time.time()
            try:
                frame = client.UpdateFrame()
                # print('frame = ', frame)
                subjectNames = client.GetSubjectNames()
                for subjectName in subjectNames:
                    segmentNames = client.GetSegmentNames(subjectName)
                    for segmentName in segmentNames:
                        # print('current time = ', t_current)

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
                        t_current = time.time()
                        cf1.addPoseVals(XYZ, orientation, frame, t_current-t_begin)
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