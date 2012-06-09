from colours import Colours
from highscoreoverlay import HighScoreOverlay
from visualhighscoresessiontype import VisualHighScoreSessionType
from prizewinnershighscoreoverlay import PrizeWinnersHighScoreOverlay
from normalhighscoreoverlay import NormalHighScoreOverlay
from viewingonlyhighscoreoverlay import ViewingOnlyHighScoreOverlay
from visualscoredisplaysession import VisualScoreDisplaySession

class VisualHighScoreSession(VisualScoreDisplaySession):

	def __init__(self,sessionType):
		super(VisualHighScoreSession, self).__init__()
		base.setBackgroundColor(45.0/255.0,67.0/255.0,157.0/255.0)

		if sessionType==VisualHighScoreSessionType.prizeWinnersInitialsEntry:
			self.highScoreOverlay=PrizeWinnersHighScoreOverlay()
		elif sessionType==VisualHighScoreSessionType.normalInitialsEntry:
			self.highScoreOverlay=NormalHighScoreOverlay()
		else:
			self.highScoreOverlay=ViewingOnlyHighScoreOverlay()

	def setRowContent(self,rowNumber,position,initials,score):
		self.highScoreOverlay.setRowContent(rowNumber,position,initials,score)

	def setRowInitial(self,rowNumber,initialIndex,value):
		self.highScoreOverlay.setRowInitial(rowNumber,initialIndex,value)

	def setCycleAllInitials(self):
		self.highScoreOverlay.setCycleAllInitials()

	def setCycleSpecificInitial(self,initialIndex):
		self.highScoreOverlay.setCycleSpecificInitial(initialIndex)

	def startRowColourCycling(self,rowNumber):
		self.highScoreOverlay.startRowColourCycling(rowNumber)

	def advanceTime(self):
		self.highScoreOverlay.advanceTime()

	def closeSession(self):
		super(VisualHighScoreSession, self).closeSession()
		self.highScoreOverlay.delete()



