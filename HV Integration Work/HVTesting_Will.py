from SpellmanHvSupply import  SpellmanHVSupply
import time
HVSupply1 = SpellmanHVSupply()
if __name__ == '__main__':
    a = HVSupply1.openComm()
    print("opened  communication")
    HVSupply1.HVOutput(1)
    print("Turned HV on")
    time.sleep(1)

    HVSupply1.HVOutput(False)
    print("Turned HV off")


    # c = HVSupply1.systemStatus()
    b = HVSupply1.closeComm()
    print("closed communication")
