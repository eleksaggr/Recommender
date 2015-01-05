import unittest

class InitializationTest(unittest.TestCase):

	def test_Initialization(self):
		self.assertEqual(1 + 1, 2)

	def test_Import(self):
		try:
			import app
		except ImportError:
			self.fail("Was not able to import.")