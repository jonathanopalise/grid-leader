from logicalcarrepresentation import LogicalCarRepresentation
from trackgeometry import TrackGeometry
from visualtracksession import VisualTrackSession
from keyboarddriver import KeyboardDriver
from tracksessionevent import TrackSessionEvent
from sessionlifecyclepoint import SessionLifecyclePoint
from tracksession import TrackSession
from sessiontype import SessionType
from carappearance import CarAppearance
from destinationlane import DestinationLane
import random
from qualifyingsessionstatus import QualifyingSessionStatus

class QualifyingSession(TrackSession):

	sessionType=SessionType.qualifying

	qualifyingLapTimesInTicks=[
		{ 'ticks':58.5*60,'bonus':4000 },
		{ 'ticks':60.0*60,'bonus':2000 },
		{ 'ticks':62.0*60,'bonus':1400 },
		{ 'ticks':64.0*60,'bonus':1000 },
		{ 'ticks':66.0*60,'bonus':800 },
		{ 'ticks':68.0*60,'bonus':600 },
		{ 'ticks':70.0*60,'bonus':400 },
		{ 'ticks':73.0*60,'bonus':200 }
	]

	def __init__(self,topScore):
		super(QualifyingSession, self).__init__()

		self.startingScore=0
		self.setTopScore(topScore)

		self.visualTrackSession.runBlimpFlight(self.getPlayerCar().getSegmentPosition(),False)
		self.visualTrackSession.runQualifyingLightsSequence()
		self.overtakeTrackingEnabled=False

	def initSession(self):
		self.sessionStatus=QualifyingSessionStatus.qualifyingInProgressStatus
		self.ticksRemaining=90*self.framesPerSecond
		self.score=0

		keyboardDriver=KeyboardDriver()

		for i in range(6):
			if i==0:
				segmentPosition=float(len(self.segments))-(float(i)+4.0)
				newCar=self.addPlayerCar(segmentPosition,0,0,CarAppearance.redAndOrange)
				self.setPlayerCar(newCar)
				self.setCameraCar(newCar)
			else:
				newCar=self.addRandomCar()
			newCar.setHandbrake(True)

	def recordQualifyingDetails(self,lapTimeTicks,position,bonus,score):
		self.qualifyingDetails={ "laptimeticks"        : lapTimeTicks,
                                 "position"            : position,
                                 "bonus"               : bonus,
								 "score"               : score }

	def getRecordedQualifyingDetails(self):
		return self.qualifyingDetails

	def onCarCompletedLap(self,participant):
		if participant is self.getPlayerCar():
			self.sendPlayerLapCompletionEventToVisualTrackSession()	
			playerLapTimeInTicks=participant.getLapTime(participant.getLapsCompleted())
			testingPosition=1
			confirmedPosition=0
			for positionQualifyingInfo in self.qualifyingLapTimesInTicks:
				requiredLapTimeForPositionInTicks=positionQualifyingInfo['ticks']
				if playerLapTimeInTicks<=requiredLapTimeForPositionInTicks:
					bonus=positionQualifyingInfo['bonus']
					confirmedPosition=testingPosition
					break
				testingPosition=testingPosition+1
			if confirmedPosition>0:
				self.scoringActive=False
				self.getPlayerCar().setHandbrake(True)
				self.setSessionStatus(QualifyingSessionStatus.qualifyingSuccessStatus)
				self.recordQualifyingDetails(playerLapTimeInTicks,confirmedPosition,bonus,self.getScore()+bonus)
				self.setSpeedLimit(0.25)

	def onCarStopped(self,participant):
		if self.getOutcome() is None:
			sessionStatus=self.getSessionStatus()
			if sessionStatus==QualifyingSessionStatus.qualifyingSuccessStatus:
				qualifyingDetails=self.getRecordedQualifyingDetails()
				seconds=qualifyingDetails["laptimeticks"]/60
				milliseconds=(qualifyingDetails["laptimeticks"]%60)*5/3
				fastestLapTime=self.getFastestLapTime()
				self.setOutcome({"sessiontype":SessionType.qualifying,
                                 "qualified":True,
                                 "score":qualifyingDetails["score"],
                                 "position":qualifyingDetails["position"],
                                 "topscore":self.getTopScore(),
                                 "laptimeseconds":fastestLapTime["seconds"],
                                 "laptimemilliseconds":fastestLapTime["milliseconds"],
                                 "topspeed":self.getTopSpeed()})
				self.visualTrackSession.displayQualifyingResult(seconds,milliseconds,qualifyingDetails["position"],qualifyingDetails["bonus"])
				self.visualTrackSession.runBlimpFlight(self.getPlayerCar().getSegmentPosition(),True)
			elif sessionStatus==QualifyingSessionStatus.qualifyingTimeExpiredStatus:
				fastestLapTime=self.getFastestLapTime()
				self.setOutcome({"sessiontype":SessionType.qualifying,
                                 "segmentposition":self.getPlayerCar().getSegmentPosition(),
                                 "sidewaysposition":self.getPlayerCar().getSidewaysPosition(),
                                 "qualified":False,
                                 "score":self.getScore(),
                                 "topscore":self.getTopScore(),
                                 "laptimeseconds":fastestLapTime["seconds"],
                                 "laptimemilliseconds":fastestLapTime["milliseconds"],
                                 "topspeed":self.getTopSpeed()})
				self.addEvent(TrackSessionEvent.sessionCompleteEvent)

	def onSessionComplete(self):
		self.closeSession()

	def onCarOvertookAnotherCar(self,overtaker,overtakee):
		# need this to calculate the passing bonus at end of race
		pass

	def onTimeExpired(self):
		self.setSessionStatus(QualifyingSessionStatus.qualifyingTimeExpiredStatus)
		if self.getPlayerCar().getSpeed()>0:
			self.getPlayerCar().setHandbrake(True)
		else:
			self.onCarStopped(self.getPlayerCar())

	def getQualifyingPositionByTicks(ticks):
		pass


