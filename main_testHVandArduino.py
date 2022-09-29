
import serial
import time
ser = serial.Serial('COM4', baudrate = 115200, timeout = 1)
def writeVals(intArray):
    vals = bytearray(intArray)
    ser.write(vals)
def getVals():
    # ser.write(b'g')
    arduinoData = ser.readline().decode('ascii')
    return arduinoData

if __name__ == "__main__":
    msgSent = input("Input 4 values of PWM (0-255)")
    for i in range(0,3):
        val = int(input())
        msgSent.append(val)
    print("Python will now send ", msgSent)
    writeVals(msgSent)
    time.sleep(0.005)
    print(getVals())
    time.sleep(1)
    writeVals([0, 0, 0, 0])
    # while True:
    #     bytesWritten = ser.write(array_bytes)
    #     print('bytesWritten: ', bytesWritten)
    #
    #     time.sleep(1)
    #     arduinoData = ser.readline().decode('ascii')
    #     print('type: ', type(arduinoData))
    #     # print('thing', arduinoData[0])
    #     # print('type first index', type(arduinoData[0]))
    #     print('length', len(arduinoData))
    #     print('data = ', arduinoData)
