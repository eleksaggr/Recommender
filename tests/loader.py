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
		
		r = l.loadSample('development', 'user', 'rating', 150)
		self.assertIsNotNone(r)

		self.failUnlessRaises(pymongo.errors.InvalidName, l.loadSample, 'wrong', 'user', 'rating', 150)

		self.failUnlessRaises(pymongo.errors.InvalidName, l.loadSample, 'development', 'wrong', 'rating', 150)

		self.failUnlessRaises(ValueError, l.loadSample, 'development', 'user', 'rating', -1)