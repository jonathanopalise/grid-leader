import random
from pandac.PandaModules import NodePath
from carsubexplosion import CarSubExplosion

class CarExplosion(object):

	def __init__(self,carNode):
		self.ticks=0
		self.endOfLife=False
		self.subExplosions=[]
		self.carNode=carNode

		self.containerNode=NodePath("CarExplosion")
		self.containerNode.reparentTo(carNode)
		self.containerNode.setPos(0.0,0.0,0.0)

		subExplosion=CarSubExplosion(
			-30,
			0.3,
			0,
			0,
			self.containerNode
        )
		self.subExplosions.append(subExplosion)
		for i in range(6):
			self.addSubExplosion()

	def addSubExplosion(self):
		subExplosion=CarSubExplosion(
			int(random.random()*40.0),
			(random.random()*0.5+0.5)*0.25,
			random.random()*0.6-0.3,
			random.random()*0.6-0.3,
			self.containerNode
        )
		self.subExplosions.append(subExplosion)

	def advanceTime(self):
		for subExplosion in self.subExplosions:
			subExplosion.advanceTime()
		self.ticks=self.ticks+1

	def isComplete(self):
		isComplete=True
		for subExplosion in self.subExplosions:
			if not subExplosion.isComplete():
				isComplete=False
		return isComplete

	def delete(self):
		self.containerNode.removeNode()
		pass


