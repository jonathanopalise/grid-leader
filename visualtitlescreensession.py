from titlescreentext import TitleScreenText
from pandac.PandaModules import CardMaker,TransparencyAttrib
from panda3d.core import Texture

class VisualTitleScreenSession(object):

	def __init__(self):
		self.ticks=0

		base.setBackgroundColor(224.0/255.0, 188.0/255.0, 112.0/255.0)
		base.camera.setPos(100,100,100)
		self.correctAspectRatio()
		self.titleScreenTrack=loader.loadModel("models/titlescreentrack")
		self.titleScreenTrack.setScale(1.0)
		self.titleScreenTrack.reparentTo(render)
		self.titleScreenTrack.setPos(0.0,-10,-2.5)
		self.trackRotation=0

		self.titleScreenTitle=loader.loadModel("models/gridleader")
		self.titleScreenTitle.setScale(1.0)
		self.titleScreenTitle.setH(180.0)
		self.titleScreenTitle.reparentTo(render)
		self.titleScreenTitle.setPos(0.0,-10,0.3)

		self.titleScreenText=TitleScreenText()

		startLineCm=CardMaker('card')
		# left, right, top, bottom
		startLineCm.setFrame(0,2.25,0,0.6)
		startLineNode=self.titleScreenTrack.attachNewNode(startLineCm.generate())
		startLineNode.setTwoSided(True)
		startLineNode.setBillboardAxis()
		startLineNode.setTransparency(TransparencyAttrib.MAlpha)
		tex=loader.loadTexture('textures/titlestartline.png')
		tex.setWrapU(Texture.WMClamp)
		tex.setWrapV(Texture.WMClamp)
		startLineNode.setTexture(tex)
		startLineNode.setPos(-0.202,1.521,0)
		self.startLineNode=startLineNode

		base.accept('aspectRatioChanged',self.correctAspectRatio)

	def advanceTime(self):
		base.camera.lookAt(self.titleScreenTrack)
		self.ticks=self.ticks+1
		self.trackRotation=self.trackRotation+0.5
		self.titleScreenTrack.setH(self.trackRotation)
		self.titleScreenText.advanceTime()

	def closeSession(self):
		self.startLineNode.removeNode()
		self.titleScreenTrack.removeNode()
		self.titleScreenText.delete()
		self.titleScreenTitle.removeNode()
		
	def correctAspectRatio(self):
		width=base.win.getXSize()
		height=base.win.getYSize()
		base.camLens.setFov(50*float(width)/float(height),50)


