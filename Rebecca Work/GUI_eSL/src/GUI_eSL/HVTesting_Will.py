from SpellmanHvSupply import  SpellmanHVSupply

HVSupply1 = SpellmanHVSupply()
if __name__ == '__main__':
    HVSupply1.openComm()
    print("opened  communication")

    HVSupply1.closeComm()
    print("closed communication")

    HVSupply1.HVOutput(True)
    print("Turned HV on")

    HVSupply1.HVOutput(False)
    print("Turned HV off")