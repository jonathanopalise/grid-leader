from visualintroscreensession import VisualIntroScreenSession
from logicalsession import LogicalSession
from sessionlifecyclepoint import SessionLifecyclePoint
from sessiontype import SessionType

class IntroScreenSession(LogicalSession):

	def __init__(self):
		self.setSessionLifecyclePoint(SessionLifecyclePoint.initialising)
		self.visualSession=VisualIntroScreenSession()
		self.setSessionLifecyclePoint(SessionLifecyclePoint.running)
		self.ticks=0

	def advanceTime(self):

		self.visualSession.advanceTime()
		self.ticks=self.ticks+1

		if self.ticks==10*60:
			self.closeSession()

	def getDestination(self):
		return self.destination

	def setDestination(self,destination):
		self.destination=destination

	def closeSession(self):
		self.setOutcome({"sessiontype":SessionType.introScreen})
		self.setSessionLifecyclePoint(SessionLifecyclePoint.closing)
		self.visualSession.closeSession()
		self.setSessionLifecyclePoint(SessionLifecyclePoint.closed)
