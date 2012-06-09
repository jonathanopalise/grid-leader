
from panda3d.core import GeomVertexFormat, GeomVertexData
from panda3d.core import Geom, GeomTriangles, GeomVertexWriter, GeomVertexReader
from panda3d.core import Texture, GeomNode
from panda3d.core import Vec3, Vec4, Point3
import math

class ShadowGeometry(object):

	def __init__(self,modelFilename):
		self.createModelClone(modelFilename)

	def setLightPos(self,x,y,z):
		self.lightWorldX=x
		self.lightWorldY=y
		self.lightWorldZ=z

	def setModelPos(self,x,y,z):
		self.modelWorldX=x
		self.modelWorldY=y
		self.modelWorldZ=z

	def setModelRotation(self,rotation):
		self.modelRotation=rotation

	def getSnode(self):
		return self.snode

	def deriveModelVertices(modelFilename):
		newVisualCar = loader.loadModel(modelFilename)
		geomNodeCollection = newVisualCar.findAllMatches('**/+GeomNode')

		simpleVertices=[]

		for nodePath in geomNodeCollection:
			geomNode = nodePath.node()
			for i in range(geomNode.getNumGeoms()):

				geom = geomNode.getGeom(i)

				vdata = geom.getVertexData()
				vertex = GeomVertexReader(vdata, 'vertex')
				while not vertex.isAtEnd():
					v=vertex.getData3f()
					vertexModelX,vertexModelY,vertexModelZ=v

					simpleVertices.append([vertexModelX,vertexModelY,vertexModelZ])

		self.unmodifiedVertexData=simpleVertices

	def projectVerticesToShadow(self):

		inVertices=self.unmodifiedVertexData
		modelWorldX=self.modelWorldX
		modelWorldY=self.modelWorldY
		modelWorldZ=self.modelWorldZ
		zRotationDegrees=self.modelRotation
		lightWorldX=self.lightWorldX
		lightWorldY=self.lightWorldY
		lightWorldZ=self.lightWorldZ

		zRotationRadians=zRotationDegrees*(math.pi/180.0)
		mathCosZRotationRadians=math.cos(zRotationRadians)
		mathSinZRotationRadians=math.sin(zRotationRadians)

		vdata=self.pandaVertexData
		vertex = GeomVertexWriter(vdata, 'vertex')

		for inVertex in inVertices:
			vertexModelX,vertexModelY,vertexModelZ=inVertex

			vertexModelOldX=vertexModelX
			vertexModelOldY=vertexModelY
			vertexModelX=vertexModelOldX*mathCosZRotationRadians-vertexModelOldY*mathSinZRotationRadians
			vertexModelY=vertexModelOldX*mathSinZRotationRadians+vertexModelOldY*mathCosZRotationRadians

			vertexWorldX=modelWorldX+vertexModelX
			vertexWorldY=modelWorldY+vertexModelY
			vertexWorldZ=modelWorldZ+vertexModelZ
			vertexLightZDiff=vertexWorldZ-lightWorldZ
			shadowVertexX=lightWorldX+((vertexWorldX-lightWorldX)*-lightWorldZ/vertexLightZDiff)
			shadowVertexY=lightWorldY+((vertexWorldY-lightWorldY)*-lightWorldZ/vertexLightZDiff)

			normalisedShadowVertexX=shadowVertexX-modelWorldX
			normalisedShadowVertexY=shadowVertexY-modelWorldY
			normalisedShadowVertexZ=0

			vertex.setData3f(normalisedShadowVertexX,normalisedShadowVertexY,normalisedShadowVertexZ)

	def createModelClone(self,modelFilename):

		newVisualCar = loader.loadModel(modelFilename)
		geomNodeCollection = newVisualCar.findAllMatches('**/+GeomNode')

		simpleTris=[]

		self.unmodifiedVertexData=[]

		for nodePath in geomNodeCollection:
			geomNode = nodePath.node()
			for i in range(geomNode.getNumGeoms()):

				geom = geomNode.getGeom(i)

				vdata = geom.getVertexData()
				vertex = GeomVertexReader(vdata, 'vertex')
				while not vertex.isAtEnd():
					v=vertex.getData3f()
					vertexModelX,vertexModelY,vertexModelZ=v
					self.unmodifiedVertexData.append([vertexModelX,vertexModelY,vertexModelZ])

				for primitiveIndex in range(geom.getNumPrimitives()):
					prim=geom.getPrimitive(primitiveIndex)
					prim=prim.decompose()
					for p in range(prim.getNumPrimitives()):
						s = prim.getPrimitiveStart(p)
						e = prim.getPrimitiveEnd(p)
						singleTriData=[]
						for i in range(s, e):
							vertex.setRow(prim.getVertex(s)) 
							vi = prim.getVertex(i)
							singleTriData.append(vi)
						simpleTris.append(singleTriData)

		simpleVertices=self.unmodifiedVertexData

		format=GeomVertexFormat.getV3()

		vdata=GeomVertexData('shadow', format, Geom.UHDynamic)
		self.pandaVertexData=vdata
		vertex=GeomVertexWriter(vdata, 'vertex')
		for vertexIndex in range(len(simpleVertices)):
			simpleVertex=simpleVertices[vertexIndex]
			vertex.addData3f(0,0,0)

		tris=GeomTriangles(Geom.UHStatic)
		for index in range(len(simpleTris)):
			simpleTri=simpleTris[index]
			tris.addVertex(simpleTri[0])
			tris.addVertex(simpleTri[1])
			tris.addVertex(simpleTri[2])
			tris.closePrimitive()

		shadow=Geom(vdata)
		shadow.addPrimitive(tris)

		snode=GeomNode('shadow')
		snode.addGeom(shadow)

		self.snode=snode

	@staticmethod
	def makeModelShadow(modelFilename,modelX,modelY,modelZ,lightX,lightY,lightZ,rotation):
		bob=ShadowGeometry(modelFilename)
		bob.setModelPos(modelX,modelY,modelZ)
		bob.setModelRotation(rotation)
		bob.setLightPos(lightX,lightY,lightZ)
		bob.projectVerticesToShadow()
		return bob.getSnode()


