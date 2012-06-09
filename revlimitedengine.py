import math

class RevLimitedEngine(object):

	engineSpeedToCarSpeedMultiplier=338

	def __init__(self,startX,endX,baseline):
		self.startX=startX
		self.endX=endX
		self.baseline=baseline
		self.gearTopSpeeds=[]
		self.gearMultipliers=[]
		self.gearIndex=0
		self.currentRevs=0.0
		self.currentSpeed=0.0
		self.maxRevs=10000.0

	def addGear(self,speedAtMaxRevs,multiplier):
		self.gearTopSpeeds.append(speedAtMaxRevs)
		self.gearMultipliers.append(multiplier)

	def getMaxRevIncreaseAtCurrentSpeedInCurrentGear(self):
		currentSpeed=self.currentSpeed
		speedAtMaxRevs=self.gearTopSpeeds[self.gearIndex]
		revIncrease=math.sin(self.startX+((self.endX-self.startX)/speedAtMaxRevs*currentSpeed))*self.gearMultipliers[self.gearIndex]
		return revIncrease

	def advanceFrame(self,acceleration,braking):
		if braking>0:
			acceleration=0

		currentSpeed=self.getSpeed()
		if currentSpeed>self.gearTopSpeeds[self.gearIndex]:
			self.currentRevs=self.currentRevs-50
		else:
			targetRevs=self.maxRevs*acceleration
			if targetRevs>self.currentRevs:
				maxRevIncrease=self.getMaxRevIncreaseAtCurrentSpeedInCurrentGear()
				actualRevIncrease=maxRevIncrease*acceleration
				self.currentRevs=self.currentRevs+actualRevIncrease
				if self.currentRevs>self.maxRevs:
					self.currentRevs=self.maxRevs
			elif targetRevs<self.currentRevs:
				revDifference=self.currentRevs-targetRevs
				revChange=revDifference/100
				if revChange<10:
					revChange=10
				self.currentRevs=self.currentRevs-revChange
				if self.currentRevs<targetRevs:
					self.currentRevs=targetRevs

		speedAtMaxRevs=self.gearTopSpeeds[self.gearIndex]
		speedAtCurrentRevs=float(speedAtMaxRevs)/float(self.maxRevs)*float(self.currentRevs)
		self.currentSpeed=speedAtCurrentRevs

		if braking>0:
			currentSpeed=self.getSpeed()
			currentSpeed=currentSpeed-0.003
			if currentSpeed<0:
				currentSpeed=0
			self.setSpeed(currentSpeed)

	def setCurrentGear(self,gearNumber):
		oldGearIndex=self.gearIndex
		self.gearIndex=gearNumber-1
		self.currentRevs=self.currentRevs*(self.gearTopSpeeds[oldGearIndex]/self.gearTopSpeeds[self.gearIndex])

	def getCurrentGear(self):
		return self.gearIndex+1

	def setSpeed(self,speed):
		speedAtMaxRevs=self.gearTopSpeeds[self.gearIndex]
		self.currentRevs=self.maxRevs/speedAtMaxRevs*speed
		self.currentSpeed=speed

	def getSpeed(self):
		return self.currentSpeed

	def getRevs(self):
		return self.currentRevs

	def setRevs(self,revs):
		self.revs=revs

	@staticmethod
	def convertCarSpeedToEngineSpeed(carSpeed):
		return(carSpeed/RevLimitedEngine.engineSpeedToCarSpeedMultiplier)

	@staticmethod
	def convertEngineSpeedToCarSpeed(engineSpeed):
		return(engineSpeed*RevLimitedEngine.engineSpeedToCarSpeedMultiplier)
