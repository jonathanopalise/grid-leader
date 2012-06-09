class NodeFlasher(object):

	toggleVisibilityTicks=15

	def __init__(self,flashingNode):

		self.flashingNode=flashingNode
		self.visible=False
		self.endOfLife=False
		self.ticks=0

	def advanceTime(self):

		if self.ticks%self.toggleVisibilityTicks==0:
			if self.visible==True:
				self.flashingNode.hide()
				self.visible=False
			else:
				self.flashingNode.show()
				self.visible=True

		self.ticks=self.ticks+1
		if self.ticks==self.toggleVisibilityTicks*13:
			self.endOfLife=True		

	def setCompletionEvent(self,completionEvent):
		self.completionEvent=completionEvent

	def getCompletionEvent(self):
		return self.completionEvent

	def hasDied(self):
		return self.endOfLife

	def delete(self):
		pass

	
