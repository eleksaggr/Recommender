from itertools import chain

def mutualRatings(x, y):
	xId = set(item.movieId for item in x)
	yId = set(item.movieId for item in y)

	zId = xId & yId

	t = set()
	mutual = [item.movieId for item in chain(x, y) if item.movieId in zId and item.movieId not in t and not t.add(item.movieId)]

	x = [item.value for item in x if item.movieId in mutual]
	y = [item.value for item in y if item.movieId in mutual]

	if(len(x) == 0 or len(y) == 0):
		raise ValueError('No mutual ratings.')

	return (x, y)