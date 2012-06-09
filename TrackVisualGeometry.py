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

def makeTrack(segments):

	format=GeomVertexFormat.getV3t2()

	vdata=GeomVertexData('track', format, Geom.UHStatic)
	vertex=GeomVertexWriter(vdata, 'vertex')
	texcoord=GeomVertexWriter(vdata, 'texcoord')

	vdata2=GeomVertexData('startline', format, Geom.UHStatic)
	vertex2=GeomVertexWriter(vdata2, 'vertex')
	texcoord2=GeomVertexWriter(vdata2, 'texcoord')

	numVertices=0
	twat=0
	for segmentIndex in range(len(segments)):
		currentSegment=segments[segmentIndex]

		if segmentIndex==0:
			nextSegment=segments[segmentIndex+1]
			currentStartLineLeftPoint=Geometry.Point.CreateByInterpolation(currentSegment.getMidPoint(),currentSegment.getLeftPoint(),100,77.5);
			currentStartLineRightPoint=Geometry.Point.CreateByInterpolation(currentSegment.getMidPoint(),currentSegment.getRightPoint(),100,77.5);
			nextStartLineLeftPoint=Geometry.Point.CreateByInterpolation(nextSegment.getMidPoint(),nextSegment.getLeftPoint(),100,77.5);
			nextStartLineRightPoint=Geometry.Point.CreateByInterpolation(nextSegment.getMidPoint(),nextSegment.getRightPoint(),100,77.5);

			vertex2.addData3f(nextStartLineLeftPoint.getX(),nextStartLineLeftPoint.getY(),0)
			vertex2.addData3f(nextStartLineRightPoint.getX(),nextStartLineRightPoint.getY(),0)
			vertex2.addData3f(currentStartLineLeftPoint.getX(),currentStartLineLeftPoint.getY(),0)
			vertex2.addData3f(currentStartLineRightPoint.getX(),currentStartLineRightPoint.getY(),0)
			texcoord2.addData2f(0.0, 0.0)
			texcoord2.addData2f(12.0, 0.0)
			texcoord2.addData2f(0.0, 2.0)
			texcoord2.addData2f(12.0, 2.0)

		vertex.addData3f(currentSegment.leftPoint.getX(),currentSegment.leftPoint.getY(),0)
		vertex.addData3f(currentSegment.rightPoint.getX(),currentSegment.rightPoint.getY(),0)
		texcoord.addData2f(0.0, 1.0/8*float(twat))
		texcoord.addData2f(1.0, 1.0/8*float(twat))
		#print('vertex at '+str(segmentIndex)+' with v='+str(1.0/8*float(twat)))
		numVertices+=2

		twat=twat+1
		if twat==9:		
			#print('surplus at '+str(segmentIndex)+' with v=0.0')
			vertex.addData3f(currentSegment.leftPoint.getX(),currentSegment.leftPoint.getY(),0)
			vertex.addData3f(currentSegment.rightPoint.getX(),currentSegment.rightPoint.getY(),0)
			texcoord.addData2f(0.0, 0.0)
			texcoord.addData2f(1.0, 0.0)
			numVertices+=2
			twat=1

	#print('vertices created: '+str(numVertices))

	tris=GeomTriangles(Geom.UHDynamic)

	bob=0
	vertexOffset=0
	for index in range(len(segments)):

		vertexOffsets=[]
		for innerIndex in range(4):
			offset=vertexOffset+innerIndex
			if offset>numVertices-1:
				offset=offset-numVertices
			vertexOffsets.append(offset)

		tris.addVertex(vertexOffsets[0])
		tris.addVertex(vertexOffsets[1])
		tris.addVertex(vertexOffsets[3])
		tris.closePrimitive()

		tris.addVertex(vertexOffsets[0])
		tris.addVertex(vertexOffsets[3])
		tris.addVertex(vertexOffsets[2])
		tris.closePrimitive()

		vertexOffset+=2

		bob+=1
		if bob==8:
			vertexOffset+=2
			bob=0

	tris2=GeomTriangles(Geom.UHDynamic)
	tris2.addVertex(0)
	tris2.addVertex(3)
	tris2.addVertex(1)
	tris2.closePrimitive()

	tris2.addVertex(0)
	tris2.addVertex(2)
	tris2.addVertex(3)
	tris2.closePrimitive()

	track=Geom(vdata)
	track.addPrimitive(tris)

	startLine=Geom(vdata2)
	startLine.addPrimitive(tris2)

	snode=GeomNode('tarmac')
	snode.addGeom(track)

	snode2=GeomNode('startline')
	snode2.addGeom(startLine)

	returnValues={"tarmac":snode,"startline":snode2}
	return returnValues

	return snode





