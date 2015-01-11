import unittest

from app import metric

class MetricTest(unittest.TestCase):

	def test_Euclidian(self):
		x = [1, 2, 3]
		y = [1, 2, 3]

		r = metric.euclidian(x, y)
		self.assertEqual(1, r)

		x = [1, 2, 3]
		y = [1, 2]

		self.assertRaises(KeyError, metric.euclidian, x, y)

	def test_Pearson(self):
		x = [1, 2, 3]
		y = [1, 5, 7]

		r = metric.pearson(x, y)
		self.assertEqual(round(r, 3), 0.982)

		x = [0, 1, 2]
		y = [0, 1]

		# Check if list being of different sizes gets caught.
		self.assertRaises(KeyError, metric.pearson, x, y)

		x = [1, 1, 1]
		y = [2, 2, 2]

		self.assertRaises(ValueError, metric.pearson, x, y)
