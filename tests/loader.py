import unittest

import pymongo.errors
import timeit
from functools import partial

from app import loader

class LoaderTest(unittest.TestCase):

	def test_Initialization(self):
		x = loader.MongoLoader()
		self.assertIsNotNone(x)

		x = loader.MongoLoader('localhost', 27017)
		self.assertIsNotNone(x)

		self.failUnlessRaises(ValueError, loader.MongoLoader, 'localhost', -1)

		self.failUnlessRaises(ValueError, loader.MongoLoader, 'localhost', 100000)

	def test_LoadSample(self):
		l = loader.MongoLoader()
		
		r = l.loadSamples('development', 'user', 'rating', 1, 'userId', {'_id' : False, 'userId' : False, 'timestamp': False, 'random' : False})
		self.assertIsNotNone(r)

		print(r)

		self.failUnlessRaises(pymongo.errors.InvalidName, l.loadSamples, 'wrong', 'user', 'rating', 150, 'userId')

		self.failUnlessRaises(pymongo.errors.InvalidName, l.loadSamples, 'development', 'wrong', 'rating', 150, 'userId')

		self.failUnlessRaises(ValueError, l.loadSamples, 'development', 'user', 'rating', -1, 'userId')