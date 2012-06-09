from playercarrepresentation import PlayerCarRepresentation
from computercarrepresentation import ComputerCarRepresentation
from nullcarrepresentation import NullCarRepresentation
from trackgeometry import TrackGeometry
from visualtracksession import VisualTrackSession
from keyboarddriver import KeyboardDriver
from tracksessionevent import TrackSessionEvent
from sessionlifecyclepoint import SessionLifecyclePoint
from logicalsession import LogicalSession
from carappearance import CarAppearance
from operator import methodcaller
import math
import Geometry
import random
from destinationlane import DestinationLane
from soundserver import SoundServer
from timeofday import TimeOfDay
from sessiontype import SessionType

class TrackSession(LogicalSession):

	beforeRaceStart=0
	duringRace=1
	outOfTime=2
	endOfSession=3

	framesPerSecond=60

	speedLimitUnlimited=100
	
	def __init__(self):

		super(TrackSession, self).__init__()

		self.paused=False

		trackData=TrackGeometry.loadFromFile('test.xml')
		self.segments=trackData.getTrackSegments()

		if self.getSessionType()==SessionType.qualifying:
			timeOfDay=TimeOfDay.earlyAfternoon
		else:
			timeOfDay=TimeOfDay.dusk

		self.visualTrackSession=VisualTrackSession(self,self.segments,timeOfDay)

		if self.getSessionType()==SessionType.qualifying:
			self.visualTrackSession.setExtendedPlayNotificationEnabled(False)

		self.sceneryPositions=[]
		self.puddlePositions=[]

		self.addStaticScenery('highsign-digdug',5,'left') # dig dug
		self.addStaticScenery('highsign-centipede',10,'right') # centipede
		self.addStaticScenery('highsign-rightarrow',15,'left') # right arrow
		self.addStaticScenery('highsign-poleposition',21,'left') # pole position
		self.addStaticScenery('highsign-atari',25,'right') # atari
		self.addStaticScenery('highsign-centipede',30,'right') # centipede
		self.addStaticScenery('highsign-amusement',31,'right') # namco
		self.addStaticScenery('lowsign-namco',35,'left') # namco
		self.addStaticScenery('highsign-digdug',32.5,'left') # dig dug
		self.addStaticScenery('lowsign-atari',39,'left') # atari
		self.addStaticScenery('highsign-leftarrow',48,'left') # left arrow 
		self.addStaticScenery('highsign-centipede',52,'right') # centipede
		self.addStaticScenery('lowsign-namco',54,'left')
		self.addStaticScenery('highsign-atari',60,'right')
		self.addStaticScenery('highsign-digdug',64,'left')
		self.addStaticScenery('highsign-amusement',68,'right')
		self.addStaticScenery('highsign-usa',72,'right')
		self.addStaticScenery('highsign-poleposition',77,'left')
		self.addStaticScenery('lowsign-atari',83,'left')
		self.addStaticScenery('highsign-digdug',87,'left')
		self.addStaticScenery('highsign-atari',91,'right')
		self.addStaticScenery('highsign-poleposition',93,'left')
		self.addStaticScenery('highsign-amusement',96,'right')

		# common to all sessions
		self.lapTimeTicks=-1
		self.frames=0
		self.secondsRemaining=-1
		self.logicalCarRepresentations=[]
		self.topScore=0
		self.events=[]
		self.score=0
		self.speed=0
		self.topSpeed=0
		self.scoringActive=False
		self.setPlayerCar(None)
		self.countdownTimerActive=False
		self.speedLimit=self.speedLimitUnlimited
		self.carsPassed=0

		self.initSession()

		self.setSessionLifecyclePoint(SessionLifecyclePoint.running)

	def setSpeedLimit(self,speedLimit):
		self.speedLimit=speedLimit

	def getSpeedLimit(self):
		return self.speedLimit

	def getFastestLapTime(self):
		return self.getPlayerCar().getFastestLapTime()

	def setCountdownTimerActive(countdownTimerActive):
		self.countdownTimerActive=countdownTimerActive

	def addPlayerCar(self,segmentPosition,sidewaysPosition,speed,carAppearance):
		newLogicalCar=PlayerCarRepresentation(self)
		newLogicalCar.setSegmentPosition(segmentPosition)
		newLogicalCar.setSidewaysPosition(sidewaysPosition)
		newLogicalCar.setSpeed(speed)
		newLogicalCar.setTrackSegments(self.segments)
		newLogicalCar.setDriver(KeyboardDriver())
		self.logicalCarRepresentations.append(newLogicalCar)
		newLogicalCar.setCarNumber(len(self.logicalCarRepresentations))
		SoundServer.getInstance().startEngine(newLogicalCar.getCarNumber())
		SoundServer.getInstance().setEngineVolume(newLogicalCar.getCarNumber(),1.0)
		newLogicalCar.setVisualPeer(self.visualTrackSession.addCar(carAppearance,True))
		return newLogicalCar

	def addNullCar(self,segmentPosition,sidewaysPosition):
		newLogicalCar=NullCarRepresentation(self)
		newLogicalCar.setSegmentPosition(segmentPosition)
		newLogicalCar.setSidewaysPosition(sidewaysPosition)
		return newLogicalCar

	def addComputerCar(self,segmentPosition,sidewaysPosition,currentLane,speed,carAppearance):
		newLogicalCar=ComputerCarRepresentation(self)
		newLogicalCar.setSegmentPosition(segmentPosition)
		newLogicalCar.setSidewaysPosition(sidewaysPosition)
		newLogicalCar.setCurrentLane(currentLane)
		newLogicalCar.setSpeed(speed)
		newLogicalCar.setTrackSegments(self.segments)
		self.logicalCarRepresentations.append(newLogicalCar)
		newLogicalCar.setCarNumber(len(self.logicalCarRepresentations))
		SoundServer.getInstance().startEngine(newLogicalCar.getCarNumber())
		newLogicalCar.setVisualPeer(self.visualTrackSession.addCar(carAppearance,False))
		return newLogicalCar

	def addRandomCar(self):
		appearanceRand=random.random()
		if appearanceRand<0.25:
			appearance=CarAppearance.whiteAndRed
		elif appearanceRand<0.5:
			appearance=CarAppearance.redAndOrange
		elif appearanceRand<0.75:	
			appearance=CarAppearance.yellowAndOrange
		else:
			appearance=CarAppearance.whiteAndGreen

		segmentsLength=len(self.getSegments())
		clearArea=100
		segmentPosition=random.random()*(segmentsLength-clearArea)+(clearArea-1)

		if random.random()>0.5:
			sidewaysPosition=DestinationLane.leftPosition
			currentLane=DestinationLane.left
		else:
			sidewaysPosition=DestinationLane.rightPosition
			currentLane=DestinationLane.right

		newCar=self.addComputerCar(segmentPosition,sidewaysPosition,currentLane,0,appearance)
		return newCar

	def addStaticScenery(self,sceneryType,percentDistance,trackSide):
		segmentIndex=int(float(len(self.segments))/100*percentDistance)
		if trackSide=='left':
			sidewaysPosition=-1.5
		else:
			sidewaysPosition=1.5

		currentSegmentVector=self.segments[segmentIndex].getVector()

		rotation=self.convertVectorToDegreesRotation(currentSegmentVector)+270.0
		if rotation>360.0:
			rotation=rotation-360.0

		worldPosition=TrackGeometry.getWorldPositionByTrackPosition(self.segments,segmentIndex,sidewaysPosition)
		self.visualTrackSession.addStaticScenery(worldPosition['xpos'],worldPosition['ypos'],rotation,sceneryType)
		self.sceneryPositions.append({ 'sidewaysposition': trackSide, 'segment': float(segmentIndex) })

	def addPuddle(self,percentDistance,trackSide):
		segmentIndex=int(float(len(self.segments))/100*percentDistance)
		if trackSide=='left':
			sidewaysPosition=-0.4
		else:
			sidewaysPosition=0.4

		currentSegmentVector=self.segments[segmentIndex].getVector()

		rotation=self.convertVectorToDegreesRotation(currentSegmentVector)+270.0
		if rotation>360.0:
			rotation=rotation-360.0

		worldPosition=TrackGeometry.getWorldPositionByTrackPosition(self.segments,segmentIndex,sidewaysPosition)
		self.visualTrackSession.addPuddle(worldPosition['xpos'],worldPosition['ypos'],rotation)
		self.puddlePositions.append({ 'sidewaysposition': sidewaysPosition, 'segment': float(segmentIndex) })

	def getSceneryPositions(self):
		return self.sceneryPositions

	def getPuddlePositions(self):
		return self.puddlePositions

	def convertVectorToDegreesRotation(self,vector):
		rotation=math.atan2(vector.getY(),vector.getX())
		if rotation>math.pi:
			rotation=rotation-math.pi*2
		if rotation<-math.pi:
			rotation=rotation+math.pi*2
		rotation=rotation/(math.pi*2)*360.0
		if rotation>360.0:
			rotation=rotation-360.0
		elif rotation<0.0:
			rotation=rotation+360.0
		return rotation	

	def setSegments(self,segments):
		self.segments=segments

	def getSegments(self):
		return self.segments

	def setTicksRemaining(self,ticksRemaining):
		self.ticksRemaining=ticksRemaining
		self.setSecondsRemaining(int(ticksRemaining/self.framesPerSecond))

	def getTicksRemaining(self):
		return self.ticksRemaining

	def setLapTimeTicks(self,lapTimeTicks):
		if (lapTimeTicks!=self.lapTimeTicks):
			self.lapTimeTicks=lapTimeTicks
			secondsAndMilliseconds=self.convertLapTimeTicksToSecondsAndMilliseconds(lapTimeTicks)
			self.visualTrackSession.setLapTime(secondsAndMilliseconds["seconds"],secondsAndMilliseconds["milliseconds"])

	def convertLapTimeTicksToSecondsAndMilliseconds(self,lapTimeTicks):
		seconds=lapTimeTicks/60
		milliseconds=(lapTimeTicks%60)*5/3
		return({"seconds":seconds,"milliseconds":milliseconds})

	def getLapTimeTicks(self):
		return self.lapTimeTicks

	def setSecondsRemaining(self,secondsRemaining):
		self.secondsRemaining=secondsRemaining
		self.visualTrackSession.setSecondsRemaining(secondsRemaining)

	def getSecondsRemaining(self):
		return self.secondsRemaining

	def getScore(self):
		return self.score

	def setScore(self,score):
		if self.score!=score:
			if score>self.getTopScore():
				self.setTopScore(score)
			self.visualTrackSession.setScore(score)
			self.score=score

	def getTopScore(self):
		return self.topScore

	def setTopScore(self,topScore):
		if self.topScore!=topScore:
			self.visualTrackSession.setTopScore(topScore)
			self.topScore=topScore

	def setSpeed(self,speed):
		if self.speed!=speed:
			self.visualTrackSession.setSpeed(speed)
			if speed>self.getTopSpeed():
				self.setTopSpeed(speed)
			self.speed=speed

	def getTopSpeed(self):
		return self.topSpeed

	def setTopSpeed(self,topSpeed):
		if self.topSpeed!=topSpeed:
			self.topSpeed=topSpeed

	def addEvent(self,eventType,params=None):
		event={
			"eventType":eventType,
			"params":params
		}
		self.events.append(event)

	def onCarCompletedLap(self,participant):
		pass

	def onTimeExpired(self):
		pass

	def processEvents(self):
		if len(self.events)>0:
			for event in self.events:
				eventType=event["eventType"]
				params=event["params"]
				if eventType==TrackSessionEvent.carCompletedLapEvent:
					self.onCarCompletedLap(params["participant"])
				elif eventType==TrackSessionEvent.carStoppedEvent:
					self.onCarStopped(params["participant"])
				elif eventType==TrackSessionEvent.playerPositionChangedEvent:
					self.onPlayerCarPositionChanged(params["newposition"])
				elif eventType==TrackSessionEvent.timeExpiredEvent:
					self.onTimeExpired()
				elif eventType==TrackSessionEvent.sessionCompleteEvent:
					self.closeSession()
				elif eventType==TrackSessionEvent.sessionStartEvent:
					self.onRaceStarted()
				elif eventType==TrackSessionEvent.carStartedFirstLapEvent:
					self.onCarStartedFirstLap(params["participant"])
				elif eventType==TrackSessionEvent.gearChangedEvent:
					self.onGearChanged(params["gear"])
				elif eventType==TrackSessionEvent.passingBonusScoreUpdateEvent:
					currentCountdownNumber=params["currentcountdownnumber"]
					topCountdownNumber=params["startcountdownnumber"]
					scoreTopUp=(topCountdownNumber-currentCountdownNumber)*50
					outcome=self.getOutcome()
					scoreBeforeTopUp=outcome["scorebeforetopup"]
					self.setScore(scoreBeforeTopUp+scoreTopUp)
			self.events=[]		

	def getPlayerCar(self):
		return self.playerCar

	def setPlayerCar(self,playerCar):
		self.playerCar=playerCar

	def getCameraCar(self):
		return self.cameraCar

	def setCameraCar(self,cameraCar):
		self.cameraCar=cameraCar

	def setSessionStatus(self,status):
		self.sessionStatus=status

	def getSessionStatus(self):
		return self.sessionStatus

	def advanceTime(self):	
		playerCar=self.getPlayerCar()
		if playerCar:
			playerDriver=self.getPlayerCar().getDriver()
			playerDriver.interpretInputs()
	
			if playerDriver.getPauseToggleRequested():
				self.paused=not self.paused
				playerDriver.acknowledgePauseToggleRequested()

		if not self.paused:
			self.advanceTimeWhenNotPaused()
		else:
			self.positionCamera()

	def advanceTimeWhenNotPaused(self):
		playerCar=self.getPlayerCar()

		if playerCar:
			if self.scoringActive:
				score=self.startingScore
				score=(playerCar.getLapsCompleted()*10120)
				score=score+self.startingScore
				score=score+int(10120.0/float(len(self.segments))*playerCar.getSegmentPosition())
				score=score-(score%10)
			else:
				score=self.getScore()
			self.setScore(score)

			self.setLapTimeTicks(self.getPlayerCar().getCurrentLapTimeTicks())

			self.setSpeed(int(self.getPlayerCar().getSpeed()*339))

		self.advanceCars()
		self.positionCamera()
		self.processEvents()
		self.updateTicksRemaining()
		self.visualTrackSession.advanceTime()

		self.frames=self.frames+1

	def updateTicksRemaining(self):
		ticksRemaining=self.getTicksRemaining()
		if self.countdownTimerActive:
			if ticksRemaining>0:
				self.setTicksRemaining(ticksRemaining-1)
			else:
				self.addEvent(TrackSessionEvent.timeExpiredEvent)
		else:	
			self.setTicksRemaining(ticksRemaining)

	def advanceCars(self):
		soundServer=SoundServer.getInstance()

		for carRepresentation in self.logicalCarRepresentations:

			carRepresentation.move()

			carWorldPosition=TrackGeometry.getWorldPositionByTrackPosition(self.getSegments(),
																			carRepresentation.getSegmentPosition(),
			  																carRepresentation.getSidewaysPosition())
	
			carRepresentation.getVisualPeer().setPos(carWorldPosition["xpos"],carWorldPosition["ypos"],0)

			currentSegmentComponents=math.modf(carRepresentation.getSegmentPosition())
			distanceThroughCurrentSegment=currentSegmentComponents[0]

			currentSegmentIndex=int(math.floor(carRepresentation.getSegmentPosition()))
			nextSegmentIndex=currentSegmentIndex+1
			if nextSegmentIndex>len(self.segments)-1:
				nextSegmentIndex=nextSegmentIndex-len(self.segments)

			currentSegmentVector=self.segments[currentSegmentIndex].getVector()
			nextSegmentVector=self.segments[nextSegmentIndex].getVector()
			interpolatedX=currentSegmentVector.getX()+(nextSegmentVector.getX()-currentSegmentVector.getX())*distanceThroughCurrentSegment
			interpolatedY=currentSegmentVector.getY()+(nextSegmentVector.getY()-currentSegmentVector.getY())*distanceThroughCurrentSegment
			
			heading=self.convertVectorToDegreesRotation(Geometry.Point(interpolatedX,interpolatedY))
			heading=heading+270.0
			if heading>360.0:
				heading=heading-360.0

			if carRepresentation is self.getPlayerCar():
				pitch=carRepresentation.getEngine().getRevs()/6000+0.4

				SoundServer.getInstance().setEnginePitch(carRepresentation.getCarNumber(),pitch)

				heading=heading-(float)(carRepresentation.getSteering())*20
				if heading>360:
					heading=heading-360
				elif heading<0:
					heading=heading+360
			else:
				pitch=carRepresentation.getSpeed()*2+0.4
				soundServer.setEnginePitch(carRepresentation.getCarNumber(),pitch)

				distance=carRepresentation.getPlayerDistance()
				volume=(10.0-distance)/10.0
				soundServer.setEngineVolume(carRepresentation.getCarNumber(),volume)

				balance=self.getCameraCar().getSidewaysPosition()-carRepresentation.getSidewaysPosition()
				if balance<-1.0:
					balance=-1.0
				elif balance>1.0:
					balance=1.0
				soundServer.setEngineBalance(carRepresentation.getCarNumber(),balance)

			carRepresentation.getVisualPeer().setH(heading)

		playerCar=self.getPlayerCar()
		if playerCar is not None:
			playerCar.detectCollisions()
			playerCar.detectSceneryCollisions()

			if self.overtakeTrackingEnabled:
				playerSegmentPosition=playerCar.getSegmentPosition()
				playerLastSegmentPosition=playerCar.getLastSegmentPosition()
				if playerSegmentPosition>playerLastSegmentPosition:
					for car in self.getLogicalCarRepresentations():
						if car is not playerCar:
							if not car.getLastMoveWasWrap():
								computerSegmentPosition=car.getSegmentPosition()
								computerLastSegmentPosition=car.getLastSegmentPosition()
								if computerSegmentPosition>computerLastSegmentPosition:
									if playerLastSegmentPosition<computerLastSegmentPosition and playerSegmentPosition>computerSegmentPosition:
										self.carsPassed=self.carsPassed+1
									if playerLastSegmentPosition>computerLastSegmentPosition and playerSegmentPosition<computerSegmentPosition:
										self.carsPassed=self.carsPassed-1

	def positionCamera(self):
		carRepresentation=self.getCameraCar()

		lookAtSegment=carRepresentation.getSegmentPosition()+1
		if lookAtSegment>float(len(self.segments)-1):
			lookAtSegment=lookAtSegment-float(len(self.segments))

		carWorldPosition=TrackGeometry.getWorldPositionByTrackPosition(self.segments,
																			carRepresentation.getSegmentPosition(),
			  																carRepresentation.getSidewaysPosition())

		carBearingPosition=TrackGeometry.getWorldPositionByTrackPosition(self.segments,
																			lookAtSegment,
			  																carRepresentation.getSidewaysPosition())

		cameraSegmentPosition=carRepresentation.getSegmentPosition()-2.5
		if cameraSegmentPosition<0:
			cameraSegmentPosition=cameraSegmentPosition+len(self.segments)

		cameraWorldPosition=TrackGeometry.getWorldPositionByTrackPosition(self.segments,
																			cameraSegmentPosition,
			  																carRepresentation.getSidewaysPosition())

		base.camera.setPos(cameraWorldPosition["xpos"],cameraWorldPosition["ypos"],0.5)
		base.camera.lookAt(carWorldPosition["xpos"],carWorldPosition["ypos"],0.5);

		cameraVectorX=carWorldPosition["xpos"]-cameraWorldPosition["xpos"]
		cameraVectorY=carWorldPosition["ypos"]-cameraWorldPosition["ypos"]
		cameraDegreesRotation=self.convertVectorToDegreesRotation(Geometry.Point(cameraVectorX,cameraVectorY))
		self.visualTrackSession.setCameraDegreesRotationHint(cameraDegreesRotation)

	def getLogicalCarRepresentations(self):
		return self.logicalCarRepresentations

	def getCornerSharpness(self,segmentPosition):
		if segmentPosition>=len(self.segments):
			segmentPosition=segmentPosition-len(self.segments)
		currentSegment=self.segments[segmentPosition]
		nextSegmentIndex=segmentPosition+1
		if nextSegmentIndex>=len(self.segments):
			nextSegmentIndex=nextSegmentIndex-len(self.segments)
		nextSegment=self.segments[nextSegmentIndex]
		currentSegmentVector=currentSegment.getVector()
		nextSegmentVector=nextSegment.getVector()
		sharpness=math.atan2(currentSegmentVector.getX(),currentSegmentVector.getY())-math.atan2(nextSegmentVector.getX(),nextSegmentVector.getY())
		if sharpness>math.pi:
			sharpness=sharpness-math.pi*2
		if sharpness<-math.pi:
			sharpness=sharpness+math.pi*2
		return sharpness

	def closeSession(self):
		soundServer=SoundServer.getInstance()
		for carRepresentation in self.logicalCarRepresentations:
			soundServer.stopEngine(carRepresentation.getCarNumber())

		self.setSessionLifecyclePoint(SessionLifecyclePoint.closing)
		self.visualTrackSession.closeSession()
		self.setSessionLifecyclePoint(SessionLifecyclePoint.closed)

	def onCarStartedFirstLap(self,participant):
		if participant is self.getPlayerCar():
			self.scoringActive=True

	def onRaceStarted(self):
		self.countdownTimerActive=True
		for logicalCarRepresentation in self.logicalCarRepresentations:
			logicalCarRepresentation.setHandbrake(False)

	def onGearChanged(self,gear):
		self.visualTrackSession.setGearIndicator(gear)

	def onPlayerCarPositionChanged(self,position):
		pass

	def getSessionType(self):
		return self.sessionType

	def setSessionType(self,sessionType):
		self.sessionType=sessionType

	def sendPlayerLapCompletionEventToVisualTrackSession(self):
		playerCar=self.getPlayerCar()
		lastLapTimeTicks=playerCar.getLapTime(playerCar.getLapsCompleted())
		secondsAndMilliseconds=self.convertLapTimeTicksToSecondsAndMilliseconds(lastLapTimeTicks)	
		self.visualTrackSession.addEvent(VisualTrackSession.playerCarPassedStartLineEvent,
                                         {"laptimeseconds":secondsAndMilliseconds["seconds"],
                                          "laptimemilliseconds":secondsAndMilliseconds["milliseconds"],
                                          "topspeed":self.getTopSpeed()})


