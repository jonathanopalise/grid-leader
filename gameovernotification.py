from pandac.PandaModules import NodePath
from lettergeometry import LetterGeometry
from pandac.PandaModules import CardMaker,TransparencyAttrib
from panda3d.core import Texture

class GameOverNotification(object):

	def __init__(self,cameraX,cameraY,cameraZ,cameraAngle):
		self.ticks=0
		self.endOfLife=False
		self.currentLetterAngle=0.0
		self.letterNodes=[]
		self.distance=200
		self.closestDistance=20
		self.endOfLifeTicks=400
		self.cameraX=cameraX
		self.reduceSpinning=False
		self.spinningChange=5.0
		self.minimumSpinning=False
		self.stoppedMoving=False

		self.gameOverContainerNode=NodePath("GameOverContainer")
		self.gameOverContainerNode.reparentTo(render)
		self.gameOverContainerNode.setPos(cameraX,cameraY,cameraZ-0.85)

		self.gameOverNode=self.getGameOverNode()
		self.gameOverNode.reparentTo(self.gameOverContainerNode)

		angle=cameraAngle-90
		if angle<0.0:
			angle=angle+360.0

		self.gameOverContainerNode.setH(angle)

	def advanceTime(self):
		if self.stoppedMoving:
			self.ticksUntilDeath=self.ticksUntilDeath-1
			if self.ticksUntilDeath==0:
				self.endOfLife=True
		else:
			self.currentLetterAngle=self.currentLetterAngle+self.spinningChange
			if self.currentLetterAngle>360.0:
				if self.minimumSpinning:
					self.stoppedMoving=True
					self.ticksUntilDeath=120
				else:
					self.currentLetterAngle=self.currentLetterAngle-360.0

		if not self.reduceSpinning:
			self.distance=self.distance-1
			if self.distance<=self.closestDistance:
				self.distance=self.closestDistance
				self.reduceSpinning=True

		if self.reduceSpinning:
			if self.spinningChange>1.75:
				self.spinningChange=self.spinningChange-0.05
			else:
				self.minimumSpinning=True
			
		self.gameOverNode.setY(self.distance)
		for letterNode in self.letterNodes:
			letterNode.setH(self.currentLetterAngle)

	def getGameOverNode(self):
		gameOverNode=NodePath("GameOver")

		letterGeometry=LetterGeometry.getCardGeometryByPhrase('game over')

		for letter in letterGeometry:
			letterCm=CardMaker('card')
			letterCm.setFrame(letter['left'],letter['right'],letter['top'],letter['bottom'])
			letterNode=gameOverNode.attachNewNode(letterCm.generate())
			self.letterNodes.append(letterNode)
			letterNode.setTwoSided(True)
			letterNode.setTransparency(TransparencyAttrib.MAlpha)
			letterNode.setBin('unsorted',50)
			letterNode.setDepthTest(False)
			letterNode.setDepthWrite(False)
			tex=loader.loadTexture('textures/letter-'+letter['letter']+'.png')
			tex.setWrapU(Texture.WMClamp)
			tex.setWrapV(Texture.WMClamp)
			letterNode.setTexture(tex)
			letterNode.setPos(letter['originx'],letter['originy'],0)
	
		return gameOverNode

	def setCompletionEvent(self,completionEvent):
		self.completionEvent=completionEvent

	def getCompletionEvent(self):
		return self.completionEvent

	def hasDied(self):
		return self.endOfLife

	def delete(self):
		self.gameOverContainerNode.removeNode()

