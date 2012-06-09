from introscreentext import IntroScreenText

class VisualIntroScreenSession(object):

	def __init__(self):
		self.ticks=0

		base.setBackgroundColor(0.0, 0.0, 0.0)
		self.introScreenText=IntroScreenText()
		base.accept('aspectRatioChanged',self.correctAspectRatio)

	def advanceTime(self):
		self.ticks=self.ticks+1
		self.introScreenText.advanceTime()

	def closeSession(self):
		self.introScreenText.delete()
		
	def correctAspectRatio(self):
		width=base.win.getXSize()
		height=base.win.getYSize()
		base.camLens.setFov(50*float(width)/float(height),50)


