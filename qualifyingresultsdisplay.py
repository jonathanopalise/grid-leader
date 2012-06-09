from textoverlay import TextOverlay
from colours import Colours

class QualifyingResultsDisplay(TextOverlay):	

	positionSwitchTicks=120
	bonusSwitchTicks=240
	endAnimationTicks=360

	def __init__(self):

		super(QualifyingResultsDisplay, self).__init__()

		self.cyclingColours=Colours.getCyclingColours()

		self.positionCaptionNode=self.addText('position','POSITION',10,5,1.0,1.0,1.0,self.alignRight)
		self.lapTimeCaptionNode=self.addText('laptime','LAP TIME',15,7,1.0,1.0,1.0,self.alignRight)
		self.bonusCaptionNode=self.addText('bonus','BONUS',15,3,1.0,1.0,1.0,self.alignRight)

		self.numberedPositionNodes={}
		for currentPosition in range(1,9):
			self.numberedPositionNodes[currentPosition]=self.addText('pos'+str(currentPosition),str(currentPosition),10+currentPosition*2,5,1.0,1.0,1.0,self.alignRight)

		self.lapTimeValueNode=self.addText('lapvalue','',21,7,1.0,1.0,1.0,self.alignRight)
		self.bonusValueNode=self.addText('bonusvalue','',20,3,1.0,1.0,1.0,self.alignRight)
		self.position=1

		self.endOfLife=False
		self.ticks=0

	def resetTime(self):
		self.ticks=0

	def advanceTime(self):

		if self.ticks==self.endAnimationTicks:
			self.setBonusColour(1.0,1.0,1.0)
			self.endOfLife=True
		elif self.ticks==self.bonusSwitchTicks:
			self.setPositionColour(1.0,1.0,1.0)
		elif self.ticks==self.positionSwitchTicks:
			self.setLapTimeColour(1.0,1.0,1.0)

		colourIndex=self.ticks%6
		r,g,b=self.cyclingColours[colourIndex]

		if self.ticks>=self.bonusSwitchTicks:
			self.setBonusColour(r,g,b)
		elif self.ticks>=self.positionSwitchTicks:
			self.setPositionColour(r,g,b)
		else:
			self.setLapTimeColour(r,g,b)

		self.ticks=self.ticks+1

	def setPositionValue(self,position):
		self.position=position

	def setPositionColour(self,r,g,b):
		self.positionCaptionNode.setTextColor(r,g,b,1.0)
		self.numberedPositionNodes[self.position].setTextColor(r,g,b,1.0)

	def setLapTimeValue(self,seconds,milliseconds):
		strMilliseconds=str(milliseconds)
		if len(strMilliseconds)<2:
			strMilliseconds="0"+strMilliseconds
		self.lapTimeValueNode.setText(str(seconds)+'"'+strMilliseconds)

	def setLapTimeColour(self,r,g,b):
		self.lapTimeCaptionNode.setTextColor(r,g,b,1.0)
		self.lapTimeValueNode.setTextColor(r,g,b,1.0)

	def setBonusValue(self,bonus):
		self.bonus=bonus
		self.bonusValueNode.setText(str(bonus))

	def setBonusColour(self,r,g,b):
		self.bonusCaptionNode.setTextColor(r,g,b,1.0)
		self.bonusValueNode.setTextColor(r,g,b,1.0)

	def setCompletionEvent(self,completionEvent):
		self.completionEvent=completionEvent

	def getCompletionEvent(self):
		return self.completionEvent

	def hasDied(self):
		return self.endOfLife

	
