from collections import namedtuple

import random
import pymongo as mongo
import pymongo.errors as error

class MongoLoader:

	def __init__(self, host='localhost', port=27017):
		"""
		Initializes a new MongoLoader object and connects to the MongoDB server
		with the given credentials.

		Parameters
		==========
		host -> String: The hostname of the MongoDB server.

		port -> int: The port of the MongoDB server.
		==========

		Throws
		==========
		ValueError: If port is less than 1 or more than 65535.
		==========
		"""

		if port < 1 or port > 65535:
			raise ValueError('Port is out of range.')

		self.client = mongo.MongoClient(host, port)
		self.refs = []

	def fetchRefs(self, db, collection, criteria):
		"""
		Fetches references from the specified collection and adds them to the pool.

		Parameters
		==========
		db -> String: The name of the database the references are fetched from.

		collection -> String: The name of the collection the references are fetched from.

		criteria -> String: The critiera to filter with.
		==========

		Throws
		==========
		InvalidName: If the specified database or collection do not exist.
		==========

		Returns
		==========
		The size of the pool of references.
		==========
		"""

		if db not in self.client.database_names():
			raise error.InvalidName('Database does not exist.')

		if collection not in self.client[db].collection_names():
			raise error.InvalidName('Reference collection doest not exist.')

		# Load existing user ids into references list.
		if len(self.refs) == 0:
			maxId = 0
		else:
			# If we already have refs, fetch all that have a higher criteria than the last one in the list.
			maxId = self.refs[-1]


		cursor = self.client[db][collection].find({criteria : {'$gt' : maxId}})

		# Add all new references to the list.
		self.refs += [ref[criteria] for ref in cursor]

		# Return the number of references in the list.
		return len(self.refs)

	def loadSamples(self, db, sampleCol, n, criteria, constraints={}):
			"""
			Loads the datasets for n references from the database db.
			Which n references will be used is decided at random.

			Parameters
			==========
			db -> String: The name of the database the operation is executed upon.

			sampleCol -> String: The name of the collection that holds the sample data.

			criteria -> String: The criteria by which to filter the items.

			constraints -> {}: A dictionary cotaining fields that should not be loaded. In the form of:
				{field_name : True}, to fetch. And vice versa.

			n -> int: The size of the random sample.
			==========

			Throws
			==========
			ValueError: If the size of the sample is less than 1.

			InvalidName: If the specified database or collection do not exist.
			==========

			Returns
			==========
			A dictionary with the following structure:
			{'criteria' : [item]}
			==========
			"""

			if db not in self.client.database_names():
				raise error.InvalidName('Database does not exist.')

			if sampleCol not in self.client[db].collection_names():
				raise error.InvalidName('Sample collection does not exist.')

			if n < 1:
				raise ValueError('The size of the sample may not be less than 1.')

			# Take a random sample of size n from the reference list.
			sample = random.sample(self.refs, n)

			# Load all items for every reference item in the sample.
			items = {}
			for id in sample:
				items.update({id : self.loadDataset(db, sampleCol, id, criteria, constraints)})

			return items
			
	def loadDataset(self, db, sampleCol, target, criteria, constraints={}):
		"""
		Loads all datasets from the sampleCol collection that fit the property:
			criteria = target

		Parameters
		==========
		db -> String: The name of the database the datasets are loaded from.

		sampleCol -> String: The name of the collection that contains the datasets.

		criteria -> String: The field that is used to filter which datasets are returned.

		constraints -> {}: A dictionary cotaining fields that should not be loaded. In the form of:
			{field_name : False}, to not fetch. And vice versa.

		target -> int: The property that decides if a dataset gets loaded.
		==========

		Throws
		==========
		InvalidName: If the database, or the collection do not exist.

		ValueError: If the target is not yet loaded into the references.
		==========

		Returns
		==========
		A list of datasets as dictionary.
		==========
		"""
		if db not in self.client.database_names():
			raise error.InvalidName('Database does not exist.')

		if sampleCol not in self.client[db].collection_names():
			raise error.InvalidName('Sample collection does not exist.')

		if target not in self.refs:
			raise ValueError('The reference does not exist.')

		cursor = self.client[db][sampleCol].find({criteria : target}, constraints)
		items = [item for item in cursor]

		return items
