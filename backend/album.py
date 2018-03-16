import os
from datetime import datetime
from functools import reduce
from json import load, dump
from timeit import default_timer as timer
from profiler import profile
import inspect

import sys

FOLDER = "images"

class Album:
	def __init__(self, key=None, path=None):
		t = timer()
		self.key = key
		self.path = path
		if self.key is not None:
			self.get_path()
		#print("album", self.key)

		if self.path is not None:
			self.get_key()
		self.name = self.path.split('\\')[-1]
		self.get_data()
		self.scan_photos()
		#print(timer() - t)

	def __repr__(self):
		return "<Album {} id: {}>".format(self.name, self.key)


	def get_path(self):
		with open(FOLDER + '/.fetula', 'r') as file:
			albums = load(file)
		for k, v in albums.items():
			if k == str(self.key):
				self.path = v
		return self.path

	def get_key(self):
		with open(FOLDER + '/.fetula', 'r') as file:
			albums = load(file)

		for k, v in albums.items():
			if v == self.path:
				self.key = k
		return self.key

	def albums(self):
		folders = []
		for dirpath, dirnames, filenames in os.walk(self.path):
			folders.extend(dirnames)
			break

		return [Album(path=self.path + '\\' + folder).key for folder in folders]

	def last_updated(self):
		return datetime.fromtimestamp(os.path.getmtime(self.path + '/.fetula'))


	def scan_photos(self):
		from photo import Photo
		files = []
		for dirpath, dirnames, filenames in os.walk(self.path):
			files.extend(filenames)
			break
		files = [file for file in files if file.split('.')[-1] in ['jpg', 'png', 'JPG'] and file != '.fetula']
		try:
			oldData = self.data
		except:
			oldData = {}
		if len(files) != len(oldData.keys()) or (datetime.now() - self.last_updated()).seconds > 3600:
			newData = []
			for file in files:
				#print(files.index(file), len(files))
				newData.append(Photo(self, file=file).data())
			data = {}
			for p in range(len(newData)):
				data[p] = newData[p]
				for k, v in oldData.items():
					if v['file'] == newData[p]['file'] or v.get('modified', 0) == newData[p]['modified']:
						oldData[k].pop('file')
						oldData[k].pop('modified', None)
						data[p].update(oldData[k].copy())
						oldData.pop(k)
						break

			with open(self.path + '/.fetula', 'w') as file:
				dump(data, file)

			for p in self.photos():
				p.rename()

	def get_data(self):
		with open(self.path + '/.fetula', 'r') as file:
			data = load(file) # type: dict
		self.data = data

	class data_file:
		def __init__(self, path):
			self.path = path
		def __enter__(self):
			with open(self.path + '/.fetula', 'r') as file:
				self.data =  load(file)
				return self.data

		def __exit__(self, a, b, c):
			with open(self.path + '/.fetula', 'w') as file:
				dump(self.data, file)


	def metadata(self):
		return {'name': self.name, 'highlights': list(self.highlights()), 'photos': list(self.data.keys()), 'albums': self.albums(), 'size': self.size(), 'range': self.range()}

	def size(self):
		return len(self.data)

	def photos(self):
		"""curframe = inspect.currentframe()
		calframe = inspect.getouterframes(curframe, 2)
		print("photos", 'caller name:', calframe[1][3])  #"""
		from photo import Photo
		for k in self.data.keys():
			yield Photo(self, k)

	def highlights(self):
		photos = self.photos()

		size = self.size()
		for photo in photos:
			if photo.star or (int(photo.key) % int(size / 8 + 1)) == 0:
				yield photo.key

	def range(self):
		from photo import Photo
		p1 = Photo(self, 0)
		p2 = Photo(self, self.size()-1)
		return [p1.date, p2.date]