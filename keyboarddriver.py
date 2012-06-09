from driverinterface import DriverInterface
from keyboardhandler import KeyboardHandler

class KeyboardDriver(DriverInterface):

	def __init__(self):
		self.keyboardHandler=KeyboardHandler.getInstance()

		self.acceleration=0
		self.braking=0
		self.steering=0
		self.gearChangeRequested=0
		self.pauseToggleRequested=0

	def interpretInputs(self):
		upArrow=self.keyboardHandler.getUpArrowStatus()
		downArrow=self.keyboardHandler.getDownArrowStatus()
		leftArrow=self.keyboardHandler.getLeftArrowStatus()
		rightArrow=self.keyboardHandler.getRightArrowStatus()
		space=self.keyboardHandler.getSpaceStatus()
		pause=self.keyboardHandler.getPStatus()

		if space==1:
			self.gearChangeRequested=True
			self.keyboardHandler.clearSpaceStatus()

		if pause==1:
			self.pauseToggleRequested=True
			self.keyboardHandler.clearPStatus()

		if upArrow==1:
			self.acceleration=1.0
		elif downArrow==1:
			self.braking=1.0
		else:
			self.acceleration=0
			self.braking=0

		if leftArrow==1:
			self.steering=self.steering-75
			if self.steering<-10000:
				self.steering=-10000
		elif rightArrow==1:
			self.steering=self.steering+75
			if self.steering>10000:
				self.steering=10000

	def getAcceleration(self):
		return float(self.acceleration)

	def getBraking(self):
		return float(self.braking)

	def getSteering(self):
		return float(self.steering)/10000

	def getGearChangeRequested(self):
		return self.gearChangeRequested

	def acknowledgeGearChangeRequested(self):
		self.gearChangeRequested=False

	def getPauseToggleRequested(self):
		return self.pauseToggleRequested

	def acknowledgePauseToggleRequested(self):
		self.pauseToggleRequested=False

