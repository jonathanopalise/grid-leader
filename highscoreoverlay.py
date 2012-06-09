from textoverlay import TextOverlay
from colours import Colours

class HighScoreOverlay(TextOverlay):

	headersRow=13

	def __init__(self):

		super(HighScoreOverlay, self).__init__()
		self.cyclingColours=Colours.getCyclingColours()

		self.cyclingRow=None
		self.rowReferences=[]
		y=self.getHeadersRow()

		self.addRowHeaders(y)
		y=y-2

		for i in range(self.getNumberOfRows()):
			self.rowReferences.append({
				'no':       self.addText('norow'+str(i),'',5,y,1.0,1.0,1.0,self.alignRight),
				'score':    self.addText('scorerow'+str(i),'',12,y,1.0,1.0,1.0,self.alignRight),
				'time':     self.addText('timerow'+str(i),'',19,y,1.0,1.0,1.0,self.alignRight),
				'initials0': self.addText('namerow'+str(i),'',24,y,1.0,1.0,1.0,self.alignRight),
				'initials1': self.addText('namerow'+str(i),'',25,y,1.0,1.0,1.0,self.alignRight),
				'initials2': self.addText('namerow'+str(i),'',26,y,1.0,1.0,1.0,self.alignRight)
			})

			y=y-2

		self.addPeripheralText()

		self.ticks=0	
		self.endOfLife=False

	def addRowHeaders(self,y):
		self.addText('noheader','NO.',5,y,1.0,1.0,1.0,self.alignRight)
		self.addText('scoreheader','SCORE',12,y,1.0,1.0,1.0,self.alignRight)
		self.addText('timeheader','TIME',19,y,1.0,1.0,1.0,self.alignRight)
		self.addText('nameheader','NAME',26,y,1.0,1.0,1.0,self.alignRight)

	def addPeripheralText(self):
		pass

	def setRowContent(self,rowNumber,position,initials,score):
		rowReference=self.rowReferences[rowNumber-1]
		rowReference['no'].setText(str(position))
		rowReference['score'].setText(str(score))
		for i in range(3):
			rowReference['initials'+str(i)].setText(initials[i])

	def setRowInitial(self,rowNumber,initialIndex,initial):
		rowReference=self.rowReferences[rowNumber-1]
		rowReference['initials'+str(initialIndex)].setText(initial)

	def getNumberOfRows(self):
		return self.numberOfRows
	
	def getHeadersRow(self):
		return self.headersRow

	def advanceTime(self):
		self.ticks=self.ticks+1
		if self.cyclingRow is not None:
			colourIndex=self.ticks%6
			r,g,b=self.cyclingColours[colourIndex]
			self.setRowColour(self.cyclingRow,r,g,b)

	def startRowColourCycling(self,rowNumber):
		self.cyclingRow=rowNumber
		self.setCycleAllInitials()

	def setCycleAllInitials(self):
		self.initialIndicesToCycle=[0,1,2]

	def setCycleSpecificInitial(self,initialIndex):	
		self.initialIndicesToCycle=[initialIndex]

	def setRowColour(self,rowNumber,r,g,b):
		rowReference=self.rowReferences[rowNumber-1]
		rowReference['no'].setTextColor(r,g,b,1.0)
		rowReference['score'].setTextColor(r,g,b,1.0)

		rowReference['initials0'].setTextColor(1.0,1.0,1.0,1.0)
		rowReference['initials1'].setTextColor(1.0,1.0,1.0,1.0)
		rowReference['initials2'].setTextColor(1.0,1.0,1.0,1.0)
		for initialToCycle in self.initialIndicesToCycle:
			rowReference['initials'+str(initialToCycle)].setTextColor(r,g,b,1.0)

