from carexplosion import CarExplosion

class VisualCarRepresentation(object):

	def __init__(self,visualPeer,bob,visualShadowPeer):
		self.visualPeer=visualPeer
		self.bob=bob
		self.visualShadowPeer=visualShadowPeer
		self.explosion=None

	def getVisualPeer(self):
		return self.visualPeer

	def getVisualShadowPeer(self):
		return self.visualShadowPeer

	def setPos(self,x,y,z):
		self.getVisualPeer().setPos(x,y,z)
		self.bob.setModelPos(x,y,z)
		self.getVisualShadowPeer().setPos(x,y,z)

	def setH(self,h):
		self.getVisualPeer().setH(h)
		self.bob.setModelRotation(h)

	def refreshShadow(self):
		self.bob.projectVerticesToShadow()

	def show(self):
		self.visualPeer.show()
		self.visualShadowPeer.show()

	def hide(self):
		self.visualPeer.hide()
		self.visualShadowPeer.hide()

	def startExplodingAnimation(self):
		self.explosion=CarExplosion(self.visualPeer)

	def isExplosionActive(self):
		return self.explosion is not None

	def updateExplodingAnimation(self):
		if self.explosion is not None:
			self.explosion.advanceTime()
			if self.explosion.isComplete():
				self.explosion.delete()
				self.explosion=None

	def stopExplodingAnimation(self):
		self.explosion=None
		#self.p.cleanup()

	def advanceTime(self):
		self.updateExplodingAnimation()
