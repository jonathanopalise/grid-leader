import math
from pandac.PandaModules import TransparencyAttrib

class CarSubExplosion(object):

	def __init__(self,startTicks,scale,xpos,ypos,parent):
		self.ticks=0
		self.startTicks=startTicks
		self.scale=scale
		self.visible=False
		self.complete=False

		m = loader.loadModel("models/explosion")
		m.reparentTo(parent)
		m.setPos(xpos,ypos,0)
		m.setTransparency(TransparencyAttrib.MAlpha)
		m.reparentTo(parent)
		self.peer=m
		self.peer.hide()

	def isComplete(self):
		return self.complete

	def advanceTime(self):
		self.ticks=self.ticks+1

		oldVisible=self.visible
		if self.ticks>=self.startTicks and self.ticks<self.startTicks+180:
			newVisible=True
		else:
			newVisible=False
		self.visible=newVisible

		animationStage=0
		if newVisible!=oldVisible:
			if newVisible==True:
				self.peer.show()
			else:
				self.peer.hide()

		if (self.ticks-self.startTicks)>180:
			self.complete=True

		if newVisible==True:
			animationStage=(self.ticks-self.startTicks)/57.29
			self.peer.setScale(math.sin(animationStage)*self.scale)
			self.peer.setAlphaScale(math.sin(animationStage))

