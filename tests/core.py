import unittest

from app import loader
from app import metric
from app import core
from app import transform

class CoreTest(unittest.TestCase):

	def test_Recommend(self):
		ml = loader.MongoLoader()

		ml.fetchRefs('development', 'user', '_id')

		p = ml.loadSamples('development', 'rating', 100, 'userId', {'_id' : False, 'userId' : False, 'timestamp': False, 'random' : False} )
		p.update({1 : ml.loadDataset('development', 'rating', 10, 'userId', {'_id' : False, 'userId' : False, 'timestamp': False, 'random' : False})})

		p = transform.toRatings(p)

		r = core.recommend(p, 1, similarity=metric.euclidian)
		print(r)
