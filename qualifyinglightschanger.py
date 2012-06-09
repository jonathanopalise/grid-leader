from soundserver import SoundServer

class QualifyingLightsChanger(object):

	def __init__(self,visualTrackSession):
		self.visualTrackSession=visualTrackSession
		self.ticks=0
		self.currentLight=-1
		self.endOfLife=False

	def advanceTime(self):
		if self.ticks==240:
			self.visualTrackSession.setStartingLight(4,True)
			self.endOfLife=True
			SoundServer.getInstance().playHighPitchedHorn()
		self.ticks=self.ticks+1

	def hasDied(self):
		return self.endOfLife

	def setCompletionEvent(self,completionEvent):
		self.completionEvent=completionEvent

	def getCompletionEvent(self):
		return self.completionEvent

	def delete(self):
		pass



