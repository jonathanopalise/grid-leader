class LetterGeometry(object):

	gapBetweenWords=1.212
	gapBetweenLetters=0.113
	letterWidth=1.0

	def __init__(self):
		self.cards=[]
		self.currentLeftCursor=0
		self.lastCardWasSpace=False

	def addLetter(self,letter):
		if len(self.cards)>0 and not self.lastCardWasSpace:
			self.currentLeftCursor=self.currentLeftCursor+self.gapBetweenLetters
		self.cards.append({ 'left': self.currentLeftCursor, 'right': self.currentLeftCursor+1, 'letter': letter })
		self.currentLeftCursor=self.currentLeftCursor+self.letterWidth
		self.lastCardWasSpace=False

	def addSpace(self):
		self.currentLeftCursor=self.currentLeftCursor+self.gapBetweenWords
		self.lastCardWasSpace=True

	def getCardGeometry(self):
		halfPhraseWidth=self.currentLeftCursor/2
		halfLetterWidth=self.letterWidth/2
		normalisedCards=[]

		for card in self.cards:
			origin=(card['left']-halfPhraseWidth)+halfLetterWidth
			normalisedCards.append({ 'originx' : origin,
                                     'originy' : 0,
                                     'left': -halfLetterWidth, 
                                     'right': halfLetterWidth, 
                                     'top': -halfLetterWidth, 
                                     'bottom': halfLetterWidth, 
                                     'letter': card['letter']})

		return(normalisedCards)

	@staticmethod
	def getCardGeometryByPhrase(phrase):
		geometry=LetterGeometry()
		for index in range(len(phrase)):
			currentLetter=phrase[index]
			if currentLetter==' ':
				geometry.addSpace()
			else:
				geometry.addLetter(currentLetter)
		return geometry.getCardGeometry()
