from operator import itemgetter

def euclidian(x, y):
	"""
	Calculates the n-dimensional euclidian distance between x and y.

	Parameters
	==========
	x -> [float] - A one-dimensional list of floats.

	y -> [float] - A one-dimensional list of floats.
	==========

	Throws
	==========
	KeyError: If x and/or y are empty or not of the same length.
	==========

	Returns
	==========
	A value between 0 and 1 that shows how similar x and y are.
	1 - equal
	0 - different
	==========
	"""
	if len(x) == 0 or len(y) == 0 or len(x) != len(y):
		raise KeyError('X and/or Y may not be empty and must have the same length.')

	# Compute the square of the sums of X and Y
	s = sum(((x[i] - y[i]) ** 2) for i in range(len(x)))

	return 1/(1 + s ** 0.5)

def pearson(x, y):
	"""
	Computes the pearson correlation coefficient between x and y.

	Parameters
	==========
	x -> [float]: A one-dimensional list of floats.

	y -> [float]: A one-dimensional list of floats.
	==========

	Throws
	==========
	KeyError: If x and/or y are empty or not of the same length.
	==========

	Returns
	==========
	A value between -1 and 1 that shows how similar x and y are.
	1 - equal
	-1 - different
	==========
	"""
	if len(x) == 0 or len(y) == 0 or len(x) != len(y):
		raise KeyError('X and/or Y may not be empty and must have the same length.')

	# Calculate average for both lists.
	avgX = float(sum(item for item in x)) / float(len(x))
	avgY = float(sum(item for item in y)) / float(len(y))

	dProduct = 0
	dxSquare = 0
	dySquare = 0
	for i in range(len(x)):
		dx = x[i] - avgX
		dy = y[i] - avgY
		dProduct += dx * dy
		dxSquare += dx ** 2
		dySquare += dy ** 2

	if(dxSquare == 0 or dySquare == 0):
		raise ValueError('Could not compute Pearson coefficent for given input.')

	return dProduct / (dxSquare * dySquare) ** 0.5