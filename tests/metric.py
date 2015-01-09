import unittest

from app import metric
from app import loader

class MetricTest(unittest.TestCase):

	def test_Pearson(self):
		x = [loader.Rating(1, 1), loader.Rating(2, 2), loader.Rating(3, 3)]
		y = [loader.Rating(1, 1), loader.Rating(2, 5), loader.Rating(3, 7)]

		r = metric.pearson(x, y)
		print(r)
		self.assertEqual(round(r, 3), 0.982)