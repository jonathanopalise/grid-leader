import trackgeometry
import Geometry

from direct.directbase import DirectStart
from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from panda3d.core import lookAt
from panda3d.core import GeomVertexFormat, GeomVertexData
from panda3d.core import Geom, GeomTriangles, GeomVertexWriter
from panda3d.core import Texture, GeomNode
from panda3d.core import PerspectiveLens
from panda3d.core import CardMaker
from panda3d.core import Light, Spotlight
from panda3d.core import TextNode
from panda3d.core import Vec3, Vec4, Point3
import sys, os

import math

class MountainsGeometry(object):

	@staticmethod
	def makeMountains():

		format=GeomVertexFormat.getV3t2()
		vdata=GeomVertexData('mountains', format, Geom.UHStatic)
		vertex=GeomVertexWriter(vdata, 'vertex')
		texcoord=GeomVertexWriter(vdata, 'texcoord')

		format2=GeomVertexFormat.getV3c4()
		vdata2=GeomVertexData('sky', format2, Geom.UHStatic)
		vertex2=GeomVertexWriter(vdata2, 'vertex')
		color2=GeomVertexWriter(vdata2, 'color')

		numQuads=32

		angle=0
		textureX=0
		angleAdd=math.pi*2/numQuads
		textureXAdd=1.0/numQuads
		currentQuad=0
		numVertices=0

		while currentQuad<numQuads:
			if currentQuad==0:

				vertexX=math.sin(angle)*3000
				vertexY=math.cos(angle)*3000
				vertex.addData3f(vertexX,vertexY,0.0)
				vertex.addData3f(vertexX,vertexY,360.0)

				texcoord.addData2f(1.0, 0.0)
				texcoord.addData2f(1.0, 1.0)

				numVertices=numVertices+2

			vertexX=math.sin(angle)*3000
			vertexY=math.cos(angle)*3000
		
			vertex.addData3f(vertexX,vertexY,0.0)
			vertex.addData3f(vertexX,vertexY,360.0)

			vertex2.addData3f(vertexX,vertexY,360.0)
			color2.addData4f(45.0/255.0,112.0/255.0,255.0/255.0,1.0)
			#color2.addData4f(1.0,1.0,1.0,1.0)

			#print('created vertex at '+str(vertexX)+','+str(vertexY)+',2')
			#print('created vertex at '+str(vertexX)+','+str(vertexY)+',0')

			texcoord.addData2f(textureX, 0.0)
			texcoord.addData2f(textureX, 1.0)
			#print('texturex is '+str(textureX))

			#print('creating vertices v'+str(numVertices)+' and v'+str(numVertices+1))

			numVertices=numVertices+2
			currentQuad=currentQuad+1
			textureX=textureX+textureXAdd
			angle=angle+angleAdd

		vertex2.addData3f(0.0,0.0,360.0)
		#color2.addData4f(1.0,1.0,1.0,1.0)
		color2.addData4f(45.0/255.0,112.0/255.0,255.0/255.0,1.0)

		currentQuad=0
		currentOffset=2
		tris=GeomTriangles(Geom.UHDynamic)

		#print('creating tris - numVertices is '+str(numVertices))

		while currentQuad<numQuads:

			vertexOffsets=[]
			for innerIndex in range(4):
				offset=currentOffset+innerIndex
				#print('comparing '+str(offset)+' with '+str(numVertices-1))
				if offset>numVertices-1:
					offset=offset-numVertices
				vertexOffsets.append(offset)

			#print('adding tri connecting v'+str(vertexOffsets[0])+', v'+str(vertexOffsets[1])+', v'+str(vertexOffsets[3]))
			#print('adding tri connecting v'+str(vertexOffsets[1])+', v'+str(vertexOffsets[3])+', v'+str(vertexOffsets[2]))

			tris.addVertex(vertexOffsets[0])
			tris.addVertex(vertexOffsets[2])
			tris.addVertex(vertexOffsets[1])
			tris.closePrimitive()

			tris.addVertex(vertexOffsets[1])
			tris.addVertex(vertexOffsets[2])
			tris.addVertex(vertexOffsets[3])
			tris.closePrimitive()

			currentOffset=currentOffset+2
			currentQuad=currentQuad+1

		tris2=GeomTriangles(Geom.UHDynamic)
		currentOffset=1

		numTris=numQuads
		currentTri=0
		while currentTri<numTris:

			tris2.addVertex(numTris)
			tris2.addVertex(currentTri)
			if currentTri==numTris-1:
				tris2.addVertex(0)
			else:
				tris2.addVertex(currentTri+1)
			tris2.closePrimitive()

			currentTri=currentTri+1

		mountains=Geom(vdata)
		mountains.addPrimitive(tris)

		sky=Geom(vdata2)
		sky.addPrimitive(tris2)

		snode=GeomNode('mountains')
		snode.addGeom(mountains)

		snode2=GeomNode('sky')
		snode2.addGeom(sky)

		returnValues={"mountains":snode,"sky":snode2}
		return returnValues





