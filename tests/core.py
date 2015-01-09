import unittest

from app import loader
from app import core

class CoreTest(unittest.TestCase):

	def test_Recommend(self):
		ml = loader.MongoLoader()

		p = ml.loadSamples('development', 'user', 'rating', 100)
		self.assertIsNotNone(p)

		p.update({1 : ml.loadById('development', 'user', 'rating', 1)})

		r = core.recommend(p, 1)
		print('{0}: {1}'.format(1, r))
