# This is a sample Python script.
from __future__ import print_function
from vicon_dssdk import ViconDataStream
import argparse
import numpy as np
from flightObject import flightObject
import time
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


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














if __name__ == '__main__':
    # from __future__ import print_function
    from vicon_dssdk import ViconDataStream

    client = ViconDataStream.RetimingClient()

    try:
        client.Connect("localhost:801")

        # Check the version
        print('Version', client.GetVersion())

        client.SetAxisMapping(ViconDataStream.Client.AxisMapping.EForward, ViconDataStream.Client.AxisMapping.ELeft,
                              ViconDataStream.Client.AxisMapping.EUp)
        xAxis, yAxis, zAxis = client.GetAxisMapping()
        print('X Axis', xAxis, 'Y Axis', yAxis, 'Z Axis', zAxis)
        while (True):
            try:
                client.UpdateFrame()
                print('1')
                subjectNames = client.GetSubjectNames()
                print('2')
                for subjectName in subjectNames:
                    segmentNames = client.GetSegmentNames(subjectName)
                    for segmentName in segmentNames:
                        rpy = client.GetSegmentGlobalRotationEulerXYZ(subjectName, segmentName)
                        XYZ = client.GetSegmentGlobalTranslation(subjectName, segmentName)
                        q1q2q3 = client.GetSegmentGlobalRotationQuaternion(subjectName, segmentName)
                        print('roll pitch yaw', rpy)
                        print('XYZ', XYZ )
                        print('quaternion', q1q2q3)

            except ViconDataStream.DataStreamException as e:
                print('Nested Try')
                print('Handled data stream error')
    except ViconDataStream.DataStreamException as e:
        print('Global Try')
        print('Handled data stream error', e)