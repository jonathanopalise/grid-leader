from soundserver import SoundServer

class RaceLightsChanger(object):

	def __init__(self,visualTrackSession):
		self.visualTrackSession=visualTrackSession
		self.ticks=0
		self.currentLight=-1
		self.endOfLife=False

	def advanceTime(self):
		if self.ticks%60==0:
			self.currentLight=self.currentLight+1
			if self.currentLight>0:
				if self.currentLight>1:
					self.visualTrackSession.setStartingLight(self.currentLight-1,False)
				self.visualTrackSession.setStartingLight(self.currentLight,True)
				if self.currentLight==4:
					SoundServer.getInstance().playLowPitchedHorn()
					self.endOfLife=True
				else:
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



