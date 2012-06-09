from sessionlifecyclepoint import SessionLifecyclePoint

class LogicalSession(object):

	def __init__(self):
		self._sessionLifecyclePoint=SessionLifecyclePoint.initialising
		self._outcome=None

	def getSessionLifecyclePoint(self):
		return self._sessionLifecyclePoint

	def setSessionLifecyclePoint(self,sessionLifecyclePoint):
		self._sessionLifecyclePoint=sessionLifecyclePoint

	def setOutcome(self,outcome):
		self._outcome=outcome

	def getOutcome(self):
		return self._outcome

	def managedAdvanceTime(self):
		if self._sessionLifecyclePoint==SessionLifecyclePoint.running:
			self.advanceTime()

