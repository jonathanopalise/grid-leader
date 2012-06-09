from textoverlay import TextOverlay

class TitleScreenText(TextOverlay):

	ticksPerPressSpaceToggle=30
	pressSpaceCaption='PRESS SPACE'
	toPlayCaption='TO PLAY'

	def __init__(self):

		super(TitleScreenText, self).__init__()

		self.pressSpaceNode=self.addText('pressspace',self.pressSpaceCaption,28,4,0.0,0.0,0.0,self.alignRight)
		self.toPlayNode=self.addText('toplay',self.toPlayCaption,24,3,0.0,0.0,0.0,self.alignRight)

		self.hiroSpeedwayNode=self.addText('hirospeedway','HIRO SPEEDWAY',13,4,0.0,0.0,0.0,self.alignRight)
		self.oneLapNode=self.addText('1lap','1LAP 4.359km',13,3,0.0,0.0,0.0,self.alignRight)

		self.endOfLife=False
		self.ticks=0

		self.pressSpaceVisible=False
		self.ticksUntilPressSpaceToggle=self.ticksPerPressSpaceToggle

	def advanceTime(self):
		self.ticks=self.ticks+1

		self.ticksUntilPressSpaceToggle=self.ticksUntilPressSpaceToggle-1
		if self.ticksUntilPressSpaceToggle==0:
			self.ticksUntilPressSpaceToggle=self.ticksPerPressSpaceToggle
			self.setPressSpaceVisibility(self.pressSpaceVisible)
			self.pressSpaceVisible=not self.pressSpaceVisible			

	def setPressSpaceVisibility(self,visible):
		if visible:
			self.pressSpaceNode.setText(self.pressSpaceCaption)
			self.toPlayNode.setText(self.toPlayCaption)
		else:
			self.pressSpaceNode.setText('')
			self.toPlayNode.setText('')

	def setCompletionEvent(self,completionEvent):
		self.completionEvent=completionEvent

	def getCompletionEvent(self):
		return self.completionEvent

	def hasDied(self):
		return self.endOfLife

	
