from operator import itemgetter

import metric

def recommend(population, targetId, similarity=metric.euclidian, k=3):
	totalScore = {}
	sumSimilarity = {}

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