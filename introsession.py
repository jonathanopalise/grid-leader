from visualtitlescreensession import VisualTitleScreenSession
from logicalsession import LogicalSession
from sessionlifecyclepoint import SessionLifecyclePoint
from sessiontype import SessionType
from keyboardhandler import KeyboardHandler
from soundserver import SoundServer

class TitleScreenSession(LogicalSession):

	def __init__(self):
		self.setSessionLifecyclePoint(SessionLifecyclePoint.initialising)
		self.visualSession=VisualTitleScreenSession()
		self.setSessionLifecyclePoint(SessionLifecyclePoint.running)
		self.ticks=0
		self.keyboardHandler=KeyboardHandler.getInstance()

		soundServer=SoundServer.getInstance()

		if not soundServer.isMusicPlaying():
			soundServer.playMusic()

	def advanceTime(self):

		self.visualSession.advanceTime()
		self.ticks=self.ticks+1

		if self.ticks==10*60:
			self.setDestination("highscores")
			self.closeSession()
		else:
			space=self.keyboardHandler.getSpaceStatus()
			if space==1:
				SoundServer.getInstance().stopMusic()
				self.setDestination("qualifying")
				self.keyboardHandler.clearSpaceStatus()
				self.closeSession()

	def getDestination(self):
		return self.destination

	def setDestination(self,destination):
		self.destination=destination

	def closeSession(self):
		self.setOutcome({"sessiontype":SessionType.titleScreen,"destination":self.getDestination()})
		self.setSessionLifecyclePoint(SessionLifecyclePoint.closing)
		self.visualSession.closeSession()
		self.setSessionLifecyclePoint(SessionLifecyclePoint.closed)
