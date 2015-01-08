import pymongo as mongo
import pymongo.errors as error

from collections import namedtuple
import random

Rating = namedtuple('Rating', 'movieId, value')

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
		self.users = []

	def _fetchUsers(self, db, collection):
		"""
		Fetches user ids from the specified collection and adds them to self.users.
		Should this have already happened before, this will only add ids higher
		than the highest id yet loaded.

		Parameters
		==========
		db -> String: The name of the database the users are fetched from.

		collection -> String: The name of the collection the users are fetched from.
		==========

		Throws
		==========
		InvalidName: If the specified database or collection do not exist.
		==========
		"""
		# Load existing user ids into users list.
		if len(self.users) == 0:
			maxId = 0
		else:
			# If we already have users, fetch all that have a higher id than the last one in the list.
			maxId = self.users[-1]

		try:
			cursor = self.client[db][collection].find({'_id' : {'$gt' : maxId}})
		except error.InvalidName:
			raise error.InvalidName('Database or collection do not exist.')


		# Add all new Users to the list.
		self.users += [user['_id'] for user in cursor]

	def loadSample(self, db, refCol, sampleCol, n):
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
			{'userId' : [Rating(...)]}
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
				self._fetchUsers(db, refCol)
			except error.InvalidName:
				raise error.InvalidName('Database or Collection do not exist.')

			# Take a random sample of size n from the user list.
			sample = random.sample(self.users, n)

			# Load all ratings for every user in the sample.
			ratings = {}
			for id in sample:
			#	ratings.setdefault(id, [])
			#	cursor = self.client[db][sampleCol].find({'userId' : id})

			#	for rating in cursor:
			#		ratings[id].append(Rating(int(rating['movieId']), float(rating['value'])))

				ratings.update({id : self.loadById(db, refCol, sampleCol, id)})

			return ratings
			
	def loadById(self, db, refCol, sampleCol, targetId):
		
		if db not in self.client.database_names():
			raise error.InvalidName('Database does not exist.')

		if refCol not in self.client[db].collection_names():
			raise error.InvalidName('Reference collection does not exist.')

		if sampleCol not in self.client[db].collection_names():
			raise error.InvalidName('Sample collection does not exist.')

		try:
			self._fetchUsers(db, refCol)
		except error.InvalidName:
			raise error.InvalidName('Database or Collection do not exist.')

		if targetId not in self.users:
			raise ValueError('The user does not exist.')

		ratings = []
		cursor = self.client[db][sampleCol].find({'userId' : targetId})

		ratings = [Rating(int(rating['movieId']), float(rating['value'])) for rating in cursor]

		return ratings