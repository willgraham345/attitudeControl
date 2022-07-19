"""implement this into the main, right underneath for segmentName in segmentNames"""

if orientationMode == 'euler':
    [(X, Y, Z), occlusion2] = client.GetSegmentGlobalTranslation(subjectName, segmentName)
    [(roll, pitch, yaw), occlusion1] = client.GetSegmentGlobalRotationEulerXYZ(subjectName,
                                                                               segmentName)
    XYZ = (X, Y, Z)
    orientation = (roll, pitch, yaw)
elif orientationMode == 'quaternion':
    [(X, Y, Z), occlusion2] = client.GetSegmentGlobalTranslation(subjectName, segmentName)
    [(q_x, q_y, q_z, q_w), occlusion3] = client.GetSegmentGlobalRotationQuaternion(subjectName, segmentName)
    XYZ = (X, Y, Z)
    orientation = (roll, pitch, yaw)

"""Add this to the flightObjectGrapher"""

if (self.orientationMode == 'euler'):
    roll, pitch, yaw = orientation
    self.roll.append(roll)
    self.pitch.append(pitch)
    self.yaw.append(yaw)
elif (self.orientationMode == 'quaternion'):
    qx, qy, qz, qw = orientation
    self.qx.append(qx)
    self.qy.append(qy)
    self.qz.append(qz)
    self.qw.append(qw)


"""In graph Pose Vals"""
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
elif (self.orientationMode == 'quaternion'):
    print("visualization for quaternions not yet supported (or understood) by our good friend Will")
# for i in range(len(self.t)):
#     samplingRate[i] = self.t(i) - self.t(i)
