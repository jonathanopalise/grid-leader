from visualhighscoresession import VisualHighScoreSession
from logicalsession import LogicalSession
from sessionlifecyclepoint import SessionLifecyclePoint
from sessiontype import SessionType
#from xml.dom import minidom
from visualhighscoresessiontype import VisualHighScoreSessionType
from soundserver import SoundServer
from keyboardhandler import KeyboardHandler
from highscoreserver import HighScoreServer

class HighScoreSession(LogicalSession):

	permittedLetters='ABCDEFGHIJKLMNOPQRSTUVWXYZ. '

	def __init__(self,score,topScore,topSpeed,fastestLapTimeSeconds,fastestLapTimeMilliseconds,whereFrom):
		self.initialsEntryActive=False
		self.viewingOnlyActive=False
		self.score=score
		self.ticks=0
		self.topScore=0
		self.keyboardHandler=KeyboardHandler.getInstance()
		self.confirmedInitials=''

		if whereFrom=="titlescreen":
			destination="titlescreen"
		else:
			destination="gameover"

		super(HighScoreSession, self).__init__()

		self.loadScores()
		tablePosition=self.getTablePosition(score)
		self.tablePosition=tablePosition

		if tablePosition is None:
			self.createVisualSession(VisualHighScoreSessionType.viewingOnly)
			self.startViewingOnly()
			self.viewingOnlyActive=True
		elif tablePosition<7:
			self.createVisualSession(VisualHighScoreSessionType.prizeWinnersInitialsEntry)
			self.startInitialsEntry(6,score,tablePosition)
		else:
			self.createVisualSession(VisualHighScoreSessionType.normalInitialsEntry)
			self.startInitialsEntry(8,score,tablePosition)

		self.setTopScore(topScore)
		self.setScore(score)
		self.setLapTime(fastestLapTimeSeconds,fastestLapTimeMilliseconds)
		self.setSpeed(topSpeed)
		
		SoundServer.getInstance().playMusic()

		self.countingDownToClose=False

		self.setOutcome({"sessiontype":SessionType.highScoreTable,
                         "score":self.score,
                         "destination":destination})

	def createVisualSession(self,sessionType):
		self.visualSession=VisualHighScoreSession(sessionType)
		self.setSessionLifecyclePoint(SessionLifecyclePoint.running)

	def setTopScore(self,topScore):
		self.visualSession.setTopScore(topScore)
		self.topScore=topScore

	def setScore(self,score):
		self.visualSession.setScore(score)
		self.score=score

	def setLapTime(self,seconds,milliseconds):
		self.visualSession.setLapTime(seconds,milliseconds)

	def setSpeed(self,speed):
		self.visualSession.setSpeed(speed)

	def insertScoreIntoTable(self,score,position):
		self.highScores.insert(position-1,{"initials" : '   ', "score" : score})
		self.highScores.pop()

	def startInitialsEntry(self,numRows,score,position):
		self.insertScoreIntoTable(score,position)

		activeRow=numRows/2
		currentSourceRow=position-(activeRow-1)
		if currentSourceRow<1:
			activeRow=activeRow+(currentSourceRow-1)
			currentSourceRow=1

		for destinationRow in range(1,numRows+1):
			highScoreListItem=self.highScores[currentSourceRow-1]
			self.visualSession.setRowContent(destinationRow,currentSourceRow,highScoreListItem['initials'],highScoreListItem['score'])
			self.visualSession.startRowColourCycling(activeRow)
			currentSourceRow=currentSourceRow+1

		self.activeRow=activeRow
		self.letterSubPosition=5
		self.permittedLettersIndex=0
		self.initialIndex=0
		self.initialsEntryActive=True
		self.startCurrentInitialEntry()

	def setInitialIndex(self,initialIndex):
		self.initialIndex=initialIndex

	def getInitialIndex(self):
		return self.initialIndex

	def startViewingOnly(self):
		currentSourceRow=1
		numRows=8
		for destinationRow in range(1,numRows+1):
			highScoreListItem=self.highScores[currentSourceRow-1]
			self.visualSession.setRowContent(destinationRow,currentSourceRow,highScoreListItem['initials'],highScoreListItem['score'])
			currentSourceRow=currentSourceRow+1

	def getTablePosition(self,score):
		checkingPosition=1
		tablePosition=None	
		for entry in self.highScores:
			if score>entry['score']:
				tablePosition=checkingPosition
				break
			checkingPosition=checkingPosition+1
		return tablePosition	


	def loadScores(self):
		highScoreServer=HighScoreServer.getInstance()
		self.highScores=highScoreServer.getHighScores()	

	def saveScores(self):
		highScoreServer=HighScoreServer.getInstance()
		highScoreServer.setHighScores(self.highScores)
	
	def startCurrentInitialEntry(self):
		self.visualSession.setCycleSpecificInitial(self.initialIndex)
		self.setCurrentInitial(self.permittedLetters[self.permittedLettersIndex])

	def setCurrentInitial(self,initial):
		self.visualSession.setRowInitial(self.activeRow,self.initialIndex,initial)
		self.currentInitial=initial

	def getCurrentInitial(self):
		return self.currentInitial

	def confirmCurrentInitial(self):
		self.confirmedInitials=self.confirmedInitials+self.permittedLetters[self.permittedLettersIndex]
		if self.initialIndex==2:
			self.highScores[self.tablePosition-1]["initials"]=self.confirmedInitials
			self.initialsEntryActive=False
			self.countingDownToClose=True
			self.ticksUntilClose=300
			self.visualSession.setCycleAllInitials()
		else:
			self.initialIndex=self.initialIndex+1
			self.startCurrentInitialEntry()

	def onNextLetter(self):
		self.permittedLettersIndex=self.permittedLettersIndex+1
		if self.permittedLettersIndex>len(self.permittedLetters)-1:
			self.permittedLettersIndex=0
		self.setCurrentInitial(self.permittedLetters[self.permittedLettersIndex])

	def onPreviousLetter(self):
		self.permittedLettersIndex=self.permittedLettersIndex-1
		if self.permittedLettersIndex<0:
			self.permittedLettersIndex=len(self.permittedLetters)-1
		self.setCurrentInitial(self.permittedLetters[self.permittedLettersIndex])

	def moveTowardsPreviousLetter(self):
		self.letterSubPosition=self.letterSubPosition-1
		if self.letterSubPosition<0:	
			self.letterSubPosition=6
			self.onPreviousLetter()

	def moveTowardsNextLetter(self):
		self.letterSubPosition=self.letterSubPosition+1
		if self.letterSubPosition>6:
			self.letterSubPosition=0
			self.onNextLetter()

	def advanceTime(self):

		if self.initialsEntryActive:

			rightArrow=self.keyboardHandler.getRightArrowStatus()
			leftArrow=self.keyboardHandler.getLeftArrowStatus()
			space=self.keyboardHandler.getSpaceStatus()

			if space==1:
				self.keyboardHandler.clearSpaceStatus()
				self.confirmCurrentInitial()
			elif rightArrow==1:
				self.moveTowardsNextLetter()
			elif leftArrow==1:
				self.moveTowardsPreviousLetter()

		if self.countingDownToClose:
			self.ticksUntilClose=self.ticksUntilClose-1
			if self.ticksUntilClose==0:
				self.closeSession()

		if self.viewingOnlyActive:
			space=self.keyboardHandler.getSpaceStatus()
			if space==1:
				self.keyboardHandler.clearSpaceStatus()
				self.closeSession()
			elif self.ticks==10*60:
				self.closeSession()

		self.visualSession.advanceTime()
		self.ticks=self.ticks+1

	def closeSession(self):
		self.saveScores()
		self.setSessionLifecyclePoint(SessionLifecyclePoint.closing)
		self.visualSession.closeSession()
		self.setSessionLifecyclePoint(SessionLifecyclePoint.closed)

