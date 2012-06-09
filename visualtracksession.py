from panda3d.core import TextNode
from statusdisplay import StatusDisplay
from qualifyingresultsdisplay import QualifyingResultsDisplay
import TrackVisualGeometry
from mountainsgeometry import MountainsGeometry
from panda3d.core import Texture, GeomNode
from panda3d.core import Geom, GeomTriangles, GeomVertexWriter, GeomVertexReader, GeomVertexRewriter
from tracksessionevent import TrackSessionEvent
from extendedplaynotification import ExtendedPlayNotification
from nodeflasher import NodeFlasher
from displaynodesinturn import DisplayNodesInTurn
from factory import Factory
from passingbonusdisplay import PassingBonusDisplay
from visualcarrepresentation import VisualCarRepresentation
from racelightschanger import RaceLightsChanger
from qualifyinglightschanger import QualifyingLightsChanger
from shadowgeometry import ShadowGeometry
from pandac.PandaModules import StencilAttrib,ColorWriteAttrib,CardMaker,TransparencyAttrib
from timeofday import TimeOfDay
from gameovernotification import GameOverNotification
from visualscoredisplaysession import VisualScoreDisplaySession
from pandac.PandaModules import Fog
from blimpflight import BlimpFlight
from gearindicator import GearIndicator
import math
from gearbox import Gearbox

