from tracksessionevent import TrackSessionEvent
import math

class LogicalCarRepresentation(object):

	def __init__(self,trackSession):
		self.previousSegmentPosition=0
		self.segmentPosition=0
		self.trackSession=trackSession
		self.lapTimeTicks=0
		self.lapTimesInTicks=[]
		self.lapTimerActive=False
		self.speed=0
		self.handbrake=False
		self.exploding=False
		self.ticksUntilExplosionEnd=0
		self.sidewaysMovement=0
		self.lastSegmentPosition=0

	def setCarNumber(self,carNumber):
		self.carNumber=carNumber

	def getCarNumber(self):
		return self.carNumber

	def setSegmentPosition(self,segmentPosition):
		if segmentPosition<self.segmentPosition:
			if self.lapTimerActive:
				self.lapTimesInTicks.append(self.getCurrentLapTimeTicks())
				#print('recorded lap time of '+str(self.getCurrentLapTimeTicks())+' ticks, '+str(len(self.lapTimesInTicks))+' laps completed')
				self.setCurrentLapTimeTicks(0)
				self.trackSession.addEvent(TrackSessionEvent.carCompletedLapEvent,{"participant":self})
			else:
				#print('starting first lap as self.segmentPosition is '+str(self.segmentPosition)+' and segmentPosition is '+str(segmentPosition))
				self.lapTimerActive=True
				self.trackSession.addEvent(TrackSessionEvent.carStartedFirstLapEvent,{"participant":self})
			
		self.segmentPosition=segmentPosition

	def getSegmentPosition(self):
		return self.segmentPosition

	def getLastSegmentPosition(self):
		return self.lastSegmentPosition

	def setSidewaysPosition(self,sidewaysPosition):
		self.sidewaysPosition=sidewaysPosition	

	def getSidewaysPosition(self):
		return self.sidewaysPosition

	def setSpeed(self,speed):
		if speed<0:
			speed=0
		if speed==0 and self.speed!=0:
			self.trackSession.addEvent(TrackSessionEvent.carStoppedEvent,{"participant":self})
		self.speed=speed

	def getSpeed(self):
		return self.speed

	def setVisualPeer(self,visualPeer):
		self.visualPeer=visualPeer

	def getVisualPeer(self):
		return self.visualPeer

	def setDriver(self,driver):
		self.driver=driver

	def getDriver(self):
		return self.driver

	def setTrackSegments(self,trackSegments):
		self.trackSegments=trackSegments

	def getTrackSegments(self):
		return self.trackSegments

	def setCurrentLapTimeTicks(self,lapTimeTicks):
		self.lapTimeTicks=lapTimeTicks

	def getCurrentLapTimeTicks(self):
		return self.lapTimeTicks

	def getLapsCompleted(self):
		return len(self.lapTimesInTicks)

	def getLapTime(self,lapNumber):
		return self.lapTimesInTicks[lapNumber-1]

	def getFastestLapTime(self):
		if len(self.lapTimesInTicks)>0:
			ticks=min(self.lapTimesInTicks)
		else:
			ticks=0
		seconds=ticks/60
		milliseconds=(ticks%60)*5/3
		return {"seconds":seconds,
                "milliseconds":milliseconds}

	def getHandbrake(self):
		return self.handbrake

	def setHandbrake(self,handbrake):
		self.handbrake=handbrake

	def incrementLapTimeTicks(self):
		if self.lapTimerActive:
			self.setCurrentLapTimeTicks(self.getCurrentLapTimeTicks()+1)

	def applyForwardMovement(self):
		speed=self.getSpeed()
		segmentPosition=self.getSegmentPosition()
		self.lastSegmentPosition=segmentPosition
		segmentPosition=segmentPosition+speed
		if segmentPosition>float(len(self.trackSegments)):
			segmentPosition=segmentPosition-float(len(self.trackSegments))
		self.setSegmentPosition(segmentPosition)

	def move(self):
		pass

	def explode(self):
		self.exploding=True
		self.getVisualPeer().startExplodingAnimation()

	def updateExplosion(self):
		if self.getVisualPeer().isExplosionActive():
			self.ticksUntilExplosionEnd=60
		if self.ticksUntilExplosionEnd>0:
			self.ticksUntilExplosionEnd=self.ticksUntilExplosionEnd-1
			if self.ticksUntilExplosionEnd==0:
				self.onExplosionEnd()	

	def onExplosionEnd(self):
		self.exploding=False
		self.getVisualPeer().stopExplodingAnimation()

	def getExploding(self):
		return self.exploding

	def setSidewaysMovement(self,sidewaysMovement):
		self.sidewaysMovement=sidewaysMovement

	def getSidewaysMovement(self):
		return self.sidewaysMovement

		
