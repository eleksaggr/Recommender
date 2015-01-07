from operator import itemgetter

import metric

def recommend(population, targetId, similarity=metric.euclidian, k=3):
	"""
	Recommends a movie to a user with the id 'targetId'.
	The movie will not have been rated by the targeted user yet.

	Parameters
	==========
	population -> {'userId' : [Rating(...)]}: A population of ratings to compare to.

	targetId -> int: The id of the targeted user.

	similarity -> function: A function that can calculate the similarity between two user
							by using their ratings.
	k -> int: The number of movies the system will recommend.
	==========

	Throws
	==========
	KeyError: If the targeted user is not in the population.

	ValueError: If the population is empty.
	==========

	Returns
	==========
	A list of movies the system recommends.
	The list will be formatted as follows:
	[(movieId, value)]
	==========
	"""
	totalScore = {}
	sumSimilarity = {}


	if len(population) == 0:
		raise ValueError('The population may not be empty.')

	# Check if the targeted user exists in the population.
	if targetId not in population.keys():
		raise KeyError('The targeted users ratings must be in the population.')

	for id in population:

		# Skip the targeted user
		if id == targetId:
			continue
		# Calculate the similarity between the targeted user and the current user.
		score = similarity(population[id], population[targetId])

		# Skip users with a similarity of 0 or less.
		if score <= 0:
			continue

		seenMovies = [rating.movieId for rating in population[targetId]]

		for rating in population[id]:

			# Only select movies the user hasnt rated yet.
			if rating.movieId not in seenMovies:
				totalScore.setdefault(rating.movieId, 0)
				totalScore[rating.movieId] += rating.value * score

				sumSimilarity.setdefault(rating.movieId, 0)
				sumSimilarity[rating.movieId] += score

		rankings = [(id, total/sumSimilarity[id]) for id, total in totalScore.items()]
		rankings = sorted(rankings, reverse=True, key=itemgetter(1))

		return rankings[0:k]
		