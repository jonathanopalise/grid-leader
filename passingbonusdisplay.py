from textoverlay import TextOverlay
from colours import Colours
from soundserver import SoundServer

class PassingBonusDisplay(TextOverlay):

	ticksPerCountdownNumber=7

	def __init__(self,visualTrackSession,carsPassed):

		super(PassingBonusDisplay, self).__init__()

		self.cyclingColours=Colours.getCyclingColours()

		self.passingBonusCaptionNode=self.addText('passingbonus','PASSING BONUS',16,3,1.0,1.0,1.0,self.alignRight)
		self.passingBonusValueNode=self.addText('passingbonusvalue','',24,3,1.0,1.0,1.0,self.alignRight)

		self.endOfLife=False
		self.ticks=0

		self.visualTrackSession=visualTrackSession
		self.startCountdownNumber=carsPassed

	def resetTime(self):
		self.ticks=0

	def advanceTime(self):

		colourIndex=self.ticks%6
		r,g,b=self.cyclingColours[colourIndex]
		self.setPassingBonusColour(r,g,b)

		if self.ticksUntilNextCountdownNumberChange==0:
			if self.currentCountdownNumber==0:
				self.endOfLife=True
			else:
				SoundServer.getInstance().playHighBeep()
				self.currentCountdownNumber=self.currentCountdownNumber-1
				self.ticksUntilNextCountdownNumberChange=self.ticksPerCountdownNumber
				self.setPassingBonusValue('50x'+str(self.currentCountdownNumber))
				self.visualTrackSession.addEvent(self.visualTrackSession.passingBonusScoreUpdateEvent,
                                                 {"currentcountdownnumber":self.currentCountdownNumber,
                                                  "startcountdownnumber":self.startCountdownNumber})

		self.ticks=self.ticks+1
		self.ticksUntilNextCountdownNumberChange=self.ticksUntilNextCountdownNumberChange-1

	def setCarsPassed(self,carsPassed):
		self.ticksUntilNextCountdownNumberChange=self.ticksPerCountdownNumber
		self.currentCountdownNumber=carsPassed

	def setPassingBonusColour(self,r,g,b):
		self.passingBonusCaptionNode.setTextColor(r,g,b,1.0)
		self.passingBonusValueNode.setTextColor(r,g,b,1.0)

	def setPassingBonusValue(self,passingBonus):
		self.passingBonus=passingBonus
		self.passingBonusValueNode.setText(str(passingBonus))

	def setCompletionEvent(self,completionEvent):
		self.completionEvent=completionEvent

	def getCompletionEvent(self):
		return self.completionEvent

	def hasDied(self):
		return self.endOfLife

	
