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

	xMovies = [movie.movieId for movie in x]
	yMovies = [movie.movieId for movie in y]

	mutual = [movie for movie in xMovies if movie in yMovies]

	s = sum(((x[i].value - y[i].value) ** 2) for i in range(len(mutual)))
	return 1/(1 + s ** 0.5)
