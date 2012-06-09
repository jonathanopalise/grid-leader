from highscoreoverlay import HighScoreOverlay

class ViewingOnlyHighScoreOverlay(HighScoreOverlay):

	numberOfRows=8
	headersRow=18

	def addPeripheralText(self):
		self.addText('past300','TODAY\'S GRID LEADERS',24,21,1.0,1.0,1.0,self.alignRight)

