from qualifyingsession import QualifyingSession
from racesession import RaceSession
from sessionlifecyclepoint import SessionLifecyclePoint
from titlescreensession import TitleScreenSession
from introscreensession import IntroScreenSession
from sessiontype import SessionType
from highscoresession import HighScoreSession
from gameoversession import GameOverSession

class SessionManager(object):

	def __init__(self):
		self.setTopScore(0)

		#self.activeSession=GameOverSession(1600,0.5,SessionType.qualifying)	
		self.activeSession=IntroScreenSession()
		#self.activeSession=RaceSession(8,43100,49200)
		#self.activeSession=HighScoreSession(700,700,200,20,20)

	def advanceSession(self):
		outcome=self.activeSession.getOutcome()
		sessionType=outcome["sessiontype"]

		if sessionType==SessionType.introScreen:
			self.activeSession=TitleScreenSession()
		if sessionType==SessionType.titleScreen:
			destination=outcome["destination"]
			if destination=="qualifying":
				self.activeSession=QualifyingSession(self.getTopScore())
			else:
				self.activeSession=HighScoreSession(0,
                                                    self.getTopScore(),
                                                    0,
                                                    0,
                                                    0,
                                                    "titlescreen")
		elif sessionType==SessionType.qualifying:
			self.setTopSpeed(outcome["topspeed"])
			self.setFastestLapTimeSeconds(outcome["laptimeseconds"])
			self.setFastestLapTimeMilliseconds(outcome["laptimemilliseconds"])
			if outcome["topscore"]>self.getTopScore():
				self.setTopScore(outcome["topscore"])
			if outcome["qualified"]:
				self.activeSession=RaceSession(outcome["position"],outcome["score"],self.getTopScore())
			else:
				self.activeSession=HighScoreSession(outcome["score"],
                                                    self.getTopScore(),
                                                    self.getTopSpeed(),
                                                    outcome["laptimeseconds"],
                                                    outcome["laptimemilliseconds"],
                                                    "qualifying")
				self.setSegmentPosition(outcome["segmentposition"])
				self.setSidewaysPosition(outcome["sidewaysposition"])
		elif sessionType==SessionType.race:
			self.setTopSpeed(outcome["topspeed"])
			self.setFastestLapTimeSeconds(outcome["laptimeseconds"])
			self.setFastestLapTimeMilliseconds(outcome["laptimemilliseconds"])
			if outcome["topscore"]>self.getTopScore():
				self.setTopScore(outcome["topscore"])
			self.activeSession=HighScoreSession(outcome["score"],
                                                self.getTopScore(),
                                                outcome["topspeed"],
                                                outcome["laptimeseconds"],
                                                outcome["laptimemilliseconds"],
                                                "race")
			self.setSegmentPosition(outcome["segmentposition"])
			self.setSidewaysPosition(outcome["sidewaysposition"])
		elif sessionType==SessionType.highScoreTable:
			destination=outcome["destination"]
			if destination=="titlescreen":
				self.activeSession=TitleScreenSession()
			else:
				self.activeSession=GameOverSession(self.getSegmentPosition(),
                                                   self.getSidewaysPosition(),
                                                   SessionType.qualifying,
                                                   self.getTopScore(),
                                                   outcome["score"],
                                                   self.getTopSpeed(),
                                                   self.getFastestLapTimeSeconds(),
                                                   self.getFastestLapTimeMilliseconds())
		elif sessionType==SessionType.gameOver:
			self.activeSession=TitleScreenSession()

	def advanceTime(self):
		status=self.activeSession.getSessionLifecyclePoint()
		if status==SessionLifecyclePoint.closed:
			self.advanceSession()
		else:
			self.activeSession.managedAdvanceTime()

	def setSegmentPosition(self,segmentPosition):
		self.segmentPosition=segmentPosition	

	def getSegmentPosition(self):
		return self.segmentPosition

	def setSidewaysPosition(self,sidewaysPosition):
		self.sidewaysPosition=sidewaysPosition	

	def getSidewaysPosition(self):
		return self.sidewaysPosition

	def getTopScore(self):
		return self.topScore

	def setTopScore(self,topScore):
		self.topScore=topScore

	def getTopSpeed(self):
		return self.topSpeed

	def setTopSpeed(self,topSpeed):
		self.topSpeed=topSpeed

	def getFastestLapTimeSeconds(self):
		return self.fastestLapTimeSeconds

	def setFastestLapTimeSeconds(self,fastestLapTimeSeconds):
		self.fastestLapTimeSeconds=fastestLapTimeSeconds

	def getFastestLapTimeMilliseconds(self):
		return self.fastestLapTimeMilliseconds

	def setFastestLapTimeMilliseconds(self,fastestLapTimeMilliseconds):
		self.fastestLapTimeMilliseconds=fastestLapTimeMilliseconds

