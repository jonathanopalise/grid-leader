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

class GameOverSession(TrackSession):

	sessionType=SessionType.gameOver

	def __init__(self,segmentPosition,sidewaysPosition,previousSessionType,topScore,score,topSpeed,fastestLapTimeSeconds,fastestLapTimeMilliseconds):
		self.segmentPosition=segmentPosition
		self.sidewaysPosition=sidewaysPosition
		self.gameOverDisplayed=False

		super(GameOverSession, self).__init__()

		self.setTopScore(topScore)
		self.setScore(score)
		self.visualTrackSession.setLapTime(fastestLapTimeSeconds,fastestLapTimeMilliseconds)
		self.setSpeed(topSpeed)

	def initSession(self):
		self.ticksRemaining=0
		for i in range(3):
			if i==0:
				newCar=self.addNullCar(self.segmentPosition,self.sidewaysPosition)
				self.setCameraCar(newCar)
			else:
				computerCar=self.addRandomCar()
		self.setOutcome({"sessiontype":SessionType.gameOver})

	def advanceTime(self):
		super(GameOverSession, self).advanceTime()

		if not self.gameOverDisplayed:
			self.visualTrackSession.displayGameOverNotification()
			self.gameOverDisplayed=True
	
	def onCarStopped(self,participant):
		pass
	




