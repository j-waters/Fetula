import inspect
import os
from datetime import datetime
from functools import reduce
from json import load, dump
from timeit import default_timer as timer
from profiler import profile
from structure import data_file

import sys

from CONFIG import *

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
		with data_file(FOLDER) as dat:
			albums = dat['albums']
		for k, v in albums.items():
			if k == str(self.key):
				self.path = v
		return self.path

	def get_key(self):
		with data_file(FOLDER) as dat:
			albums = dat['albums']

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
			oldData = self.data['photos']
		except:
			oldData = {}
		if len(files) != len(oldData.keys()) or (datetime.now() - self.last_updated()).seconds > 3600:
			newData = []
			for file in files:
				#print(files.index(file), len(files))
				newData.append(Photo(self, file=file).data())
			data = {}
			for p in range(len(newData)):
				data[str(p)] = newData[p]
				for k, v in oldData.items():
					if v['file'] == newData[p]['file'] or v.get('modified', 0) == newData[p]['modified']:
						oldData[k].pop('file')
						oldData[k].pop('modified', None)
						data[str(p)].update(oldData[k].copy())
						oldData.pop(k)
						break

			with data_file(self.path) as dat:
				dat['photos'] = data
			self.data['photos'] = data

			for p in self.photos():
				p.rename()

	def get_data(self):
		with data_file(self.path) as dat:
			data = dat
		self.data = data


	def metadata(self, mode):
		if mode == 'l':
			return {'name': self.name, 'photos': list(self.data['photos'].keys()), 'albums': self.albums(), 'size': self.size(), 'range': self.range()}
		if mode == 'm':
			return {'name': self.name, 'highlights': list(self.highlights()), 'albums': self.albums(), 'size': self.size(), 'range': self.range()}
		if mode == 's':
			return {'name': self.name, 'size': self.size(), 'range': self.range()}

	def size(self):
		return len(self.data['photos'])

	def photos(self):
		from photo import Photo
		for k in self.data['photos'].keys():
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