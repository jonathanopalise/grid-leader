from highscoreoverlay import HighScoreOverlay

class PrizeWinnersHighScoreOverlay(HighScoreOverlay):

	numberOfRows=6
	headersRow=16

	def addPeripheralText(self):
		self.addText('enterinitials','ENTER YOUR INITIALS',23,21,1.0,1.0,1.0,self.alignRight)
		self.addText('prizewinners','<PRIZE WINNERS>',21,19,1.0,1.0,1.0,self.alignRight)

