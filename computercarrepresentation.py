from logicalcarrepresentation import LogicalCarRepresentation
import math
from destinationlane import DestinationLane
import random
from qualifyingsessionstatus import QualifyingSessionStatus
from racesessionstatus import RaceSessionStatus
from sessiontype import SessionType

class ComputerCarRepresentation(LogicalCarRepresentation):

	def __init__(self,trackSession):
		super(ComputerCarRepresentation, self).__init__(trackSession)
		self.hasArrivedAtDestinationLane=True
		self.topSpeed=0.675+random.random()/5
		self.targetCornerSpeed=self.topSpeed
		self.targetCarInteractionSpeed=self.topSpeed
		self.lastMoveWasWrap=False

	def getLastMoveWasWrap(self):
		return self.lastMoveWasWrap

	def setLastMoveWasWrap(self,lastMoveWasWrap):
		self.lastMoveWasWrap=lastMoveWasWrap

	def setCurrentLane(self,currentLane):
		self.destinationLane=currentLane
		self.hasArrivedAtDestinationLane=True

	def setDestinationLane(self,destinationLane):
		self.destinationLane=destinationLane
		self.hasArrivedAtDestinationLane=False

	def getDestinationLane(self):
		return self.destinationLane

	def approachDestinationLane(self):
		if not self.hasArrivedAtDestinationLane:
			sidewaysPosition=self.getSidewaysPosition()
			if self.destinationLane==DestinationLane.left:
				sidewaysPosition=sidewaysPosition-0.0075
				self.setSidewaysMovement(-0.0075)
				if sidewaysPosition<DestinationLane.leftPosition:
					sidewaysPosition=DestinationLane.leftPosition
					self.hasArrivedAtDestinationLane=True
			else:
				sidewaysPosition=sidewaysPosition+0.0075
				self.setSidewaysMovement(0.0075)
				if sidewaysPosition>DestinationLane.rightPosition:
					sidewaysPosition=DestinationLane.rightPosition
					self.hasArrivedAtDestinationLane=True
			self.setSidewaysPosition(sidewaysPosition)

	def avoidCollisions(self):
		logicalCars=self.trackSession.getLogicalCarRepresentations()
		threatInSameLane=False
		threatInOtherLane=False
		overtakeRequired=False
		overtakingWouldBeStupid=False
		speedOfClosestSameLaneThreat=1000
		distanceOfClosestSameLaneThreat=1000

		if not self.hasArrivedAtDestinationLane:
			overtakingWouldBeStupid=True

		for otherCar in logicalCars:
			if not otherCar is self:
				segmentPositionDifference=otherCar.getSegmentPosition()-self.getSegmentPosition()
				speedDifference=self.getSpeed()-otherCar.getSpeed()
				if segmentPositionDifference<15.0 and segmentPositionDifference>0.0:
					if otherCar.getDestinationLane()==self.getDestinationLane():
						threatInSameLane=True
						if segmentPositionDifference<distanceOfClosestSameLaneThreat:
							distanceOfClosestSameLaneThreat=segmentPositionDifference
							speedOfClosestSameLaneThreat=otherCar.getSpeed()
					else:
						threatInOtherLane=True
				if segmentPositionDifference<15.0 and segmentPositionDifference>-5.0 and not otherCar.hasArrivedAtDestinationLane:
					overtakingWouldBeStupid=True

		if threatInSameLane and threatInOtherLane:
			if distanceOfClosestSameLaneThreat<5.0 and speedDifference>0.1:
				self.setTargetCarInteractionSpeed(speedOfClosestSameLaneThreat-0.025)
			else:
				self.setTargetCarInteractionSpeed(speedOfClosestSameLaneThreat)
		else:
			if threatInSameLane and overtakingWouldBeStupid:
				self.setTargetCarInteractionSpeed(speedOfClosestSameLaneThreat)
			else:
				self.setTargetCarInteractionSpeed(self.topSpeed)

			if threatInSameLane and self.getSpeed()>speedOfClosestSameLaneThreat and not overtakingWouldBeStupid:
				currentLane=self.getDestinationLane()
				if currentLane==DestinationLane.left:
					destinationLane=DestinationLane.right
				else:
					destinationLane=DestinationLane.left
				self.setDestinationLane(destinationLane)

	def setCornerSpeed(self):
		currentSegment=int(math.floor(self.getSegmentPosition()))
		sharpness=math.fabs(self.trackSession.getCornerSharpness(currentSegment+10))
		self.setTargetCornerSpeed(0.85-sharpness*4)
		pass

	def getSpeed(self):
		return self.speed

	def setTargetCornerSpeed(self,targetSpeed):
		if targetSpeed<0:
			targetSpeed=0
		if targetSpeed>self.topSpeed:
			targetSpeed=self.topSpeed
		self.targetCornerSpeed=targetSpeed

	def setTargetCarInteractionSpeed(self,targetSpeed):
		if targetSpeed<0:
			targetSpeed=0
		if targetSpeed>self.topSpeed:
			targetSpeed=self.topSpeed
		self.targetCarInteractionSpeed=targetSpeed
		
	def getTargetSpeed(self):
		speeds=[self.targetCornerSpeed,self.targetCarInteractionSpeed,self.trackSession.getSpeedLimit()]
		return min(speeds)

		#if self.targetCornerSpeed<self.targetCarInteractionSpeed:
		#	return self.targetCornerSpeed
		#else:
		#	return self.targetCarInteractionSpeed

	def updateSpeed(self):
		if self.getExploding():
			self.setTargetCornerSpeed(0)
			self.setTargetCarInteractionSpeed(0)
			speed=self.getSpeed()
			speed=speed-0.0075
			if speed<0:
				speed=0
			self.setSpeed(speed)
			
		else:

			targetSpeed=self.getTargetSpeed()
			if self.getHandbrake()==True:
				targetSpeed=0

			speed=self.getSpeed()
			if speed>targetSpeed:
				speed=speed-0.01
				if speed<targetSpeed:	
					speed=targetSpeed
			else:
				speed=speed+self.topSpeed/700
				if speed>targetSpeed:
					speed=targetSpeed
			self.setSpeed(speed)

	def checkPlayerRelativeBoundary(self):
		self.setLastMoveWasWrap(False)

		playerCar=self.trackSession.getPlayerCar()
		if not playerCar:
			playerCar=self.trackSession.getCameraCar()

		playerSegmentPosition=playerCar.getSegmentPosition()
		selfSegmentPosition=self.getSegmentPosition()
		selfSpeed=self.getSpeed()

		forwardZoneSize=120.0
		backwardZoneSize=20.0

		insideForwardBoundary=False
		forwardBoundaryWrapped=False

		forwardBoundary=playerSegmentPosition+forwardZoneSize
		if forwardBoundary>len(self.trackSession.getSegments()):
			forwardBoundary=forwardBoundary-len(self.trackSession.getSegments())
			forwardBoundaryWrapped=True

		if forwardBoundaryWrapped:
			if selfSegmentPosition>=playerSegmentPosition or selfSegmentPosition<=forwardBoundary:
				insideForwardBoundary=True
		else:
			if selfSegmentPosition>=playerSegmentPosition and selfSegmentPosition<=forwardBoundary:
				insideForwardBoundary=True

		insideBackwardBoundary=False
		backwardBoundaryWrapped=False

		backwardBoundary=playerSegmentPosition-backwardZoneSize
		if backwardBoundary<0:
			backwardBoundary=backwardBoundary+len(self.trackSession.getSegments())
			backwardBoundaryWrapped=True

		if backwardBoundaryWrapped:
			if selfSegmentPosition<=playerSegmentPosition or selfSegmentPosition>=backwardBoundary:
				insideBackwardBoundary=True
		else:
			if selfSegmentPosition>=backwardBoundary and selfSegmentPosition<=playerSegmentPosition:
				insideBackwardBoundary=True

		if not insideForwardBoundary and not insideBackwardBoundary:

			selfAheadOfPlayer=False
			halfTrackBoundaryWrapped=False

			halfTrackBoundary=playerSegmentPosition+len(self.trackSession.getSegments())/2
			if halfTrackBoundary>len(self.trackSession.getSegments()):
				halfTrackBoundary=forwardBoundary-len(self.trackSession.getSegments())
				halfTrackBoundaryWrapped=True

			if halfTrackBoundaryWrapped:
				if selfSegmentPosition>playerSegmentPosition or selfSegmentPosition<halfTrackBoundary:
					selfAheadOfPlayer=True
			else:
				if selfSegmentPosition>playerSegmentPosition and selfSegmentPosition<halfTrackBoundary:
					selfAheadOfPlayer=True

			if selfAheadOfPlayer:
				self.setLastMoveWasWrap(True)
				selfSpeed=0.01
				selfSegmentPosition=playerSegmentPosition-backwardZoneSize
				if selfSegmentPosition<0:
					selfSegmentPosition=selfSegmentPosition+len(self.trackSession.getSegments())
			else:
				self.setLastMoveWasWrap(True)
				selfSegmentPosition=playerSegmentPosition+forwardZoneSize
				selfSpeed=playerCar.getSpeed()-0.05
				if self.speed>self.topSpeed:
					self.speed=self.topSpeed
				if selfSegmentPosition>len(self.trackSession.getSegments()):
					selfSegmentPosition=selfSegmentPosition-len(self.trackSession.getSegments())

		self.setSpeed(selfSpeed)
		self.setSegmentPosition(selfSegmentPosition)

	def updatePlayerDistance(self):
		playerCar=self.trackSession.getPlayerCar()
		if not playerCar:
			playerCar=self.trackSession.getCameraCar()

		playerSegmentPosition=playerCar.getSegmentPosition()
		selfSegmentPosition=self.getSegmentPosition()

		if selfSegmentPosition<playerSegmentPosition and selfSegmentPosition>playerSegmentPosition-10.0:
			distance=playerSegmentPosition-selfSegmentPosition
		elif selfSegmentPosition>playerSegmentPosition and selfSegmentPosition<playerSegmentPosition+10.0:
			distance=selfSegmentPosition-playerSegmentPosition
		else:
			distance=10.0

		self.playerDistance=distance

	def getPlayerDistance(self):
		return self.playerDistance

	def move(self):

		moveCar=True

		sessionType=self.trackSession.getSessionType()
		if sessionType==SessionType.qualifying or sessionType==SessionType.race:
			sessionStatus=self.trackSession.getSessionStatus()
			if 	sessionStatus==QualifyingSessionStatus.qualifyingSuccessStatus or sessionStatus==RaceSessionStatus.raceSuccessStatus:
				if self.segmentPosition>len(self.trackSession.getSegments())-10:
					moveCar=False

		if moveCar:
			super(ComputerCarRepresentation, self).move()

			self.avoidCollisions()
			self.setCornerSpeed()
			self.updateSpeed()
			self.applyForwardMovement()
			self.checkPlayerRelativeBoundary()
			self.updatePlayerDistance()
			self.approachDestinationLane()
			self.incrementLapTimeTicks()
			self.updateExplosion()

	def onExplosionEnd(self):
		super(ComputerCarRepresentation, self).onExplosionEnd()

		segmentPosition=self.getSegmentPosition()	
		segmentPosition=segmentPosition+float(len(self.trackSegments)/2)
		if segmentPosition>float(len(self.trackSegments)):
			segmentPosition=segmentPosition-float(len(self.trackSegments))
		self.setSegmentPosition(segmentPosition)

	
		
