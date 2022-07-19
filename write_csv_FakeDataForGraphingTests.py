import time
import csv
class csvWriterGuy:
    def __init__(self):
        self.x_Fun = lambda(timeval) timeval*.2
        self.y_Fun = lambda(timeval) timeval*.5
        self.z_Fun = lambda(timeval) timeval*.2
        self.roll_Fun = lambda(timeval) timeval*.1
        self.pitch_Fun = lambda(timeval) timeval*.0
        self.yaw_Fun = lambda(timeval) timeval*.0
        self.omega_roll_Fun = lambda(timeval) timeval*.0001
        self.omega_yaw_Fun = lambda(timeval) timeval*.1
        self.omega_pitch_Fun = lambda(timeval) timeval*.1
        self.T1_Fun = lambda(timeval) timeval*.1
        self.T2_Fun = lambda(timeval) timeval*.1
        self.T3_Fun = lambda(timeval) timeval*.1
        self.T4_Fun = lambda(timeval) timeval*.1
    def writeVals(self, timeVal):
        for i in range(self):


if __name__ == "__main__":
    filename = 'FakeFlightData.csv'
    timeBegin = time.time()
    with open(filename, 'w', newline='') as file:

        writer = csv.writer(file)
        writer.writerow({"Time", "Frame"})
        for i in range(0,100):
            timeVal = time.time()
            frame = i
            data = [x, y, z, roll, pitch, yaw, omega_roll, omega_pitch, omega_yaw, T1, T2, T3, T4]
            data = [timeVal, frame]
            writer.writerow(data)
            # time.sleep(.005)