
from SpellmanHvSupply import SpellmanHVSupply
import time


hvSupply = SpellmanHVSupply();
if __name__ == "__main__":
    hvSupply.openComm()
    hvSupply.HVOutput(1)
    try:
        hvSupply.setKV(3.3)
        time.sleep(15)
        hvSupply.HVOutput(False)
    except:
        hvSupply.HVOutput(False)
        print("test failed")
    # hvSupply.sendCmd(

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
