

from vicon_dssdk import ViconDataStream
import time
def connectToVicon(client):
    client.Connect("localhost:801",250)
    print("Vicon is connected...", client.IsConnected())
    # Check the version
    print('Version #: ', client.GetVersion())
    client.SetAxisMapping(ViconDataStream.Client.AxisMapping.EForward, ViconDataStream.Client.AxisMapping.ELeft,
                          ViconDataStream.Client.AxisMapping.EUp)
    xAxis, yAxis, zAxis = client.GetAxisMapping()
    print('X Axis', xAxis, 'Y Axis', yAxis, 'Z Axis', zAxis)
    time.sleep(1)
    return


def viconLoop(client):
    try:
        subjectNames = client.GetSubjectNames()
        for subjectName in subjectNames:
            segmentNames = client.GetSegmentNames(subjectName)
            for segmentName in segmentNames:
                # print(segmentName)
                # print('current time = ', t_current)

                ''' Get data from VICON'''
                [(X, Y, Z), occlusion2] = client.GetSegmentGlobalTranslation(subjectName, segmentName)
                [(roll, pitch, yaw), occlusion1] = client.GetSegmentGlobalRotationEulerXYZ(subjectName,
                                                                                           segmentName)
                XYZ = (X, Y, Z)
                orientation = (roll, pitch, yaw)
                return XYZ, orientation, True
    except ViconDataStream.DataStreamException as e:
        print('Handled data stream error (Nested)... ERROR:', e)
        return 0, 0, False
