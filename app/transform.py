from collections import namedtuple

Rating = namedtuple('Rating', 'movieId, value')

def toRatings(data):
	
	ratings = {}
	for k in data.keys():
		for entry in data[k]:
			ratings.setdefault(k, [])
			ratings[k].append(Rating(int(entry['movieId']), float(entry['value'])))
	return ratings;