import serial.tools.list_ports

print('----strating port connction ----')
# list  of all Serial Ports
PortsList = serial.tools.list_ports.comports()
print(f'1.Step  object of all ports: {PortsList}')
# count of available ports
PortsCount = len(PortsList)
print(f'2.Step  count of ports: {PortsCount}')

# dictionary for serial ports
availableDevicesDict = {}

for i in range(PortsCount):
    print(f'3.Step  each port: {PortsList[i]}')
    strPort = str(PortsList[i])

    if 'Arduino' in strPort:
        splitPort = strPort.split(' ')
        commPort = (splitPort[0])
        print(f'4.Step  get port: {commPort}')

        serialComm = serial.Serial(commPort, baudrate=9600, timeout=1)

        print(f'serialComm.inWaiting() = {serialComm.inWaiting()}')
        i = 0
        while serialComm.inWaiting() == 0:
            print(f'serial communication: in waiting, i = {i}')
            i += 1
            if i > 1000000:
                print('-:-:-not able to connect with a port-:-:-')
                break
            # pass

        CatVersion = serialComm.readline().decode("utf-8")[:-2]
        print(CatVersion)

        availableDevicesDict[CatVersion] = serialComm
        #serialComm.flush()
        #serialComm.close()

# print(availableDevicesDict)

print(availableDevicesDict.keys())
print('----port connection finished----')

# print(f'isOpen() = {availableDevicesDict["CR-B00-B00-000"].isOpen()}')
#
#
# TestPacket = bytearray(b'\x41\xFF\x42\xFF\x43\xFF')
# t = bytearray(b'ri1\xffri2\xffri3\xffri4\xffrm1\xffrm2\xffrm3\xffrm4\xffrr1\xffrr2\xffrr3\xffrr4\xffrp1\xffrp2\xffrp3\xffrt11\xffrt12\xffrt21\xffrt22\xffrt23\xffrt31\xffrt32\xffrt33\xffrt41\xffrt42\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff')
#
# print(TestPacket)
# availableDevicesDict["CR-B00-B00-000"].write(TestPacket)

# ser.isOpen():
