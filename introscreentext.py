from textoverlay import TextOverlay

class IntroScreenText(TextOverlay):

	def __init__(self):

		super(IntroScreenText, self).__init__()

		self.hiroSpeedwayNode=self.addText('line1','GRID LEADER',0,26,1.0,1.0,1.0,self.alignLeft)
		self.hiroSpeedwayNode=self.addText('line1','PUBLIC BETA 2 [6/1/2011]',0,25,1.0,1.0,1.0,self.alignLeft)

		self.hiroSpeedwayNode=self.addText('line2','CONTROLS:',0,22,1.0,1.0,1.0,self.alignLeft)
		self.hiroSpeedwayNode=self.addText('line2','UP ARROW: ACCELERATE',0,21,0.7,0.7,0.7,self.alignLeft)
		self.hiroSpeedwayNode=self.addText('line2','DOWN ARROW: BRAKE',0,20,0.7,0.7,0.7,self.alignLeft)	
		self.hiroSpeedwayNode=self.addText('line2','LEFT ARROW: STEER LEFT',0,19,0.7,0.7,0.7,self.alignLeft)
		self.hiroSpeedwayNode=self.addText('line2','RIGHT ARROW: STEER RIGHT',0,18,0.7,0.7,0.7,self.alignLeft)
		self.hiroSpeedwayNode=self.addText('line2','SPACE: CHANGE GEAR',0,17,0.7,0.7,0.7,self.alignLeft)
		self.hiroSpeedwayNode=self.addText('line2','ESC: QUIT',0,16,0.7,0.7,0.7,self.alignLeft)

		self.hiroSpeedwayNode=self.addText('line2','CREDITS:',0,14,1.0,1.0,1.0,self.alignLeft)
		self.hiroSpeedwayNode=self.addText('line2','CODE/GFX/SFX:',0,13,0.7,0.7,0.7,self.alignLeft)
		self.hiroSpeedwayNode=self.addText('line2','CHICANE',0,12,0.7,0.7,0.7,self.alignLeft)
		self.hiroSpeedwayNode=self.addText('line2','(TWITTER: RETRORACING)',0,11,0.7,0.7,0.7,self.alignLeft)

		self.hiroSpeedwayNode=self.addText('line2','MUSIC:',0,9,0.7,0.7,0.7,self.alignLeft)
		self.hiroSpeedwayNode=self.addText('line2','MR.LOU/DEWFALL PRODUCTIONS',0,8,0.7,0.7,0.7,self.alignLeft)

		self.hiroSpeedwayNode=self.addText('line2','FONT (PRESS START K):',0,6,0.7,0.7,0.7,self.alignLeft)
		self.hiroSpeedwayNode=self.addText('line2','CODEMAN38',0,5,0.7,0.7,0.7,self.alignLeft)

		self.hiroSpeedwayNode=self.addText('line2','FMOD SOUND SYSTEM',0,3,0.7,0.7,0.7,self.alignLeft)
		self.hiroSpeedwayNode=self.addText('line2','FIRELIGHT TECHNOLOGIES',0,2,0.7,0.7,0.7,self.alignLeft)

		self.endOfLife=False
		self.ticks=0

	def advanceTime(self):
		self.ticks=self.ticks+1

	def setCompletionEvent(self,completionEvent):
		self.completionEvent=completionEvent

	def getCompletionEvent(self):
		return self.completionEvent

	def hasDied(self):
		return self.endOfLife

	
