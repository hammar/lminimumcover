import copy
import string

class AttributeSet(set):
	"""
	Class representing a set of attributes that can be part of a functional 
	dependency or relation.
	"""
	
	def __str__(self):
		sortedSelf = list(self)
		sortedSelf.sort()
		return "".join(sortedSelf)
	
	def closure(self,fdset):
		"""
		Calculates closure of an this attribute set over a given set of 
		functional dependencies.
		
		>>> from FD import FD
		>>> from FDset import FDset
		>>> fd1 = FD(AttributeSet('AB'),AttributeSet('E'))
		>>> fd2 = FD(AttributeSet('AG'),AttributeSet('J'))
		>>> fd3 = FD(AttributeSet('BE'),AttributeSet('I'))
		>>> fd4 = FD(AttributeSet('E'),AttributeSet('G'))
		>>> fd5 = FD(AttributeSet('GI'),AttributeSet('H'))
		>>> F = FDset([fd1,fd2,fd3,fd4,fd5])
		
		>>> print AttributeSet('AB').closure(F)
		ABEGIHJ
		>>> print AttributeSet('BE').closure(F)
		IHBEG
		"""
		work = copy.deepcopy(self)
		closed = False
		while not closed:
			closed = True
			for fd in fdset:
				if (work.issuperset(fd.left)) and (not work.issuperset(fd.right)):
					closed = False
					work = work.union(fd.right)
		return work

def _test():
	import doctest
	doctest.testmod()

if __name__ == "__main__":
	_test()