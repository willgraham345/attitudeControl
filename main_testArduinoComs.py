# from arduinoControl import arduinoControl
# import time
# import numpy
#
# import serial
# from struct import *
# import sys
#
#
# try:
#     ser=serial.Serial(baudrate='115200', timeout=.1, port='com4')
# except:
#     print('Port open error')
#
#
# while True:
#     try:
#         ser.write(pack ('15h',0,1,2,3,4,5,6,7,8,9,10,11,12,13,14))#the 15h is 15 element, and h is an int type data
#         dat=ser.readline()
#         if dat!=b''and dat!=b'\r\n':
#             print(str(dat)) #data is bytes type (b'')
#     except KeyboardInterrupt:
#         break
#     except:
#         print(str(sys.exc_info())) #print error
#         break

import serial
import time
ser = serial.Serial('COM4', baudrate = 115200, timeout = 1)
def writeVals(array):
    vals = bytearray(array)
    ser.write(vals)
def getVals():
    # ser.write(b'g')
    arduinoData = ser.readline().decode('ascii')
    return arduinoData

a = 1; b = 2; c = 3; d = 4;

n
dict =

byteString = bytes(a d)
if __name__ == "__main__":
    while True:
        bytesWritten = ser.write(array_bytes)
        print('bytesWritten: ', bytesWritten)

        time.sleep(1)
        arduinoData = ser.readline().decode('ascii')
        print('type: ', type(arduinoData))
        # print('thing', arduinoData[0])
        # print('type first index', type(arduinoData[0]))
        print('length', len(arduinoData))
        print('data = ', arduinoData)
