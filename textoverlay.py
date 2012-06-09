from panda3d.core import TextNode

class TextOverlay(object):

	fontScale=0.072
	alignRight=TextNode.ARight
	alignLeft=TextNode.ALeft

	characterWidth=28
	characterHeight=28

	def __init__(self):
		self.font = loader.loadFont('fonts/prstartk.ttf')
		self.containerNode=aspect2d.attachNewNode('container')

	def addText(self,name,text,xpos,ypos,r,g,b,align):
		textNode=TextNode(name)
		textNode.setText(text)
		textNode.setFont(self.font)
		textNode.setTextColor(r,g,b,1.0)
		textNode.setAlign(align)
		textNodePath=self.containerNode.attachNewNode(textNode)
		textNodePath.setScale(self.fontScale)
		textNodePath.setPos((2.0/self.characterWidth*xpos)-1,0.0,(2.0/self.characterHeight*ypos)-1) 
		return textNode

	def show(self):
		self.containerNode.show()

	def hide(self):
		self.containerNode.hide()

	def delete(self):
		self.containerNode.removeNode()

	
