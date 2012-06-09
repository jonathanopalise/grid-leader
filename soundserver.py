class SoundServer(object):

	_instance = None

	@classmethod 
	def getInstance(cls):
		if cls._instance is None:
			cls._instance=SoundServerInternal()
		return cls._instance	

class SoundServerInternal():

	def __init__(self):
		self.engineSounds={}
		self.horn=base.loader.loadSfx("sounds/horn.wav")
		self.horn.setVolume(1.0)
		self.explosion=base.loader.loadSfx("sounds/explosion.wav")
		self.explosion.setVolume(1.0)
		self.music=base.loader.loadSfx("music/anotherretrotune.ogg")
		self.bump=base.loader.loadSfx("sounds/bump.ogg")
		self.highBeep=base.loader.loadSfx("sounds/highbeep.ogg")

	def startEngine(self,carNumber):
		if not carNumber in self.engineSounds:
			self.engineSounds[carNumber]={ "sample" : base.loader.loadSfx("sounds/f1sound1.ogg"), "playing" : False	}
			self.engineSounds[carNumber]['sample'].setLoop(True)
			#self.engineSounds[carNumber]['sample'].play()

	def stopEngine(self,carNumber):
		self.engineSounds[carNumber]['sample'].stop()

	def setEnginePitch(self,carNumber,pitch):
		self.engineSounds[carNumber]['sample'].setPlayRate(pitch)

	def setEngineBalance(self,carNumber,balance):
		self.engineSounds[carNumber]['sample'].setBalance(balance)

	def setEngineVolume(self,carNumber,volume):
		sound=self.engineSounds[carNumber]	
		if volume<0.01:
			if sound['playing']==True:
				sound['sample'].stop()
		else:
			if sound['playing']==False:
				sound['sample'].play()
				sound['sample'].setVolume(volume)

	def playLowPitchedHorn(self):
		self.horn.setPlayRate(0.5)
		self.horn.play()

	def playHighPitchedHorn(self):
		self.horn.setPlayRate(0.75)
		self.horn.play()

	def playExplosion(self):
		self.explosion.play()

	def playMusic(self):
		if not self.isMusicPlaying():
			self.music.play()

	def playBump(self):
		self.bump.play()

	def playHighBeep(self):
		self.highBeep.play()

	def stopMusic(self):
		self.music.stop()
		pass

	def isMusicPlaying(self):
		return self.music.status()==self.music.PLAYING

			
