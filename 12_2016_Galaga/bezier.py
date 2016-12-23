from vector2 import Vector2


''' implemented bezier quadratic curve

TO DO: 
- cubic curves
- bezier paths? as a collection of bezier curves? --> alien.getTrajectory()?

- calculate length of curves
- having length, calculate next bezier point on curve since next tick of the clock
- calculate the angle between points accurately, for rotating the alien 

'''
from constants import FPS, ALIENSPEED


# straight line
def bezier1(p0, p1, nrSteps):
    bez_points = []

    for i in range(0, nrSteps):
        t = i / nrSteps
        x = (1 - t) * p0.x + t * p1.x
        y = (1 - t) * p0.y + t * p1.y 
        bez_points.append(Vector2(int(x), int(y)))

    return bez_points


# quadratic curve
def bezier2(p0, p1, p2):
    bez_points = []

    for i in range(0, 51):
        t = i / 50
        x = (1 - t) ** 2 * p0.x + 2 * (1 - t) * t * p1.x + t ** 2 * p2.x
        y = (1 - t) ** 2 * p0.y + 2 * (1 - t) * t * p1.y + t ** 2 * p2.y
        bez_points.append(Vector2(int(x), int(y)))

    return bez_points


def calculateBezierPoint(p0, p1, p2, p3, t):
    ''' p0 and p3 are the endpoints, p1 and p2 the other control points
        t is a value between 0 and 1, determining the position on the curve
        0 equals p0 and 1 equals p3
    '''
    x = (1 - t) ** 3 * p0.x + 3 * (1 - t) ** 2 * t * p1.x + 3 * (1 - t) * t ** 2 * p2.x + t ** 3 * p3.x
    y = (1 - t) ** 3 * p0.y + 3 * (1 - t) ** 2 * t * p1.y + 3 * (1 - t) * t ** 2 * p2.y + t ** 3 * p3.y
    return Vector2(int(x), int(y))


def findDrawingPoints(p0, p1, p2, p3, t0, t1, insertionIndex, pointList):
    tMid = (t0 + t1) / 2
    lp0 = calculateBezierPoint(p0, p1, p2, p3, t0)
    lp1 = calculateBezierPoint(p0, p1, p2, p3, t1)

    a = (lp0 - lp1).get_magnitude()
    print(a)
    if a <= 1:
        return 0
    
    pMid = calculateBezierPoint(p0, p1, p2, p3, tMid)
    leftDirection = (lp0 - pMid) 
    leftDirection.normalize()
    rightDirection = (lp1 - pMid) 
    rightDirection.normalize()
    
    print(Vector2.dot(leftDirection, rightDirection))
    dotP = Vector2.dot(leftDirection, rightDirection)
    if dotP > -0.99:
        pointsAdded = 0
        pointsAdded += findDrawingPoints(p0, p1, p2, p3, t0, tMid, insertionIndex, pointList)
        
        pointList.insert(len(pointList) - (insertionIndex + pointsAdded), pMid)
        pointsAdded += findDrawingPoints(p0, p1, p2, p3, tMid, t1, insertionIndex + pointsAdded, pointList)
        
        return pointsAdded
        
    return 0
    
    
def findPoints(p0, p1, p2, p3):
    pointList = []
    lp0 = calculateBezierPoint(p0, p1, p2, p3, 0)
    lp1 = calculateBezierPoint(p0, p1, p2, p3, 1)
    pointList.append(lp0)
    pointList.append(lp1)
    
    pointsAdded = findDrawingPoints(p0, p1, p2, p3, 0, 1, 1, pointList)
    
    #assert(pointsAdded + 2 == len(pointList))
    return pointList


class BezierPath(object):

    def __init__(self, vs):
        self.controlPoints = []
        self.controlPoints = [Vector2(*t) for t in vs]


    def getLength(self, p0, p1, p2, p3):
        length_bezier = 0
        points = findPoints(p0, p1, p2, p3)
        
        m0 = points[0]
        for m1 in points[1:]:
            length_bezier += (m1 - m0).get_magnitude()
            m0 = m1
            
        print('length bezier curve: {}'.format(length_bezier))
        return length_bezier
        
        
    '''TO DO: improve BezierPath to include linear and quadratic curves as well,
        maybe by using a list of different size tuples? 2-tuple -> linear,
        3-tuple -> quadratic, and 4-tuple -> cubic?
    '''
    def getDrawingPoints(self, timePassed):
        drawingPoints = []
        
        '''determine length per bezier curve, and so determine segments per curve ...'''
        ''' TBD if calculating segments per curve is actually a good idea, instead of
        calculating the segments for the entire path... possibly jerky movement?'''
        #SEGMENTS_PER_CURVE = 30
        
        for i in range(0, len(self.controlPoints) - 3, 3):
            p0 = self.controlPoints[i]
            p1 = self.controlPoints[i + 1]
            p2 = self.controlPoints[i + 2]
            p3 = self.controlPoints[i + 3]
            
            curveLength = self.getLength(p0, p1, p2, p3)
            speed = ALIENSPEED * timePassed
            SEGMENTS_PER_CURVE = int(curveLength / speed) 
            
            if i == 0:
                drawingPoints.append(calculateBezierPoint(p0, p1, p2, p3, 0))
                
            for j in range(1, SEGMENTS_PER_CURVE + 1):
                t = j / SEGMENTS_PER_CURVE
                drawingPoints.append(calculateBezierPoint(p0, p1, p2, p3, t))
        
        return drawingPoints 