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

