from SpellmanHvSupply import  SpellmanHVSupply
import time
HVSupply1 = SpellmanHVSupply()
turnOn = True
if __name__ == '__main__':

    print("opening communciation with HV supply")
    a = HVSupply1.openComm()
    # time.sleep(3)

    if turnOn == True:
        HVSupply1.HVOutput(1)
        print("Turned HV on")
        time.sleep(2)
        HVSupply1.HVOutput(0)
        print("Turned HV off")



    # c = HVSupply1.systemStatus()
    b = HVSupply1.closeComm()
    print("closed communication w/HV Supply")

def turnOnHVSupply():
