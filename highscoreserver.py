class HighScoreServer(object):

	_instance = None

	@classmethod 
	def getInstance(cls):
		if cls._instance is None:
			cls._instance=HighScoreServerInternal()
		return cls._instance	

class HighScoreServerInternal():

	def __init__(self):
		self.highScores=[]
		scoresFile=open(self.getScoresFilename(),'r')
		line=scoresFile.readline()
		while line!='':
			row=line.split(',')
			self.highScores.append({"initials":row[0],"score":int(row[1])})
			line=scoresFile.readline()
		scoresFile.close()

	def getHighScores(self):
		return self.highScores

	def setHighScores(self,highScores):
		self.highScores=highScores

	def getScoresFilename(self):
		prefix=''
		if base.appRunner:
			prefix=base.appRunner.multifileRoot+'/'
		return prefix+'highscores.txt'

	
