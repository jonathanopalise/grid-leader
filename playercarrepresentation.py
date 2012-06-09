from logicalcarrepresentation import LogicalCarRepresentation
from destinationlane import DestinationLane
from revlimitedengine import RevLimitedEngine
import math
from soundserver import SoundServer
from gearbox import Gearbox
from tracksessionevent import TrackSessionEvent

class PlayerCarRepresentation(LogicalCarRepresentation):

	topSpeedInLowGear=170.0
	topSpeedInHighGear=288.0

	maxSidewaysPosition=1.25
	startSlowdownSidewaysPosition=0.85
	speedAtMaxSidewaysPosition=0.236
	speedAtStartSlowdownSidewaysPosition=0.42

	def __init__(self,trackSession):
		super(PlayerCarRepresentation, self).__init__(trackSession)
		self.speedMultiplier=1
		self.hasArrivedAtDestinationLane=True

		engine=RevLimitedEngine(0.3,2.54,0.5)
		engine.addGear(RevLimitedEngine.convertCarSpeedToEngineSpeed(self.topSpeedInLowGear),35)
		engine.addGear(RevLimitedEngine.convertCarSpeedToEngineSpeed(self.topSpeedInHighGear),20)

		engine.setCurrentGear(1)
		self.engine=engine
	
	def setSpeedAdjust(self,speedAdjust):
		self.speedAdjust=speedAdjust

	def getSpeedAdjust(self):
		return self.speedAdjust

	def getSteering(self):
		if self.getExploding():
			steering=self.preExplosionSteering
		else:
			steering=self.driver.getSteering()
		return steering

	def applyManualSteeringAndSkidding(self):

		sidewaysPosition=self.getSidewaysPosition()
		sidewaysPositionBefore=sidewaysPosition

		speed=self.engine.getSpeed()
		steering=self.getSteering()

		sidewaysPosition=sidewaysPosition+(steering/2)*speed
		if sidewaysPosition>1.25:
			sidewaysPosition=1.25
		elif sidewaysPosition<-1.25:
			sidewaysPosition=-1.25

		currentSegment=int(math.floor(self.getSegmentPosition()))
		skidPotential=self.trackSession.getCornerSharpness(currentSegment)

		threshold=0.5
		if skidPotential>threshold:
			skidPotential=((skidPotential-threshold)*(skidPotential-threshold))+threshold
		if skidPotential<-threshold:
			skidPotential=((skidPotential+threshold)*(skidPotential+threshold))-threshold

		actualSkid=skidPotential*speed*40
		actualSkidNegative=actualSkid<0
		actualSkid=math.fabs(actualSkid)

		newSpeed=speed-actualSkid/600
		self.engine.setSpeed(newSpeed)
		self.setSpeed(newSpeed)
			
		if actualSkid>1.0:
			actualSkid=actualSkid+((actualSkid-1)*(actualSkid-1))
		if actualSkidNegative:
			actualSkid=-actualSkid

		sidewaysPosition=sidewaysPosition+(actualSkid/10)
		self.setSidewaysPosition(sidewaysPosition)

		#self.engine.setSpeed(speed)
		self.setSidewaysMovement(sidewaysPosition-sidewaysPositionBefore)

	def detectCollisions(self):
		if not self.getExploding():
			logicalCars=self.trackSession.getLogicalCarRepresentations()
			for otherCar in logicalCars:
				if not otherCar is self:
					segmentPositionDifference=otherCar.getSegmentPosition()-self.getSegmentPosition()
					if segmentPositionDifference>-0.62 and segmentPositionDifference<0.62:
						sidewaysPositionDifference=otherCar.getSidewaysPosition()-self.getSidewaysPosition()
						if sidewaysPositionDifference>-0.32 and sidewaysPositionDifference<0.32:

							selfSidewaysMovement=self.getSidewaysMovement()
							otherSidewaysMovement=otherCar.getSidewaysMovement()
							selfSpeed=self.getSpeed()
							otherSpeed=otherCar.getSpeed()

							sidewaysDifference=selfSidewaysMovement-otherSidewaysMovement
							speedDifference=selfSpeed-otherSpeed

							collisionSpeed=math.sqrt((sidewaysDifference*sidewaysDifference)+(speedDifference*speedDifference))

							if collisionSpeed>0.05:
								if not self.getExploding():
									self.explode()
									otherCar.explode()
							else:
								adjustedSegmentPositionDifference=segmentPositionDifference/6*3.2
								if math.fabs(adjustedSegmentPositionDifference)>math.fabs(sidewaysPositionDifference):
									if segmentPositionDifference>0.0:
										self.segmentPosition=otherCar.getSegmentPosition()-0.62
										self.engine.setSpeed(otherCar.getSpeed()-0.05)
									else:
										self.segmentPosition=otherCar.getSegmentPosition()+0.62
										self.setSpeed(otherCar.getSpeed()+0.05)
										self.engine.setSpeed(otherCar.getSpeed()+0.05)
								else:
									if sidewaysPositionDifference>0.0:
										self.setSidewaysPosition(otherCar.getSidewaysPosition()-0.32)
									else:
										self.setSidewaysPosition(otherCar.getSidewaysPosition()+0.32)

	def getDestinationLane(self):
		if self.getSidewaysPosition()>0:
			return DestinationLane.right
		else:
			return DestinationLane.left
		
	def applyGroundFriction(self):

		startSlowdownSidewaysPosition=self.startSlowdownSidewaysPosition
		speedAtMaxSidewaysPosition=self.speedAtMaxSidewaysPosition
		speedAtStartSlowdownSidewaysPosition=self.speedAtStartSlowdownSidewaysPosition
		maxSidewaysPosition=self.maxSidewaysPosition

		absoluteSidewaysPosition=math.fabs(self.getSidewaysPosition())

		segmentPositionComponents=math.modf(self.segmentPosition)
		lastSegmentPositionComponents=math.modf(self.lastSegmentPosition)

		if absoluteSidewaysPosition>0.725 and absoluteSidewaysPosition<1.15:
			if segmentPositionComponents[0]<lastSegmentPositionComponents[0]:
				SoundServer.getInstance().playBump()

		if absoluteSidewaysPosition>startSlowdownSidewaysPosition:
			forcedSpeed=speedAtStartSlowdownSidewaysPosition+(speedAtMaxSidewaysPosition-speedAtStartSlowdownSidewaysPosition)/(maxSidewaysPosition-startSlowdownSidewaysPosition)*(absoluteSidewaysPosition-startSlowdownSidewaysPosition)
			currentSpeed=self.getSpeed()
			if currentSpeed>forcedSpeed:
				self.engine.setSpeed(currentSpeed-0.01)

	def updateSpeed(self):
		driver=self.getDriver()

		if driver.getGearChangeRequested():
			driver.acknowledgeGearChangeRequested()
			if self.engine.getCurrentGear()==1:
				self.engine.setCurrentGear(2)
				newGear=Gearbox.high
			else:
				self.engine.setCurrentGear(1)
				newGear=Gearbox.low
			self.trackSession.addEvent(TrackSessionEvent.gearChangedEvent,{ "gear" : newGear })

		if self.getHandbrake()==True:
			braking=1.0
		elif self.getExploding()==True:
			braking=3.0
		else:
			braking=driver.getBraking()

		self.engine.advanceFrame(driver.getAcceleration(),braking)
		self.setSpeed(self.engine.getSpeed())

	def recordCurrentPosition(self):
		self.oldSegmentPosition=self.segmentPosition
		self.oldSidewaysPosition=self.sidewaysPosition

	def detectSceneryCollisions(self):
		if not self.getExploding():
			sceneryPositions=self.trackSession.getSceneryPositions()
			for sceneryPosition in sceneryPositions:
				if self.segmentPosition>sceneryPosition['segment'] and self.oldSegmentPosition<sceneryPosition['segment']:
					if sceneryPosition['sidewaysposition']=='left':
						if self.sidewaysPosition<-0.95:
							self.explode()
					else:
						if self.sidewaysPosition>0.95:
							self.explode()

			puddlePositions=self.trackSession.getPuddlePositions()
			for puddlePosition in puddlePositions:
				segmentPositionDifference=puddlePosition['segment']-self.getSegmentPosition()
				if segmentPositionDifference>-0.62 and segmentPositionDifference<0.62:
					sidewaysPositionDifference=puddlePosition['sidewaysposition']-self.getSidewaysPosition()
					if sidewaysPositionDifference>-0.32 and sidewaysPositionDifference<0.32:
						newSpeed=self.getSpeed()-0.05
						if newSpeed<0.05:
							newSpeed=0.05
						self.setSpeed(newSpeed)
						self.engine.setSpeed(newSpeed)
			
	def explode(self):
		super(PlayerCarRepresentation, self).explode()
		self.preExplosionSteering=self.driver.getSteering()
		SoundServer.getInstance().playExplosion()
		self.trackSession.setSpeedLimit(0.25)

	def getEngine(self):
		return(self.engine)

	def onExplosionEnd(self):
		super(PlayerCarRepresentation, self).onExplosionEnd()
		self.trackSession.setSpeedLimit(self.trackSession.speedLimitUnlimited)
	
	def move(self):

		super(PlayerCarRepresentation, self).move()

		driver=self.getDriver()
		self.updateSpeed()
		self.applyGroundFriction()
		self.recordCurrentPosition()
		self.applyForwardMovement()
		self.applyManualSteeringAndSkidding()
		self.incrementLapTimeTicks()
		self.updateExplosion()

