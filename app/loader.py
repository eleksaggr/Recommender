import pymongo as mongo
import pymongo.errors as error

from collections import namedtuple
import random

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

	def _fetchRefs(self, db, collection, criteria):
		"""
		Fetches reference ids from the specified collection and adds them to self.refs.
		Should this have already happened before, this will only add ids higher
		than the highest id yet loaded.

		Parameters
		==========
		db -> String: The name of the database the references are fetched from.

		collection -> String: The name of the collection the reference are fetched from.

		criteria -> String: The critiera to filter with.
		==========

		Throws
		==========
		InvalidName: If the specified database or collection do not exist.
		==========
		"""
		# Load existing user ids into references list.
		if len(self.refs) == 0:
			maxId = 0
		else:
			# If we already have refs, fetch all that have a higher id than the last one in the list.
			maxId = self.refs[-1]

		try:
			cursor = self.client[db][collection].find({criteria : {'$gt' : maxId}})
		except error.InvalidName:
			raise error.InvalidName('Database or collection do not exist.')


		# Add all new references to the list.
		self.refs += [ref[criteria] for ref in cursor]

	def loadSamples(self, db, refCol, sampleCol, n, criteria, constraints={}):
			"""
			Loads a random sample of ratings from the database db.
			The entries of refCol are used to select a random sample.
			Exactly n entries from refCol will be gotten.
			The sampleCol holds all entries that could be in the sample.

			Parameters
			==========
			db -> String: The name of the database to load from.

			refCol -> String: The name of the reference collection.

			sampleCol -> String: The name of the sample collection.

			criteria -> String: The criteria by which to filter the items.

			constraints -> {}: A dictionary cotaining fields that should not be loaded.

			n -> int: The size of the random sample taken from refCol.
			==========

			Throws
			==========
			ValueError: If n is less than 1.

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

			if refCol not in self.client[db].collection_names():
				raise error.InvalidName('Reference collection does not exist.')

			if sampleCol not in self.client[db].collection_names():
				raise error.InvalidName('Sample collection does not exist.')

			if n < 1:
				raise ValueError('The size of the sample may not be less than 1.')

			try:
				# Should not always be _id.
				self._fetchRefs(db, refCol, '_id')
			except error.InvalidName:
				raise error.InvalidName('Database or Collection do not exist.')

			# Take a random sample of size n from the reference list.
			sample = random.sample(self.refs, n)

			# Load all items for every reference item in the sample.
			items = {}
			for id in sample:
				items.update({id : self.loadById(db, sampleCol, id, criteria, constraints)})

			return items
			
	def loadById(self, db, sampleCol, targetId, criteria, constraints={}):
		"""
		Loads all entries from the sampleCol collection with the property:
			criteria = targetId

		Parameters
		==========
		db -> String: The name of the database to perform this operation on.

		sampleCol -> String: The name of the collection that contains the sample data.

		criteria -> String: The critiera field that is used to filter the items.

		constraints -> {}: A dictionary cotaining fields that should not be loaded.

		targetId -> int: The id of the target.
		==========

		Throws
		==========
		InvalidName: If the database, or the sampleCol do not exist.

		ValueError: If the target with the id targetId does not exist in the
					references list.
		==========

		Returns
		==========
		A list of items fetched for the specified id.
		==========
		"""
		if db not in self.client.database_names():
			raise error.InvalidName('Database does not exist.')

		if sampleCol not in self.client[db].collection_names():
			raise error.InvalidName('Sample collection does not exist.')

		if targetId not in self.refs:
			raise ValueError('The reference does not exist.')

		cursor = self.client[db][sampleCol].find({criteria : targetId}, constraints)
		items = [item for item in cursor]

		return items