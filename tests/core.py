import unittest

from app import loader
from app import metric
from app import core

class CoreTest(unittest.TestCase):

	def test_Recommend(self):
		ml = loader.MongoLoader()

		p = ml.loadSamples('development', 'user', 'rating', 1000)
		self.assertIsNotNone(p)

		p.update({1 : ml.loadById('development', 'user', 'rating', 10)})

		r = core.recommend(p, 1, similarity=metric.euclidian, k=10000
			)
		print('{0}: {1}'.format(1, r))
