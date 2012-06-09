from highscoreoverlay import HighScoreOverlay

class NormalHighScoreOverlay(HighScoreOverlay):

	numberOfRows=8
	headersRow=18

	def addPeripheralText(self):
		self.addText('enterinitials','ENTER YOUR INITIALS',23,21,1.0,1.0,1.0,self.alignRight)

