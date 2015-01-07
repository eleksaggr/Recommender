import unittest

from app import loader
from app import core

class CoreTest(unittest.TestCase):

	def test_Recommend(self):
		ml = loader.MongoLoader()

		p = ml.loadSample('development', 'user', 'rating', 2)

		print(core.recommend(p, p.keys()[0]))
