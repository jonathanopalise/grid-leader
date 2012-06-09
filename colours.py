class Colours(object):

	black=0,0,0
	lightGreen=143/255,255/255,112/255
	yellow=255/255,255/255,112/255
	white=255/255,255/255,255/255
	pink=255/255,255/143,255/174
	red=255/255,31/255,67/255

	@staticmethod
	def getCyclingColours():
		return [Colours.black,
				Colours.lightGreen,
				Colours.yellow,
				Colours.white,
				Colours.pink,
				Colours.red]
