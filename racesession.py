from logicalcarrepresentation import LogicalCarRepresentation
from trackgeometry import TrackGeometry
from collections import deque
from visualtracksession import VisualTrackSession
from keyboarddriver import KeyboardDriver
from tracksessionevent import TrackSessionEvent
from sessionlifecyclepoint import SessionLifecyclePoint
from tracksession import TrackSession
from sessiontype import SessionType
from carappearance import CarAppearance
from destinationlane import DestinationLane
import random
from racesessionstatus import RaceSessionStatus

class RaceSession(TrackSession):

	sessionType=SessionType.race

	def __init__(self,startingPosition,score,topScore):
		self.startingScore=score
		self.startingPosition=startingPosition

		super(RaceSession, self).__init__()

		self.setTopScore(topScore)
		self.setScore(score)

		self.visualTrackSession.highlightCar(self.getPlayerCar().getVisualPeer())
		self.visualTrackSession.runRaceLightsSequence()
		self.carsPassed=0

		self.addPuddle(59,'left')
		self.addPuddle(96,'right')
		self.addPuddle(92,'left')

		self.overtakeTrackingEnabled=True
		self.carsPassed=0

	def initSession(self):

		self.sessionStatus=RaceSessionStatus.raceNotStartedStatus
		self.ticksRemaining=75*self.framesPerSecond

		keyboardDriver=KeyboardDriver()

		segmentPosition=len(self.segments)-1
		currentLane=DestinationLane.right

		aiCarAppearances=[
			CarAppearance.redAndOrange,
			CarAppearance.whiteAndRed,
			CarAppearance.yellowAndOrange,	
			CarAppearance.whiteAndGreen
		]

		aiCarAppearance=0
		currentLane=DestinationLane.right
		currentSidewaysPosition=DestinationLane.rightPosition

		for i in range(9):

			if i<8:
				if i==(self.startingPosition-1):
					newCar=self.addPlayerCar(segmentPosition,currentSidewaysPosition,0,CarAppearance.redAndOrange)
				else:
					newCar=self.addComputerCar(segmentPosition,currentSidewaysPosition,currentLane,0,aiCarAppearances[aiCarAppearance])

				newCar.setHandbrake(True)

				if currentLane==DestinationLane.right:
					currentLane=DestinationLane.left
					currentSidewaysPosition=DestinationLane.leftPosition
				else:
					currentLane=DestinationLane.right
					currentSidewaysPosition=DestinationLane.rightPosition
					segmentPosition=segmentPosition-2
					aiCarAppearance=aiCarAppearance+1

				if i==(self.startingPosition-1):
					self.setPlayerCar(newCar)
					self.setCameraCar(newCar)

			else:
				self.addRandomCar()

	def onCarCompletedLap(self,participant):
		# note that player is still allowed extended play if car passes
		# start line when time has expired (ie when car is slowing down)
		playerCar=self.getPlayerCar()
		if participant is playerCar:
			if self.getSessionStatus()==RaceSessionStatus.raceTimeExpiredStatus:
				self.setSessionStatus(RaceSessionStatus.raceInProgressStatus)
				self.getPlayerCar().setHandbrake(False)
	
			lapsCompleted=participant.getLapsCompleted()
			if lapsCompleted==3:
				self.overtakeTrackingEnabled=False
				self.scoringActive=False
				participant.setHandbrake(True)
				self.setSessionStatus(RaceSessionStatus.raceSuccessStatus)
				self.setSpeedLimit(0.25)
			else:
				self.sendPlayerLapCompletionEventToVisualTrackSession()
				if lapsCompleted==2:
					secondsToAdd=61
				else:
					secondsToAdd=50
				self.setTicksRemaining(self.getTicksRemaining()+(secondsToAdd*self.framesPerSecond))

	def onCarStopped(self,participant):
		if self.getOutcome() is None:
			sessionStatus=self.getSessionStatus()
			if sessionStatus==RaceSessionStatus.raceTimeExpiredStatus or sessionStatus==RaceSessionStatus.raceSuccessStatus:
				if sessionStatus==RaceSessionStatus.raceTimeExpiredStatus:
					self.scoringActive=False
				carsPassed=self.getCarsPassed()
				if carsPassed<0:
					carsPassed=0
				score=self.getScore()
				scoreAfterTopUp=score+carsPassed*50

				self.setScore(scoreAfterTopUp)
				self.setScore(score)
				self.visualTrackSession.displayPassingBonus(carsPassed)
				fastestLapTime=self.getFastestLapTime()
				self.setOutcome({"sessiontype":SessionType.race,
                                 "segmentposition":self.getPlayerCar().getSegmentPosition(),
                                 "sidewaysposition":self.getPlayerCar().getSidewaysPosition(),
                                 "scorebeforetopup":score,
                                 "score":scoreAfterTopUp,
                                 "topscore":self.getTopScore(),
                                 "laptimeseconds":fastestLapTime["seconds"],
                                 "laptimemilliseconds":fastestLapTime["milliseconds"],
                                 "topspeed":self.getTopSpeed()})

	def getCarsPassed(self):
		return self.carsPassed

	def setCarsPassed(self,carsPassed):
		self.carsPassed=carsPassed

	def onSessionComplete(self):
		self.closeSession()

	def onCarOvertookAnotherCar(self,overtaker,overtakee):
		# need this to calculate the passing bonus at end of race
		pass

	def onTimeExpired(self):
		self.setSessionStatus(RaceSessionStatus.raceTimeExpiredStatus)
		if self.getPlayerCar().getSpeed()>0:
			self.getPlayerCar().setHandbrake(True)
		else:
			self.onCarStopped(self.getPlayerCar())

	def advanceTime(self):
		if self.frames==240:
			self.addEvent(TrackSessionEvent.sessionStartEvent)

		super(RaceSession, self).advanceTime()


