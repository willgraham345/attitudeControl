
import serial
import time
import numpy as np
ser = serial.Serial('COM4', baudrate = 115200, timeout = 1)
def writeVals(intArray):
    vals = bytearray(intArray)
    ser.write(vals)
def getVals():
    # ser.write(b'g')
    arduinoData = ser.readline().decode('ascii')
    return arduinoData
ser = serial.Serial('COM4', baudrate = 115200, timeout = 1)
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
if __name__ == "__main__":
    a = 1; b = 2; c = 3; d = 4;
    comma = ','
    while True:
        msgSendStr = 's' + '5'+ 'e'
        print(msgSendStr);
        ser.write(b'msgSendStr')
        # print(print(msgSendStr.encode('utf-8')));
        # print()
        print("received: ", ser.readline().decode())
