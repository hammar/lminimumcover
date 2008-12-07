import copy
from FD import FD

class FDset(set):
	"""
	Class representing a set of functional dependencies.
	"""
	
	def __str__(self):
		output = []
		for fd in self:
			output.append("%s->%s"%(fd.left,fd.right))
		return "\n".join(output)
	
	def equivalent(self,anotherset):
		"""
		Returns true if and only if another set is functionally equivalent 
		with this set.
		
		# Necessary imports
		>>> from FD import FD
		>>> from AttributeSet import AttributeSet
		
		# F is a set of functional dependencies.
		>>> fd1 = FD(AttributeSet('GB'),AttributeSet('AB'))
		>>> fd2 = FD(AttributeSet('AG'),AttributeSet('FB'))
		>>> fd3 = FD(AttributeSet('C'),AttributeSet('D'))
		>>> fd4 = FD(AttributeSet('A'),AttributeSet('FG'))
		>>> F = FDset([fd1,fd2,fd3,fd4])
		
		# The set G is the attribute closed set to F.
		>>> fd5 = FD(AttributeSet('GB'),AttributeSet('GB').closure(F))
		>>> fd6 = FD(AttributeSet('AG'),AttributeSet('AG').closure(F))
		>>> fd7 = FD(AttributeSet('C'),AttributeSet('C').closure(F))
		>>> fd8 = FD(AttributeSet('A'),AttributeSet('A').closure(F))
		>>> G = FDset([fd5,fd6,fd7,fd8])
		
		# F should be functionally equivalent with G.
		>>> F.equivalent(G)
		True
		
		# H is another set of functional dependencies
		>>> fd9 = FD(AttributeSet('D'),AttributeSet('EA'))
		>>> fd10 = FD(AttributeSet('AB'),AttributeSet('C'))
		>>> fd11 = FD(AttributeSet('E'),AttributeSet('B'))
		>>> fd12 = FD(AttributeSet('C'),AttributeSet('D'))
		>>> H = FDset([fd9,fd10,fd11,fd12])
		
		# I is a set which is not equivalent with H.
		>>> fd13 = FD(AttributeSet('C'),AttributeSet('D'))
		>>> fd14 = FD(AttributeSet('D'),AttributeSet('EA'))
		>>> I = FDset([fd13,fd14])
		
		# This should therefore not return true.
		>>> H.equivalent(I)
		False
		"""
		# First check if this set covers other set by trying to infer each 
		# FD in other set from this set.
		for fd in anotherset:
			leftPlusOverSelf = fd.left.closure(self)
			if not leftPlusOverSelf.issuperset(fd.right):
				return False
		# Then do the reverse to check if other set covers this set.
		for fd in self:
			LeftPlusOverOtherSet = fd.left.closure(anotherset)
			if not LeftPlusOverOtherSet.issuperset(fd.right):
				return False
		return True
	
	def AttributeClosedSet(self):
		"""
		Returns the attribute closed set matching this set of functional 
		dependencies.
		
		>>> from FD import FD
		>>> from AttributeSet import AttributeSet
		>>> fd1 = FD(AttributeSet('GB'),AttributeSet('AB'))
		>>> fd2 = FD(AttributeSet('AG'),AttributeSet('FB'))
		>>> fd3 = FD(AttributeSet('C'),AttributeSet('D'))
		>>> fd4 = FD(AttributeSet('A'),AttributeSet('FG'))
		>>> F = FDset([fd1,fd2,fd3,fd4])
		>>> print F.AttributeClosedSet()
		A->ABGF
		AG->ABGF
		C->CD
		BG->ABGF
		"""
		newSet = FDset()
		for fd in self:
			newSet.add(FD(fd.left,fd.left.closure(self)))
		return newSet
	
	def MinimumSet(self):
		"""
		Returns minimum set equivalent, i.e. with any redundant functional 
		dependencies removed.
		
		>>> from FD import FD
		>>> from AttributeSet import AttributeSet
		>>> fd1 = FD(AttributeSet('GB'),AttributeSet('AB'))
		>>> fd2 = FD(AttributeSet('AG'),AttributeSet('FB'))
		>>> fd3 = FD(AttributeSet('C'),AttributeSet('D'))
		>>> fd4 = FD(AttributeSet('A'),AttributeSet('FG'))
		>>> F = FDset([fd1,fd2,fd3,fd4])
		>>> print F.MinimumSet()
		A->ABGF
		BG->ABGF
		C->CD
		"""
		workSet = self.AttributeClosedSet()
		for fd in workSet:
			tempSet = copy.deepcopy(workSet)
			tempSet.remove(fd)
			if tempSet.equivalent(workSet):
				workSet = tempSet
		return workSet
	
	def LMinimumSet(self):
		"""
		Returns L-minimum set equivalent, i.e. with any redundant left hand 
		sides removed from functional dependencies.
		"""
		workSet = self.MinimumSet()
		for fd in workSet:
			for character in fd.left:
				if ((fd.left-set([character])).closure(self) == (fd.left).closure(self)):
					fd.left.remove(character)
		return workSet

def _test():
	import doctest
	doctest.testmod()

if __name__ == "__main__":
	_test()