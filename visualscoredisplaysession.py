from statusdisplay import StatusDisplay

class VisualScoreDisplaySession(object):

	def __init__(self):
		self.statusDisplay=StatusDisplay()
		self.topScore=-1
		self.lapTimeSeconds=-1
		self.lapTimeMilliseconds=-1
		self.speed=-1

	def setScore(self,score):
		self.statusDisplay.setScore(score)

	def setTopScore(self,topScore):
		if topScore!=self.topScore:
			self.topScore=topScore
			self.statusDisplay.setTopScore(topScore)

	def setSecondsRemaining(self,secondsRemaining):
		if secondsRemaining!=self.secondsRemaining:
			self.secondsRemaining=secondsRemaining
			self.statusDisplay.setSecondsRemaining(secondsRemaining)

	def setLapTime(self,seconds,milliseconds):
		if milliseconds!=self.lapTimeMilliseconds or seconds!=self.lapTimeSeconds:
			self.lapTimeMilliseconds=milliseconds
			self.lapTimeSeconds=seconds
			self.statusDisplay.setLapTime(seconds,milliseconds)

	def setSpeed(self,speed):
		if speed!=self.speed:
			self.speed=speed
			self.statusDisplay.setSpeed(str(speed)+"km")

	def onLapCompleted(lapTime,topSpeed,lapsCompleted):
		if lapsCompleted>0:
			self.statusDisplay.flashLapTimeAndTopSpeed(lapTime,topSpeed)

	def closeSession(self):
		self.statusDisplay.delete()

