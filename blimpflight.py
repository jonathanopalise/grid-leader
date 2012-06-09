from pandac.PandaModules import NodePath
from panda3d.core import Texture
from pandac.PandaModules import TransparencyAttrib

class BlimpFlight(object):

	def __init__(self,originX,originY,textureFilename):
		self.ticks=0
		self.endOfLife=False
		self.blimpSpeed=0.20
		self.blimpYEnd=40
		self.blimpYStart=-40
		self.blimpY=self.blimpYStart

		self.originY=originY
		self.originX=originX
		
		m = loader.loadModel("models/blimp")
		m.reparentTo(render)
		m.setPos(originX,originY+self.blimpY,8)
		m.setH(180)
		m.setTransparency(TransparencyAttrib.MAlpha)

		n=m.find("**/Banner")
		t=loader.loadTexture("models/"+textureFilename+".png")
		t.setMinfilter(Texture.FTLinearMipmapLinear)
		n.setTexture(t,1)

		self.blimpNode=m

	def advanceTime(self):

		self.blimpY=self.blimpY+self.blimpSpeed
		self.blimpNode.setY(self.originY+self.blimpY)
		transparency=1.0

		if self.blimpY<self.blimpYStart+5:
			transparency=(self.blimpY-self.blimpYStart)/5.0

		if self.blimpY>self.blimpYEnd-5:
			transparency=(self.blimpYEnd-self.blimpY)/5.0

		self.blimpNode.setAlphaScale(transparency)

		if self.blimpY>self.blimpYEnd:
			self.endOfLife=True

	def setCompletionEvent(self,completionEvent):
		self.completionEvent=completionEvent

	def getCompletionEvent(self):
		return self.completionEvent

	def hasDied(self):
		return self.endOfLife

	def delete(self):
		self.blimpNode.removeNode()

