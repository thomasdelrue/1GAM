import math
import pprint

class Vector2(object):
	def __init__(self, x=0.0, y=0.0):
		self.x = x
		self.y = y
		
	def __str__(self):
		return 'v({}, {})'.format(self.x, self.y)
	
	def __add__(self, other):
		return Vector2(self.x + other.x, self.y + other.y)
	
	def __iter__(self):
		return iter([self.x, self.y])
	
	def __mul__(self, scalar):
		return Vector2(self.x * scalar, self.y * scalar)
	
	def __sub__(self, other):
		return Vector2(self.x - other.x, self.y - other.y)
	
	@staticmethod
	def from_points(p1, p2):
		return Vector2(p2[0] - p1[0], p2[1] - p1[1])
	
	def get_magnitude(self):
		return math.sqrt(self.x ** 2 + self.y ** 2)
	
	def normalize(self):
		magnitude = self.get_magnitude()
		self.x /= magnitude
		self.y /= magnitude
		
	@staticmethod
	def getAngle(va, vb):
		dot = va.x * vb.x + va.y * vb.y
		vam = va.get_magnitude()
		vbm = vb.get_magnitude()
		if vam == 0:
			vam = 1
		if vbm == 0:
			vbm = 1
		cosa = dot / vam / vbm
		res = math.acos(cosa) * 180 / math.pi
		if va.x == 0 and vb.x < 0:
			res = 360 - res
		return res


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

	pprint.pprint(bez_points)
	return bez_points