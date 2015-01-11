import unittest

from app import metric

class MetricTest(unittest.TestCase):

	def test_Pearson(self):
		x = [{1 : 1}, {2 : 2}, {3 : 3}]
		x = [{1 : 1}, {2 : 5}, {3 : 7}]

		r = metric.pearson(x, y)
		self.assertEqual(round(r, 3), 0.982)