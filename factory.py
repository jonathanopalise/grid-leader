from panda3d.core import Geom, GeomTriangles, GeomVertexWriter, GeomVertexReader, GeomVertexRewriter
from carappearance import CarAppearance

class Factory(object):

	@staticmethod
	def Car(carAppearance):

		newVisualCar = loader.loadModel("models/f1car")
		geomNodeCollection = newVisualCar.findAllMatches('**/+GeomNode')

		for nodePath in geomNodeCollection:
			geomNode = nodePath.node()
			for i in range(geomNode.getNumGeoms()):
				geom = geomNode.modifyGeom(i)
				state = geomNode.getGeomState(i)
				vdata = geom.modifyVertexData()
				color = GeomVertexRewriter(vdata, 'color')
				while not color.isAtEnd():
					c = color.getData4f()
					r,g,b,a=c
					#f r==1.0 and g==0.0 and b==0.0:
					#	g=1.0
					#	b=1.0
					if r==0.0 and g==1.0 and b==0.0:
						r=carAppearance[0]
						g=carAppearance[1]
						b=carAppearance[2]
					elif r==1.0 and g==0.0 and b==0.0:
						r=carAppearance[3]
						g=carAppearance[4]
						b=carAppearance[5]
					elif r==1.0 and g==1.0 and b==1.0:
						r=carAppearance[6]
						g=carAppearance[7]
						b=carAppearance[8]
					elif r==1.0 and g==1.0 and b==0:
						r=carAppearance[9]
						g=carAppearance[10]
						b=carAppearance[11]

					#print "c = %s" % (repr(c))
					#print('r='+str(r)+' g='+str(g)+' b='+str(b))
					color.setData4f(r,g,b,1.0)

		return newVisualCar


