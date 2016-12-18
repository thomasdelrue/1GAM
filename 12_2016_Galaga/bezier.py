from vector2 import Vector2


''' implemented bezier quadratic curve

TO DO: 
- cubic curves
- bezier paths? as a collection of bezier curves? --> alien.getTrajectory()?

- calculate length of curves
- having length, calculate next bezier point on curve since next tick of the clock
- calculate the angle between points accurately, for rotating the alien 

'''
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
    if a < 0.01:
        return 0
    
    pMid = calculateBezierPoint(p0, p1, p2, p3, tMid)
    leftDirection = (lp0 - pMid) 
    leftDirection.normalize()
    rightDirection = (lp1 - pMid) 
    rightDirection.normalize()
    
    print('3v', lp0, lp1, pMid)
    print('l', leftDirection)
    print('r', rightDirection)
    
    print(dot(leftDirection, rightDirection))
    dotP = dot(leftDirection, rightDirection)
    if dotP > -0.99 or abs(tMid - .5) < .0001:
        pointsAdded = 0
        
        pointsAdded += findDrawingPoints(p0, p1, p2, p3, t0, tMid, insertionIndex, pointList)
        
        print('pointList=', pointList)
        print('pMid=', pMid)
        print('insertionIndex={} pointsAdded={}'.format(insertionIndex, pointsAdded))
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
    '''eerst drawing points, dan lengte, dan grootte segment berekenen op basis snelheid, dan de echte te tekenen punten berekenen...'''
    def __init__(self, vs):
        self.controlPoints = []
        self.controlPoints = [Vector2(*t) for t in vs]
        
    def getDrawingPoints(self):
        drawingPoints = []
        
        SEGMENTS_PER_CURVE = 30
        
        for i in range(0, len(self.controlPoints) - 3, 3):
            p0 = self.controlPoints[i]
            p1 = self.controlPoints[i + 1]
            p2 = self.controlPoints[i + 2]
            p3 = self.controlPoints[i + 3]
            
            if i == 0:
                drawingPoints.append(calculateBezierPoint(p0, p1, p2, p3, 0))
                
            for j in range(1, SEGMENTS_PER_CURVE + 1):
                t = j / SEGMENTS_PER_CURVE
                drawingPoints.append(calculateBezierPoint(p0, p1, p2, p3, t))
        
        return drawingPoints 