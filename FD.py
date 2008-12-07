class FD:
	"Class representing a functional dependency."
	
	def __init__(self,left,right):
		self.left = left
		self.right = right
	
	def __eq__(self,other):
		if (isinstance(other,FD)):
			return ((self.left == other.left) and (self.right == other.right))
		else:
			return NotImplemented
	
	def __ne__(self,other):
		equal_result = self.__eq__(other)
		if (equal_result is not NotImplemented):
			return not equal_result
		else:
			return NotImplemented
	
	def __str__(self):
		return "%s->%s"%(self.left,self.right)
	
	def __repr__(self):
		return "FD(%s,%s)"%(self.left,self.right)
	
	def __hash__(self):
		return hash(str(self))

def _test():
	import doctest
	doctest.testmod()

if __name__ == "__main__":
	_test()