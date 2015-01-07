def euclidian(x, y):
	if len(x) == 0 or len(y) == 0:
		raise KeyError('X and/or Y may not be empty.')

	xMovies = [movie.movieId for movie in x]
	yMovies = [movie.movieId for movie in y]

	mutual = [movie for movie in xMovies if movie in yMovies]

	s = sum(((x[i].value - y[i].value) ** 2) for i in range(len(mutual)))
	return 1/(1 + s ** 0.5)
