class DisplayNodesInTurn(object):

	toggleVisibilityTicks=30

	def __init__(self,nodeList):

		self.nodeList=nodeList
		self.endOfLife=False
		self.ticks=0

	def advanceTime(self):

		self.ticks=self.ticks+1
		if self.ticks==180:
			self.endOfLife=True		

	def setCompletionEvent(self,completionEvent):
		self.completionEvent=completionEvent

	def getCompletionEvent(self):
		return self.completionEvent

	def hasDied(self):
		return self.endOfLife

	def delete(self):
		pass

	
