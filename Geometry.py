from math import sqrt

class Point(object):
	def __init__(self,x,y):
		self.x=x
		self.y=y

	@staticmethod
	def CreateByInterpolation(point1,point2,totalPoints,currentPoint):
		return Point(point1.x+((point2.x-point1.x)*currentPoint/totalPoints),point1.y+((point2.y-point1.y)*currentPoint/totalPoints))

	def getX(self):
		return self.x

	def getY(self):
		return self.y

	def subtractedFrom(self,point):
		return Point(point.x-self.x,point.y-self.y)

	def addedTo(self,point):
		return Point(self.x+point.x,self.y+point.y)

	def dividedBy(self,num):
		return Point(self.x/num,self.y/num);

	def multipliedBy(self,num):
		return Point(self.x*num,self.y*num);

	def length(self):
		return(sqrt(self.x*self.x+self.y*self.y))

	def normalised(self):
		return(self.dividedBy(self.length()))

	def rotatedLeft(self):
		return(Point(-self.y,self.x))

class CubicBezier(object):
	def __init__(self,control0,control1,control2,control3):
		self.control0=control0
		self.control1=control1
		self.control2=control2
		self.control3=control3

	def getApproximateLength(self):
		points=self.getPoints(100)
		distance=0.0

		for index in range(len(points)-1):
			currentPoint=points[index]
			nextPoint=points[index+1]
			difference=currentPoint.subtractedFrom(nextPoint)
			distance=distance+difference.length()

		return distance	

	def getEvenlySpacedPoints(self,numberOfPoints):
		points=self.getPoints(50000)
		segmentLengths=[]
		newPoints=[]
		totalDistance=0.0

		for index in range(len(points)-1):
			currentPoint=points[index]
			nextPoint=points[index+1]
			difference=currentPoint.subtractedFrom(nextPoint)
			differenceLength=difference.length()
			segmentLengths.append(differenceLength)
			totalDistance=totalDistance+differenceLength

		for currentPoint in range(0,numberOfPoints):

			if currentPoint==numberOfPoints-1:
				newPoints.append(points[len(points)-1])
			else:
				targetDistance=totalDistance/(numberOfPoints-1)*currentPoint
				currentDistance=0.0
				foundCorrectSegment=False
				segmentIndex=0
				while foundCorrectSegment==False:
					if currentDistance+segmentLengths[segmentIndex]>targetDistance:
						newPoints.append(Point.CreateByInterpolation(points[segmentIndex],points[segmentIndex+1],currentDistance+segmentLengths[segmentIndex],targetDistance-currentDistance))
						foundCorrectSegment=True
					currentDistance+=segmentLengths[segmentIndex]
					segmentIndex=segmentIndex+1


		return newPoints

	def getPoints(self,numberOfPoints):
		points=[]

		for currentPoint in range(0,numberOfPoints):
			green1=Point.CreateByInterpolation(self.control0,self.control1,numberOfPoints-1,currentPoint)
			green2=Point.CreateByInterpolation(self.control1,self.control2,numberOfPoints-1,currentPoint)
			green3=Point.CreateByInterpolation(self.control2,self.control3,numberOfPoints-1,currentPoint)
			blue1=Point.CreateByInterpolation(green1,green2,numberOfPoints-1,currentPoint)
			blue2=Point.CreateByInterpolation(green2,green3,numberOfPoints-1,currentPoint)
			bezierPoint=Point.CreateByInterpolation(blue1,blue2,numberOfPoints-1,currentPoint)
			points.append(bezierPoint)

		return points




