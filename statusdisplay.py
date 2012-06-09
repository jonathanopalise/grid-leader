from textoverlay import TextOverlay

class StatusDisplay(TextOverlay):

	def __init__(self):

		super(StatusDisplay, self).__init__()

		self.ignoreLapTimeAndSpeedUpdates=False
		self.ticksToIgnoreLapTimeAndSpeedUpdates=0
		self.ticksToToggleLapTimeAndSpeedVisibility=0

		self.addText('timecaption','TIME',16,26,1.0,1.0,0.4375,self.alignRight)
		self.addText('lapcaption','LAP',23,26,143.0/255,255.0/255.0,112.0/255,self.alignRight)
		self.addText('speedcaption','SPEED',23,24,1.0,1.0,1.0,self.alignRight)
		self.addText('scorecaption','SCORE',4,24,1.0,1.0,1.0,self.alignRight)
		self.addText('topscorecaption','TOP',4,26,255.0/255,143.0/255,174.0/255,self.alignRight)

		self.timeValue=self.addText('timevalue','00',15,24,1.0,1.0,0.4375,self.alignRight)
		self.lapValue=self.addText('lapvalue','',29,26,143.0/255,255.0/255.0,112.0/255,self.alignRight)
		self.speedValue=self.addText('speedvalue','0km',29,24,1.0,1.0,1.0,self.alignRight)
		self.scoreValue=self.addText('scorevalue','0',10,24,1.0,1.0,1.0,self.alignRight)
		self.topScoreValue=self.addText('topscorevalue','0',10,26,255.0/255,143.0/255,174.0/255,self.alignRight)

	def setScore(self,score):
		self.scoreValue.setText(str(score))
		pass

	def setTopScore(self,topScore):
		self.topScoreValue.setText(str(topScore))
		pass

	def setSecondsRemaining(self,secondsRemaining):
		self.timeValue.setText(str(secondsRemaining))
		pass

	def setLapTime(self,seconds,milliseconds):
		if not self.ignoreLapTimeAndSpeedUpdates:
			strMilliseconds=str(milliseconds)
			if len(strMilliseconds)<2:
				strMilliseconds="0"+strMilliseconds
			self.lapValue.setText(str(seconds)+'"'+strMilliseconds)

	def setSpeed(self,speed):
		if not self.ignoreLapTimeAndSpeedUpdates:
			self.speedValue.setText(str(speed))

	def flashLapTimeAndTopSpeed(self,lapTimeSeconds,lapTimeMilliseconds,topSpeed):
		self.setLapTime(lapTimeSeconds,lapTimeMilliseconds)
		self.setSpeed(str(topSpeed)+"km")
		self.ignoreLapTimeAndSpeedUpdates=True
		self.lapTimeAndSpeedVisibility=False
		self.ticksToToggleLapTimeAndSpeedVisibility=0
		self.flashingLapText=self.lapValue.getText()
		self.flashingSpeedText=self.speedValue.getText()
		self.ticksToIgnoreLapTimeAndSpeedUpdates=255
		
	def advanceTime(self):
		if self.ticksToIgnoreLapTimeAndSpeedUpdates>0:
			if self.ticksToToggleLapTimeAndSpeedVisibility==0:
				self.ticksToToggleLapTimeAndSpeedVisibility=15
				self.lapTimeAndSpeedVisibility=not self.lapTimeAndSpeedVisibility
				if self.lapTimeAndSpeedVisibility:
					self.lapValue.setText(self.flashingLapText)
					self.speedValue.setText(self.flashingSpeedText)
				else:
					self.lapValue.setText('')
					self.speedValue.setText('')

			self.ticksToIgnoreLapTimeAndSpeedUpdates=self.ticksToIgnoreLapTimeAndSpeedUpdates-1
			self.ticksToToggleLapTimeAndSpeedVisibility=self.ticksToToggleLapTimeAndSpeedVisibility-1

			if self.ticksToIgnoreLapTimeAndSpeedUpdates==0:
				self.ignoreLapTimeAndSpeedUpdates=False

	