class VisualTrackSession(VisualScoreDisplaySession):

	sessionOverEvent=0
	sessionStartEvent=1
	playerCarPassedStartLineEvent=2
	greenLightEvent=3
	qualifyingStartBlimpFlightCompleteEvent=4
	qualifyingEndBlimpFlightCompleteEvent=5
	qualifyingResultsDisplayCompleteEvent=6
	passingBonusScoreUpdateEvent=7

	playerCar=None
	extendedPlayNotificationEnabled=True

	def __init__(self,parent,segments,timeOfDay):

		super(VisualTrackSession, self).__init__()

		self.parent=parent
		self.ticks=0
		self.cars=[]
		self.events=[]
		self.timerDependentObjects=[]
		self.segments=segments
		self.createdNodes=[]
		self.stencilReaders={}
		self.stencilWriters={}
		self.carShadowRefreshIndex=0

		self.speed=-1
		self.lapTimeSeconds=-1
		self.lapTimeMilliseconds=-1
		self.secondsRemaining=-1
		self.topScore=-1

		self.correctAspectRatio()
		base.setBackgroundColor(0.262,0.615,0.054)
		base.accept('aspectRatioChanged',self.correctAspectRatio )

		self.carsAndSceneryNode=render.attachNewNode("CarsAndSceneryNode")
		self.carsAndSceneryNode.setColorScale(1.0,1.0,1.0,1.0)

		self.sunEffectsEnabled=False
		if timeOfDay==TimeOfDay.dusk:
			self.setBackgroundTexture('textures/mountains4x2blurredblended.png')
			self.setLightSourcePosition([12000,-800,1200])
			self.addSunEffects()
		else:
			self.setBackgroundTexture('textures/mountainsx2blurredblended.png')
			self.setLightSourcePosition([-4000,-1800,2400])

		m = loader.loadModel("models/newstartline")
		m.reparentTo(self.carsAndSceneryNode)
		m.setPos(self.segments[0].getMidPoint().getX(),self.segments[0].getMidPoint().getY(),0)
		m.setH(270)
		self.lights=m
		self.lightsIlluminated=False
		for i in range(1,5):
			self.setStartingLight(i,False)
		self.createdNodes.append(m)

		trackGeomNodes=TrackVisualGeometry.makeTrack(self.segments)

		track=render.attachNewNode(trackGeomNodes['tarmac'])
		texture=loader.loadTexture("textures/track256.png")
		texture.setAnisotropicDegree(4)
		texture.setMagfilter(Texture.FTNearest)
		texture.setMinfilter(Texture.FTLinearMipmapLinear)
		texture.setWrapU(Texture.WMRepeat)
		texture.setWrapV(Texture.WMRepeat)
		track.setTexture(texture)
		track.setTwoSided(False)
		track.setDepthWrite(False)
		track.setDepthTest(False)
		track.setBin("background",10)
		self.createdNodes.append(track)

		constantTwoStencil = StencilAttrib.make(1,StencilAttrib.SCFEqual,StencilAttrib.SOZero,StencilAttrib.SOKeep,StencilAttrib.SOReplace,2,0,2)
		track.node().setAttrib(constantTwoStencil)

		startLine=render.attachNewNode(trackGeomNodes['startline'])
		texture=loader.loadTexture("textures/startline.png")
		texture.setAnisotropicDegree(4)
		texture.setMagfilter(Texture.FTNearest)
		texture.setMinfilter(Texture.FTLinearMipmapLinear)
		texture.setWrapU(Texture.WMRepeat)	
		texture.setWrapV(Texture.WMRepeat)
		startLine.setTexture(texture)
		startLine.setTwoSided(False)
		startLine.setDepthWrite(False)
		startLine.setDepthTest(False)
		startLine.setBin("background",11);
		self.createdNodes.append(startLine)

		backgroundGeomNodes=MountainsGeometry.makeMountains()

		mountainsGeomNode=backgroundGeomNodes['mountains']
		mountains=render.attachNewNode(mountainsGeomNode)
		texture=loader.loadTexture(self.getBackgroundTexture())
		texture.setAnisotropicDegree(4)
		texture.setWrapU(Texture.WMRepeat)	
		texture.setWrapV(Texture.WMClamp)
		mountains.setTexture(texture)
		mountains.setTwoSided(False)
		mountains.setDepthWrite(False)
		mountains.setDepthTest(False)
		mountains.setBin("background",10);
		self.createdNodes.append(mountains)

		skyGeomNode=backgroundGeomNodes['sky']
		sky=render.attachNewNode(skyGeomNode)
		sky.setDepthWrite(False)
		sky.setDepthTest(False)
		sky.setBin("background",11)
		self.createdNodes.append(sky)

		constantOneStencil = StencilAttrib.make(1,StencilAttrib.SCFEqual,StencilAttrib.SOZero,StencilAttrib.SOKeep,StencilAttrib.SOReplace,1,0,1)
		shadowX=self.segments[0].getMidPoint().getX()
		shadowY=self.segments[0].getMidPoint().getY()
		lightSourceX,lightSourceY,lightSourceZ=self.getLightSourcePosition()
		shadowGeomNode=ShadowGeometry.makeModelShadow("models/newstartlineshadow",shadowX,shadowY,0,lightSourceX,lightSourceY,lightSourceZ,270)
		shadow=render.attachNewNode(shadowGeomNode)
		shadow.setTwoSided(True)
		self.createdNodes.append(shadow)
		shadow.setPos(shadowX,shadowY,0)
		shadow.node().setAttrib(constantOneStencil)
		shadow.node().setAttrib(ColorWriteAttrib.make(0))
		shadow.setBin('fixed',40)
		shadow.setDepthWrite(0)
		self.createdNodes.append(shadow)

		stencilReader = StencilAttrib.make(1,StencilAttrib.SCFEqual,StencilAttrib.SOKeep, StencilAttrib.SOKeep,StencilAttrib.SOKeep,1,1,0) 
		cm2d = CardMaker('card')
		cm2d.setFrameFullscreenQuad()
		card = render2d.attachNewNode(cm2d.generate())
		card.node().setAttrib(stencilReader)
		card.setDepthTest(False)
		card.setTransparency(TransparencyAttrib.MAlpha)
		card.setColor(0,0,0,0.40)
		self.createdNodes.append(card)

		trafficLightCm=CardMaker('card')
		trafficLightCm.setFrame(-0.20,0.20,0.20,-0.20)
		trafficLight = render.attachNewNode(trafficLightCm.generate())
		trafficLight.reparentTo(self.lights)
		trafficLight.setDepthTest(True)
		trafficLight.setDepthWrite(False)
		trafficLight.setColor(1.0,0.0,0.0,1.0)
		trafficLight.setBin("unsorted",50)
		trafficLight.setBillboardAxis()
		trafficLight.setTwoSided(True)
		tex = loader.loadTexture('textures/roadhighlight.png')
		trafficLight.setTexture(tex)
		trafficLight.setTransparency(TransparencyAttrib.MAlpha)
		trafficLight.hide()
		self.trafficLight=trafficLight
		self.createdNodes.append(trafficLight)

		colour = (45.0/255.0,81.0/255.0,98.0/255.0)
		expfog = Fog("Scene-wide exponential Fog object")
		expfog.setColor(*colour)
		expfog.setExpDensity(0.002)
		self.carsAndSceneryNode.setFog(expfog)

		self.qualifyingEndBlimpFlightComplete=False
		self.qualifyingResultsDisplayComplete=False	

		self.gearIndicator=GearIndicator()
		self.gearIndicator.setGear(Gearbox.low)

	def runBlimpFlight(self,carSegment,endOfQualifying):
		if endOfQualifying:
			textureFilename='preparerace'
			completionEvent=self.qualifyingEndBlimpFlightCompleteEvent
		else:
			textureFilename='preparequalify'
			completionEvent=self.qualifyingStartBlimpFlightCompleteEvent

		blimpSegment=int(math.floor(carSegment))+55
		if blimpSegment>len(self.segments):
			blimpSegment=blimpSegment-len(self.segments)

		blimpFlight=BlimpFlight(self.segments[blimpSegment].getMidPoint().getX(),self.segments[blimpSegment].getMidPoint().getY(),textureFilename)
		blimpFlight.setCompletionEvent(completionEvent)
		self.addTimerDependentObject(blimpFlight)

	def addSunEffects(self):
		self.sunEffectsEnabled=True

		dazzlerCm = CardMaker('card')
		dazzlerCm.setFrameFullscreenQuad()
		self.dazzler = render2d.attachNewNode(dazzlerCm.generate())
		self.dazzler.setDepthTest(False)
		self.dazzler.setTransparency(TransparencyAttrib.MAlpha)
		self.dazzler.setColor(1.0,1.0,1.0,0.0)
		self.dazzler.setBin("fixed",40)
		self.createdNodes.append(self.dazzler)

		sunCm=CardMaker('card')
		sunCm.setFrame(-500,500,500,-500)
		sun = render.attachNewNode(sunCm.generate())
		sun.setDepthTest(True)
		sun.setDepthWrite(False)
		sun.setColor(1.0,0.8,0.4,1.0)
		sun.setBin("unsorted",50)
		sunX,sunY,sunZ=self.getLightSourcePosition()
		sun.setPos(sunX,sunY,sunZ)
		sun.setBillboardAxis()
		sun.setTwoSided(True)
		tex = loader.loadTexture('textures/sun.png')
		sun.setTexture(tex)
		sun.setTransparency(TransparencyAttrib.MAlpha)
		self.createdNodes.append(sun)

		sunSurroundCm=CardMaker('card')
		sunSurroundCm.setFrame(-1500,1500,1500,-1500)
		sunSurround = render.attachNewNode(sunSurroundCm.generate())
		sunSurround.setDepthTest(True)
		sunSurround.setDepthWrite(False)
		sunSurround.setColor(1.0,1.0,1.0,1.0)
		sunSurround.setBin("unsorted",50)
		sunX,sunY,sunZ=self.getLightSourcePosition()
		sunSurround.setPos(sunX,sunY,sunZ)
		sunSurround.setBillboardAxis()
		sunSurround.setTwoSided(True)
		tex = loader.loadTexture('textures/roadhighlight.png')
		sunSurround.setTexture(tex)
		sunSurround.setTransparency(TransparencyAttrib.MAlpha)
		self.sunSurround=sunSurround
		self.createdNodes.append(sunSurround)

		stencilReader2 = StencilAttrib.make(1,StencilAttrib.SCFEqual,StencilAttrib.SOKeep, StencilAttrib.SOKeep,StencilAttrib.SOKeep,2,2,0) 
		roadHighlightCm=CardMaker('card')
		roadHighlightCm.setFrame(-3000,3000,3000,-3000)
		roadHighlight = render.attachNewNode(roadHighlightCm.generate())
		roadHighlight.setDepthTest(True)
		roadHighlight.setDepthWrite(False)
		roadHighlight.setColor(1.0,1.0,1.0,0.4)
		roadHighlight.setBin("unsorted",50)
		sunX,sunY,sunZ=self.getLightSourcePosition()
		roadHighlight.setPos(sunX,sunY,sunZ)
		roadHighlight.setBillboardAxis()
		roadHighlight.setTwoSided(True)
		tex = loader.loadTexture('textures/roadhighlight.png')
		roadHighlight.setTexture(tex)
		roadHighlight.setTransparency(TransparencyAttrib.MAlpha)
		self.createdNodes.append(roadHighlight)
		roadHighlight.node().setAttrib(stencilReader2)
	
	def setStartingLight(self,lightNumber,illuminated):
		if illuminated:	
			n=self.lights.find("**/Light"+str(lightNumber)+"Off")
			n.hide()
			n=self.lights.find("**/Light"+str(lightNumber)+"On")
			n.show()
		else:
			n=self.lights.find("**/Light"+str(lightNumber)+"On")
			n.hide()		
			n=self.lights.find("**/Light"+str(lightNumber)+"Off")
			n.show()

		if illuminated:
			n=self.lights.find("**/Light"+str(lightNumber)+"On")
			x,y,z=n.getPos()
			self.trafficLight.setPos(x,y-0.02,z)
			self.trafficLight.show()
			if lightNumber==4:
				self.trafficLight.setColor(0.0,1.0,0.0,1.0)
			else:
				self.trafficLight.setColor(1.0,0.0,0.0,1.0)

	def addStaticScenery(self,xpos,ypos,rotation,modelFilename):

		modelFilenameElements=modelFilename.split('-')
		modelFilename=modelFilenameElements[0]
		textureFilename=modelFilenameElements[1]
		if modelFilename=='lowsign':
			textureFilename="alt-"+textureFilename+"low"
		if modelFilename=='highsign':
			textureFilename="alt-"+textureFilename

		m = loader.loadModel("models/"+modelFilename)
		m.reparentTo(self.carsAndSceneryNode)

		n=m.find("**/SignLogoAdvert")
		t=loader.loadTexture("models/"+textureFilename+".png")
		t.setMinfilter(Texture.FTLinearMipmapLinear)
		n.setTexture(t,1)

		m.setPos(xpos,ypos,0)
		m.setH(rotation)

		self.createdNodes.append(m)

		lightSourceX,lightSourceY,lightSourceZ=self.getLightSourcePosition()
		shadowGeomNode=ShadowGeometry.makeModelShadow('models/'+modelFilename+'shadow',xpos,ypos,0,lightSourceX,lightSourceY,lightSourceZ,rotation)
		shadow=render.attachNewNode(shadowGeomNode)
		shadow.setTwoSided(True)
		self.createdNodes.append(shadow)
		shadow.setPos(xpos,ypos,0)

		constantOneStencil = StencilAttrib.make(1,StencilAttrib.SCFAlways,StencilAttrib.SOZero,StencilAttrib.SOKeep,StencilAttrib.SOReplace,1,0,1)
		shadow.node().setAttrib(constantOneStencil)
		shadow.node().setAttrib(ColorWriteAttrib.make(0))
		shadow.setBin('fixed',40)
		shadow.setDepthWrite(0)

	def addPuddle(self,xpos,ypos,rotation):

		stencilWriter=self.getStencilWriter(4)
		puddleStencil = loader.loadModel("models/puddlestencil")
		puddleStencil.reparentTo(self.carsAndSceneryNode)
		puddleStencil.setPos(xpos,ypos,0)
		puddleStencil.setH(rotation)
		puddleStencil.node().setAttrib(stencilWriter)
		puddleStencil.node().setAttrib(ColorWriteAttrib.make(0))
		puddleStencil.setDepthWrite(False)
		puddleStencil.setDepthTest(False)
		self.createdNodes.append(puddleStencil)

		stencilReader = self.getStencilReader(4)
		puddle = loader.loadModel("models/puddle")
		puddle.reparentTo(self.carsAndSceneryNode)
		puddle.setPos(xpos,ypos,0)
		puddle.setH(rotation)
		puddle.setDepthWrite(False)
		puddle.node().setAttrib(stencilReader)
		puddle.setBin('fixed',40)
		self.createdNodes.append(puddle)

	def getStencilReader(self,bitmask):
		if bitmask in self.stencilReaders:
			stencilReader=self.stencilReaders[bitmask]
		else:
			stencilReader = StencilAttrib.make(1,StencilAttrib.SCFEqual,StencilAttrib.SOKeep, StencilAttrib.SOKeep,StencilAttrib.SOKeep,bitmask,bitmask,0) 
			self.stencilReaders[bitmask]=stencilReader
		return stencilReader

	def getStencilWriter(self,bitmask):
		if bitmask in self.stencilWriters:
			stencilWriter=self.stencilWriters[bitmask]
		else:
			stencilWriter = StencilAttrib.make(1,StencilAttrib.SCFEqual,StencilAttrib.SOZero,StencilAttrib.SOKeep,StencilAttrib.SOReplace,bitmask,0,bitmask)
			self.stencilWriters[bitmask]=stencilWriter
		return stencilWriter

	def addEvent(self,eventType,params=None):
		event={
			"eventType":eventType,
			"params":params
		}
		self.events.append(event)

	def onLapCompleted(self,lapTimeSeconds,lapTimeMilliseconds,topSpeed):
		if self.extendedPlayNotificationEnabled:
			self.displayExtendedPlayNotification()
		self.statusDisplay.flashLapTimeAndTopSpeed(lapTimeSeconds,lapTimeMilliseconds,topSpeed)

	def processEvents(self):
		if len(self.events)>0:
			for event in self.events:
				eventType=event["eventType"]
				params=event["params"]
				if eventType==self.sessionOverEvent:
					self.parent.addEvent(TrackSessionEvent.sessionCompleteEvent)
				elif eventType==self.sessionStartEvent:
					self.parent.addEvent(TrackSessionEvent.sessionStartEvent)
				elif eventType==self.playerCarPassedStartLineEvent:
					self.onLapCompleted(params["laptimeseconds"],params["laptimemilliseconds"],params["topspeed"])
				elif eventType==self.greenLightEvent:
					self.parent.addEvent(TrackSessionEvent.sessionStartEvent)
				elif eventType==self.qualifyingEndBlimpFlightCompleteEvent:
					self.qualifyingEndBlimpFlightComplete=True
					if self.qualifyingResultsDisplayComplete:
						self.addEvent(self.sessionOverEvent)
				elif eventType==self.qualifyingResultsDisplayCompleteEvent:
					self.qualifyingResultsDisplayComplete=True
					if self.qualifyingEndBlimpFlightComplete:
						self.addEvent(self.sessionOverEvent)
				elif eventType==self.passingBonusScoreUpdateEvent:
					self.parent.addEvent(TrackSessionEvent.passingBonusScoreUpdateEvent,
                                         {"currentcountdownnumber":params["currentcountdownnumber"],
                                          "startcountdownnumber":params["startcountdownnumber"]})

			self.events=[]

	def addCar(self,carAppearance,isPlayerCar):

		newVisualCar=Factory.Car(carAppearance)

		newVisualCar.reparentTo(self.carsAndSceneryNode)
		newVisualCar.setPos(self.segments[100].getMidPoint().getX(),self.segments[100].getMidPoint().getY(),0)
		newVisualCar.setH(270)

		constantOneStencil = StencilAttrib.make(1,StencilAttrib.SCFEqual,StencilAttrib.SOZero,StencilAttrib.SOKeep,StencilAttrib.SOReplace,1,0,1)

		bob=ShadowGeometry('models/f1carshadow')
		newVisualCarShadowGeomNode=bob.getSnode()
		lightSourceX,lightSourceY,lightSourceZ=self.getLightSourcePosition()
		bob.setLightPos(lightSourceX,lightSourceY,lightSourceZ)
		newVisualCarShadow=render.attachNewNode(newVisualCarShadowGeomNode)
		newVisualCarShadow.setTwoSided(True)
		newVisualCarShadow.node().setAttrib(constantOneStencil)
		newVisualCarShadow.node().setAttrib(ColorWriteAttrib.make(0))
		newVisualCarShadow.setBin('fixed',40)
		newVisualCarShadow.setDepthWrite(0)

		self.createdNodes.append(newVisualCar)
		self.createdNodes.append(newVisualCarShadow)
		visualCarRepresentation=VisualCarRepresentation(newVisualCar,bob,newVisualCarShadow)
		self.cars.append(visualCarRepresentation)
		if isPlayerCar:
			self.setPlayerCar(visualCarRepresentation)

		return visualCarRepresentation

	def getPlayerCar(self):
		return self.playerCar

	def setPlayerCar(self,playerCar):
		self.playerCar=playerCar

	def getCar(self,index):
		return self.cars[index]

	def setExtendedPlayNotificationEnabled(self,enabled):
		self.extendedPlayNotificationEnabled=enabled

	def displayQualifyingResult(self,lapTimeSeconds,lapTimeMilliseconds,position,bonus):
		qualifyingResultsDisplay=QualifyingResultsDisplay()
		qualifyingResultsDisplay.setLapTimeValue(lapTimeSeconds,lapTimeMilliseconds)
		qualifyingResultsDisplay.setPositionValue(position)
		qualifyingResultsDisplay.setBonusValue(bonus)
		qualifyingResultsDisplay.setCompletionEvent(self.qualifyingResultsDisplayCompleteEvent)
		self.addTimerDependentObject(qualifyingResultsDisplay)
		pass

	def displayExtendedPlayNotification(self):
		extendedPlayNotification=ExtendedPlayNotification()
		extendedPlayNotification.setCompletionEvent(None)
		self.addTimerDependentObject(extendedPlayNotification)

	def displayPassingBonus(self,carsPassed):
		passingBonusDisplay=PassingBonusDisplay(self,carsPassed)
		passingBonusDisplay.setCarsPassed(carsPassed)
		passingBonusDisplay.setCompletionEvent(self.sessionOverEvent)
		self.addTimerDependentObject(passingBonusDisplay)

	def displayGameOverNotification(self):
		camX,camY,camZ=base.camera.getPos()
		gameOverNotification=GameOverNotification(camX,camY,camZ,self.cameraRotationDegrees)
		gameOverNotification.setCompletionEvent(self.sessionOverEvent)
		self.addTimerDependentObject(gameOverNotification)

	def highlightCar(self,carNode):
		flasher=NodeFlasher(carNode)
		flasher.setCompletionEvent(None)
		self.addTimerDependentObject(flasher)

	def explodeCar(self,carNumber):
		pass

	def runQualifyingLightsSequence(self):
		qualifyingLightsChanger=QualifyingLightsChanger(self)
		qualifyingLightsChanger.setCompletionEvent(self.greenLightEvent)
		self.addTimerDependentObject(qualifyingLightsChanger)

	def runRaceLightsSequence(self):
		raceLightsChanger=RaceLightsChanger(self)
		raceLightsChanger.setCompletionEvent(self.greenLightEvent)
		self.addTimerDependentObject(raceLightsChanger)

	def addTimerDependentObject(self,obj):
		self.timerDependentObjects.append(obj)

	def advanceTime(self):
		self.processEvents()

		objectsToRemove=[]
		for timerDependentObject in self.timerDependentObjects:
			timerDependentObject.advanceTime()
			if timerDependentObject.hasDied():
				objectsToRemove.append(timerDependentObject)
		for objectToRemove in objectsToRemove:
			completionEvent=objectToRemove.getCompletionEvent()
			if completionEvent is not None:
				self.addEvent(objectToRemove.getCompletionEvent())
			objectToRemove.delete()
			self.timerDependentObjects.remove(objectToRemove)

		if self.ticks==0:
			for car in self.cars:
				car.refreshShadow()
		else:
			playerCar=self.getPlayerCar()
			if playerCar is not None:
				playerCar.refreshShadow()
			self.carShadowRefreshIndex=self.carShadowRefreshIndex+1
			if self.carShadowRefreshIndex==len(self.cars):
				self.carShadowRefreshIndex=0
			shadowCar=self.cars[self.carShadowRefreshIndex]
			if shadowCar is not playerCar:
				self.cars[self.carShadowRefreshIndex].refreshShadow()

		self.ticks=self.ticks+1
		self.statusDisplay.advanceTime()

		for car in self.cars:
			car.advanceTime()

	def closeSession(self):
		super(VisualTrackSession, self).closeSession()
		for createdNode in self.createdNodes:
			createdNode.removeNode()
		for timerDependentObject in self.timerDependentObjects:
			timerDependentObject.delete()
		self.gearIndicator.delete()

	def correctAspectRatio(self):
		width=base.win.getXSize()
		height=base.win.getYSize()
		base.camLens.setFov(30*float(width)/float(height),30)

	def getLightSourcePosition(self):
		return self.lightSourcePosition

	def setLightSourcePosition(self,lightSourcePosition):
		self.lightSourcePosition=lightSourcePosition

	def setBackgroundTexture(self,backgroundTexture):
		self.backgroundTexture=backgroundTexture

	def getBackgroundTexture(self):
		return self.backgroundTexture

	def setCameraDegreesRotationHint(self,degrees):

		self.cameraRotationDegrees=degrees
		if self.sunEffectsEnabled:
			startFlare=175.35
			degrees=degrees+180
			if degrees>360.0:
				degrees=degrees-360.0

			dazzlerColour=0.0
			carsAndSceneryScale=1.0
			sunSurroundBrightness=0.0

			if degrees>startFlare-15 and degrees<startFlare+15:
				if degrees>startFlare:
					brightness=(startFlare+15)-degrees
				else:
					brightness=degrees-(startFlare-15)
				sunSurroundBrightness=brightness/15
				carsAndSceneryScale=1.0-(brightness/100)*4

				if degrees>startFlare-5 and degrees<startFlare+5:
					if degrees>startFlare:
						dazzlerBrightness=(startFlare+5)-degrees
					else:
						dazzlerBrightness=degrees-(startFlare-5)
					dazzlerColour=dazzlerBrightness/5*0.25
			
			self.dazzler.setColor(1.0,1.0,0.75,dazzlerColour)
			self.sunSurround.setColor(1.0,1.0,0.75,sunSurroundBrightness)
			self.carsAndSceneryNode.setColorScale(carsAndSceneryScale,carsAndSceneryScale,carsAndSceneryScale,1.0)

	def setGearIndicator(self,gear):
		self.gearIndicator.setGear(gear)


