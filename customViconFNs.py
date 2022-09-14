

from vicon_dssdk import ViconDataStream
import time
def connectToVicon(clientInstance):
    clientInstance.Connect("localhost:801",250)
    print("Vicon is connected...", clientInstance.IsConnected())
    # Check the version
    print('Version #: ', clientInstance.GetVersion())
    clientInstance.SetAxisMapping(ViconDataStream.Client.AxisMapping.EForward, ViconDataStream.Client.AxisMapping.ELeft,
                          ViconDataStream.Client.AxisMapping.EUp)
    xAxis, yAxis, zAxis = clientInstance.GetAxisMapping()
    print('X Axis', xAxis, 'Y Axis', yAxis, 'Z Axis', zAxis)
    time.sleep(1)
    return


def viconLoop()
    subjectNames = client.GetSubjectNames()
    for subjectName in subjectNames:
        segmentNames = client.GetSegmentNames(subjectName)
        for segmentName in segmentNames:
            print(segmentName)
            # print('current time = ', t_current)

            ''' Get data from VICON'''
            [(X, Y, Z), occlusion2] = client.GetSegmentGlobalTranslation(subjectName, segmentName)
            [(roll, pitch, yaw), occlusion1] = client.GetSegmentGlobalRotationEulerXYZ(subjectName,
                                                                                       segmentName)
            XYZ = (X, Y, Z)
            orientation = (roll, pitch, yaw)
    return