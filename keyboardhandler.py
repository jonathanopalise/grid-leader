from direct.showbase import DirectObject
from driverinterface import DriverInterface
import sys

class KeyboardHandler(object):

	_instance = None

	@classmethod 
	def getInstance(cls):
		if cls._instance is None:
			cls._instance=KeyboardHandlerInternal()
		return cls._instance	

class KeyboardHandlerInternal(DirectObject.DirectObject):

	def __init__(self):

		self.keyMap = {"accelerate":0, "brake":0, "left":0, "right":0, "space":0, "p":0}

		self.accept("arrow_up", self.setKey, ["accelerate",1])
		self.accept("arrow_down", self.setKey, ["brake",1])
		self.accept("arrow_up-up", self.setKey, ["accelerate",0])
		self.accept("arrow_down-up", self.setKey, ["brake",0])

		self.accept("arrow_left", self.setKey, ["left",1])
		self.accept("arrow_right", self.setKey, ["right",1])
		self.accept("arrow_left-up", self.setKey, ["left",0])
		self.accept("arrow_right-up", self.setKey, ["right",0])

		self.accept("space", self.setKey, ["space",1])

		self.accept("p", self.setKey, ["p",1])
		self.accept("escape", sys.exit)

	def setKey(self, key, value):
		self.keyMap[key] = value

	def getUpArrowStatus(self):
		return self.keyMap["accelerate"]

	def getDownArrowStatus(self):
		return self.keyMap["brake"]

	def getRightArrowStatus(self):
		return self.keyMap["right"]

	def getLeftArrowStatus(self):
		return self.keyMap["left"]

	def getSpaceStatus(self):
		return self.keyMap["space"]

	def clearSpaceStatus(self):
		self.keyMap["space"]=0

	def getPStatus(self):
		return self.keyMap["p"]

	def clearPStatus(self):
		self.keyMap["p"]=0
	
