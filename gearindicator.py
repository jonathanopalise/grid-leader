from textoverlay import TextOverlay
from gearbox import Gearbox

class GearIndicator(TextOverlay):

	lowGear=0
	highGear=1

	def __init__(self):

		super(GearIndicator, self).__init__()
		self.gearIndicatorNode=self.addText('gearindicator','',29,2,1.0,1.0,1.0,self.alignRight)
		self.ticks=0	

	def setGear(self,gear):
		if gear==Gearbox.low:
			caption="LO"
		else:
			caption="HI"
		self.gearIndicatorNode.setText(caption)

	def advanceTime(self):
		pass
				
	def setCompletionEvent(self,completionEvent):
		self.completionEvent=completionEvent

	def getCompletionEvent(self):
		return self.completionEvent

	def hasDied(self):
		return self.endOfLife


	
