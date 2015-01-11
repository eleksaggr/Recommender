import unittest

from app import loader
from app import metric
from app import core
from app import transform

class CoreTest(unittest.TestCase):

	def test_Recommend(self):

		# Get data to test with.
		ml = loader.MongoLoader()
		ml.fetchRefs('development', 'user', '_id')
		p = ml.loadSamples('development', 'rating', 20, 'userId', {'_id' : False, 'userId' : False, 'timestamp': False, 'random' : False} )
		p.update({100 : ml.loadDataset('development', 'rating', 100, 'userId', {'_id' : False, 'userId' : False, 'timestamp': False, 'random' : False})})
		p = transform.toRatings(p)

		# Check if correct amount of films is being retruned.
		r = core.recommend(p, 100, similarity=metric.euclidian)
		self.assertEqual(3, len(r))

		r = core.recommend(p, 100, similarity=metric.euclidian, k=5)
		self.assertEqual(5, len(r))

		# Also try pearson metric.
		r = core.recommend(p, 100, similarity=metric.pearson)
		self.assertEqual(3, len(r))

		# Empty population.
		self.assertRaises(ValueError, core.recommend, {}, 100)

		# User not in population.
		self.assertRaises(KeyError, core.recommend, p, -1)

		# No mutual ratings.
		p = {1 : [transform.Rating(1, 1)], 2 : [transform.Rating(2, 1)]}
		r = core.recommend(p, 1)
		self.assertEqual(0, len(r))