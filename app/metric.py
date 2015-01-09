from operator import itemgetter

def euclidian(x, y):
	"""
	Calculates the n-dimensional euclidian distance between x and y.

	Parameters
	==========
	x -> [Rating(...)] - A one-dimensional list of Ratings.

	y -> [Rating(...)] - A one-dimensional list of Ratings.
	==========

	Returns
	==========
	A value between 0 and 1 that shows how similar x and y are.
	1 - equal
	0 - different
	==========
	"""
	if len(x) == 0 or len(y) == 0:
		raise KeyError('X and/or Y may not be empty.')

	mutual = _mutual(x, y)

	s = sum(((x[i].value - y[i].value) ** 2) for i in range(len(mutual)))
	return 1/(1 + s ** 0.5)

def pearson(x, y):
	if len(x) == 0 or len(y) == 0:
		raise KeyError('X and/or Y may not be empty.')

	mutual = _mutual(x, y)

	# Remove all items that are not in both lists.
	x = [item for item in x if item.movieId in mutual]
	y = [item for item in y if item.movieId in mutual]

	# Sort so both lists will be in the same order.
	x = sorted(x, key=itemgetter(0))
	y = sorted(y, key=itemgetter(0))

	# Calculate average for both lists.
	avgX = float(sum(rating.value for rating in x)) / float(len(x))
	avgY = float(sum(rating.value for rating in y)) / float(len(y))

	print(sum(rating.value for rating in y))
	print(len(y))

	dP = 0
	dxSquare = 0
	dySquare = 0
	for i in range(len(mutual)):
		dx = x[i].value - avgX
		dy = y[i].value - avgY
		dP += dx * dy
		dxSquare += dx ** 2
		dySquare += dy ** 2

	if(dxSquare == 0 or dySquare == 0):
		raise ValueError('Could not compute Pearson coefficent for given input.')

	return dP / (dxSquare * dySquare) ** 0.5

def _mutual(x, y):
	if len(x) == 0 or len(y) == 0:
		raise KeyError('X and/or Y may not be empty.')

	xMovies = [movie.movieId for movie in x]
	yMovies = [movie.movieId for movie in y]

	return [movie for movie in xMovies if movie in yMovies]