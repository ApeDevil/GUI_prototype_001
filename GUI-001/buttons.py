
class button:
	def __init__(self, KeySet, Shortcut, Description):
		#self.title = title
		self.KeySet = KeySet
		self.Shortcut = Shortcut
		self.Description = Description

class slider:
	def __init__(self,):
		pass
		#self.title = title
		# self.KeySet = KeySet
		# self.Shortcut = Shortcut
		# self.Description = Description

leftDeviceList  = [
				'LI1',
	'LI2',
	'LI3',
	'LI4',
	'LM1',
	'LM2',
	'LM3',
	'LM4',
	'LR1',
	'LR2',
	'LR3',
	'LR4',
	'LP1',
	'LP2',
	'LP3',
	'LT11',
	'LT12',
	'LT21',
	'LT22',
	'LT23',
	'LT31',
	'LT32',
	'LT33',
	'LT41',
	'LT42',
	# joystick
				'LJM',
	'LJU1',
	'LJU2',
	'LJD1',
	'LJD2',
	'LJL1',
	'LJL2',
	'LJR1',
	'LJR2',
	# scroll wheel
				'LWF',
	'LWB',
]

rightDeviceList = [
				'RI1',
	'RI2',
	'RI3',
	'RI4',
	'RM1',
	'RM2',
	'RM3',
	'RM4',
	'RR1',
	'RR2',
	'RR3',
	'RR4',
	'RP1',
	'RP2',
	'RP3',
	'RT11',
	'RT12',
	'RT21',
	'RT22',
	'RT23',
	'RT31',
	'RT32',
	'RT33',
	'RT41',
	'RT42',
	# joystick
				'RJM',
	'RJU1',
	'RJU2',
	'RJD1',
	'RJD2',
	'RJL1',
	'RJL2',
	'RJR1',
	'RJR2',
	# scroll wheel
				'RWF',
	'RWB',
]



leftDeviceDict = {}

for i,b in enumerate(leftDeviceList):
	#print(f'i {i}   b {b}')
	i = button(bytearray(b'\x30'),'0','zero')
	leftDeviceDict[b] = i
	


rightDeviceDict = {}

for i,b in enumerate(rightDeviceList):
	#print(f'i {i}   b {b}')
	i = button(bytearray(b'\x30'),'0','zero')

	rightDeviceDict[b] = i


#print(leftDeviceDict['LI1'].KeySet)

