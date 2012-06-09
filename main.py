from panda3d.core import loadPrcFileData 
loadPrcFileData('', "window-type none") 
import direct.directbase.DirectStart 

from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
from direct.interval.IntervalGlobal import *
from sessionmanager import SessionManager

class World(DirectObject):
	def __init__(self):

		base.makeDefaultPipe()
		width=base.pipe.getDisplayWidth()
		height=base.pipe.getDisplayHeight()
		print('screen dimensions are '+str(width)+','+str(height))

		base.windowType = 'onscreen' 
		props=WindowProperties.getDefault()
		props.setSize(width,height)
		props.setFullscreen(True) 
		base.openDefaultWindow(props) 

		PStatClient.connect()
		loadPrcFileData("", "framebuffer-stencil #t")
		self.sessionManager=SessionManager()

		FPS = 60
		globalClock = ClockObject.getGlobalClock() 
		globalClock.setMode(ClockObject.MLimited) 
		globalClock.setFrameRate(FPS)

		taskMgr.add(self.move,"moveTask")

	def move(self, task):

		self.sessionManager.advanceTime()
		return task.cont

w=World()
run()


