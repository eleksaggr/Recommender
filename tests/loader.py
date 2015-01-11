import unittest

import pymongo.errors
import timeit
from functools import partial

from app import loader

class LoaderTest(unittest.TestCase):

	def test_Initialization(self):
		# Check instancing a new object.
		x = loader.MongoLoader()
		self.assertIsNotNone(x)

		# Check explicitly passing the connection arguments.
		x = loader.MongoLoader('localhost', 27017)
		self.assertIsNotNone(x)

		# Check for port being less than 1
		self.failUnlessRaises(ValueError, loader.MongoLoader, 'localhost', -1)

		# Check for port being greater than 65535
		self.failUnlessRaises(ValueError, loader.MongoLoader, 'localhost', 100000)

	def test_FetchRefs(self):
		l = loader.MongoLoader()

		# Check fetching for references.
		r = l.fetchRefs('development', 'user', '_id')
		self.assertNotEqual(r, 0)

		# No new users should have been added.
		r1 = l.fetchRefs('development', 'user', '_id')
		self.assertEqual(r, r1)

		# Check if wrong database is being caught.
		self.failUnlessRaises(pymongo.errors.InvalidName, l.fetchRefs, 'wrong', 'user', '_id')

		# Check if wrong collection is being caught.
		self.failUnlessRaises(pymongo.errors.InvalidName, l.fetchRefs, 'development', 'wrong', '_id')

	def test_LoadById(self):
		l = loader.MongoLoader()

		r = l.fetchRefs('development', 'user', '_id')

		# Try getting all ratings from the user with the id 1, without any constraints.
		r = l.loadById('development', 'rating', 1, 'userId')
		self.assertNotEqual(0, len(r[0]))

		# Check whether only the right fields are being returned.
		r = l.loadById('development', 'rating', 1, 'userId',  {'_id' : False, 'userId' : False, 'timestamp': False, 'random' : False})
		self.assertEqual(2, len(r[0]))

		# Check if wrong database is being caught.
		self.failUnlessRaises(pymongo.errors.InvalidName, l.loadById, 'wrong', 'rating', 1, 'userId')

		# Check if wrong collection is being caught.
		self.failUnlessRaises(pymongo.errors.InvalidName, l.loadById, 'development', 'wrong', 1, 'userId')

		# Check if user that hasnt been loaded is being caught.
		self.failUnlessRaises(ValueError, l.loadById, 'development', 'rating', -1, 'userId')

	def test_LoadSample(self):
		l = loader.MongoLoader()

		l.fetchRefs('development', 'user', '_id')

		# Check if loading works.
		r = l.loadSamples('development', 'rating', 1, 'userId', {'_id' : False, 'userId' : False, 'timestamp': False, 'random' : False})
		self.assertIsNotNone(r)

		# Check if wrong database is being caught.
		self.failUnlessRaises(pymongo.errors.InvalidName, l.loadSamples, 'wrong', 'rating', 50, 'userId')

		# Check if wrong collection is being caught.
		self.failUnlessRaises(pymongo.errors.InvalidName, l.loadSamples, 'development', 'wrong', 50, 'userId')

		# Check if loading a negative amount is being caught.
		self.failUnlessRaises(ValueError, l.loadSamples, 'development', 'rating', -1, 'userId')