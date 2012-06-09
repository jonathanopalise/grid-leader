import Geometry
import Hardcoded
import math
import os.path

class Segment(object):
	def __init__(self,midPoint,leftPoint,rightPoint,vector):
		self.midPoint=midPoint
		self.leftPoint=leftPoint
		self.rightPoint=rightPoint
		self.vector=vector

	def getMidPoint(self):
		return self.midPoint

	def getLeftPoint(self):
		return self.leftPoint

	def getRightPoint(self):
		return self.rightPoint

	def getVector(self):
		return self.vector

class TrackGeometry(object):

	@staticmethod
	def loadFromFile(filename):
		# load trackPartialBeziers from file

		fileExists=True
		if fileExists:
			trackSegments=[]

			if base.appRunner:
				segmentsFilename=base.appRunner.multifileRoot+'/data/segments.txt'
				print('filename is '+segmentsFilename)
			else:
				segmentsFilename='data/segments.txt'

			segmentsFile=open(segmentsFilename)

			line=segmentsFile.readline()
			while line!='':
				row=line.split(',')
				trackSegments.append(Segment(Geometry.Point(float(row[0]),float(row[1])),
											 Geometry.Point(float(row[2]),float(row[3])),
											 Geometry.Point(float(row[4]),float(row[5])),
											 Geometry.Point(float(row[6]),float(row[7]))
											 ))
				line=segmentsFile.readline()

			segmentsFile.close()
		else:
			controlPoints=Hardcoded.controlPoints()
			cubicBeziers=TrackGeometry.deriveCubicBeziersFromControlPoints(controlPoints)
			trackPoints=TrackGeometry.deriveTrackPointsFromCubicBeziers(cubicBeziers)
			trackPoints=TrackGeometry.setLogicalStartingTrackPoint(trackPoints)
			trackSegments=TrackGeometry.deriveTrackSegmentsFromTrackPoints(trackPoints)

			#segmentsFile=open('segments.txt','w')
			#csvWriter=csv.writer(segmentsFile)
			#for trackSegment in trackSegments:
			#	csvWriter.writerow([trackSegment.getMidPoint().getX(),trackSegment.getMidPoint().getY(),
			#						trackSegment.getLeftPoint().getX(),trackSegment.getLeftPoint().getY(),
			#						trackSegment.getRightPoint().getX(),trackSegment.getRightPoint().getY(),
			#						trackSegment.getVector().getX(),trackSegment.getVector().getY()])	
			#segmentsFile.close()

		newTrack=TrackGeometry()
		newTrack.setTrackSegments(trackSegments)
		return newTrack

	@staticmethod	
	def deriveCubicBeziersFromControlPoints(controlPoints):
		cubicBeziers=[]
		startIndex=1

		while startIndex<len(controlPoints):

			pointOffsets=[]
			for index in range(4):
				pointOffset=startIndex+index
				if pointOffset>len(controlPoints)-1:
					pointOffset-=len(controlPoints)
				pointOffsets.append(pointOffset)

			print('creating bezier from control points: ('+str(pointOffsets[0])+','+str(pointOffsets[1])+','+str(pointOffsets[2])+','+str(pointOffsets[3])+')')

			cubicBeziers.append(Geometry.CubicBezier(controlPoints[pointOffsets[0]],
													 controlPoints[pointOffsets[1]],
													 controlPoints[pointOffsets[2]],
													 controlPoints[pointOffsets[3]]))

			startIndex+=3

		return cubicBeziers
	
	@staticmethod
	def deriveTrackPointsFromCubicBeziers(cubicBeziers):
		trackPoints=[]

		for cubicBezier in cubicBeziers:
			approximateLength=int(cubicBezier.getApproximateLength())
			print "approximate length",approximateLength
			#bezierPoints=cubicBezier.getPoints(approximateLength*3)
			bezierPoints=cubicBezier.getEvenlySpacedPoints(approximateLength)

			bezierPoints.pop()
			for bezierPoint in bezierPoints:
				#print "added point at ",bezierPoint.x,bezierPoint.y
				trackPoints.append(bezierPoint)

		return trackPoints

	@staticmethod
	def setLogicalStartingTrackPoint(trackPoints):
		outTrackPoints=[]

		trackPointIndex=0
		for trackPoint in trackPoints:
			if trackPointIndex>350:
				outTrackPoints.append(trackPoint)
			trackPointIndex=trackPointIndex+1		

		trackPointIndex=0
		for trackPoint in trackPoints:
			if trackPointIndex<=350:
				outTrackPoints.append(trackPoint)
			trackPointIndex=trackPointIndex+1

		return outTrackPoints

	@staticmethod
	def deriveTrackSegmentsFromTrackPoints(trackPoints):
		trackSegments=[]

		trackPointsLength=len(trackPoints)
		for index in range(trackPointsLength):
			currentTrackPoint=trackPoints[index]

			nextTrackPointIndex=index+1
			if nextTrackPointIndex==trackPointsLength:
				nextTrackPointIndex=0

			nextTrackPoint=trackPoints[nextTrackPointIndex]

			normalisedTrackVector=currentTrackPoint.subtractedFrom(nextTrackPoint).normalised()
			#print "normalised vector is ",normalisedTrackVector.getX(),normalisedTrackVector.getY()

			leftPoint=currentTrackPoint.addedTo(normalisedTrackVector.rotatedLeft().multipliedBy(1.0));
			rightPoint=currentTrackPoint.addedTo(normalisedTrackVector.rotatedLeft().multipliedBy(-1.0));

			trackSegments.append(Segment(currentTrackPoint,leftPoint,rightPoint,normalisedTrackVector))

		return trackSegments

	def getTrackSegments(self):

		return self.trackSegments

	def setTrackSegments(self,trackSegments):

		self.trackSegments=trackSegments

	@staticmethod
	def getWorldPositionByTrackPosition(segments,segmentPosition,sidewaysPosition):

		segmentComponents=math.modf(segmentPosition)

		segmentFractional=segmentComponents[0]
		segmentInteger=int(segmentComponents[1])

		firstMidPoint=segments[segmentInteger].getMidPoint()
		firstRightPoint=segments[segmentInteger].getRightPoint()

		firstXpos=firstMidPoint.getX()+(firstRightPoint.getX()-firstMidPoint.getX())*sidewaysPosition
		firstYpos=firstMidPoint.getY()+(firstRightPoint.getY()-firstMidPoint.getY())*sidewaysPosition
		
		segmentIntegerPlusOne=segmentInteger+1
		if segmentIntegerPlusOne==len(segments):
			segmentIntegerPlusOne=0

		secondMidPoint=segments[segmentIntegerPlusOne].getMidPoint()
		secondRightPoint=segments[segmentIntegerPlusOne].getRightPoint()

		secondXpos=secondMidPoint.getX()+(secondRightPoint.getX()-secondMidPoint.getX())*sidewaysPosition
		secondYpos=secondMidPoint.getY()+(secondRightPoint.getY()-secondMidPoint.getY())*sidewaysPosition

		finalXpos=firstXpos+((secondXpos-firstXpos)*segmentFractional)
		finalYpos=firstYpos+((secondYpos-firstYpos)*segmentFractional)

		return {"xpos":finalXpos, "ypos":finalYpos}


		
