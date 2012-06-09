from textoverlay import TextOverlay
from colours import Colours
from soundserver import SoundServer

class ExtendedPlayNotification(TextOverlay):

	toggleVisibilityTicks=15

	def __init__(self):

		super(ExtendedPlayNotification, self).__init__()

		r,g,b=Colours.red
		self.extendedPlayCaptionNode=self.addText('extendedplay','EXTENDED PLAY!',21,18,r,g,b,self.alignRight)
		self.ticks=0	
		self.visible=False
		self.endOfLife=False

	def resetTime(self):
		self.ticks=0

	def advanceTime(self):

		if self.ticks%self.toggleVisibilityTicks==0:
			SoundServer.getInstance().playHighBeep()
			if self.visible==True:
				self.hide()
				self.visible=False
			else:
				self.show()
				self.visible=True

		self.ticks=self.ticks+1
		if self.ticks==self.toggleVisibilityTicks*10:
			self.endOfLife=True			

	def setCompletionEvent(self,completionEvent):
		self.completionEvent=completionEvent

	def getCompletionEvent(self):
		return self.completionEvent

	def hasDied(self):
		return self.endOfLife

	
