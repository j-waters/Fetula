import os
from datetime import datetime
from json import dump, loads, load
from json.decoder import JSONDecodeError
import face_recognition
import random

from CONFIG import *

def album_structure():
	albums = []
	for dirpath, dirnames, filenames in os.walk(FOLDER):
		if dirpath != FOLDER:
			albums.append(dirpath)
	data = {i: albums[i] for i in range(len(albums))}
	with data_file(FOLDER) as dat:
		dat['albums'] = data

def get_albums(depth=1):
	from album import Album
	with data_file(FOLDER) as dat:
		struct = dat['albums']
	return [Album(k) for k,v in struct.items() if len(v.split('\\')) == depth + 1]

def get_models():
	names = []
	for dirpath, dirnames, filenames in os.walk('faces'):
		names.extend(filenames)
		break
	faces = {}
	for n in names:
		image = face_recognition.load_image_file('faces/' + n)
		encoding = face_recognition.face_encodings(image)[0]
		faces[n.split(".")[0]] = list(encoding)

	with data_file(FOLDER) as dat:
		dat['faces'] = faces


gkey = 0
class data_file:
	def __init__(self, path):
		self.path = path
		global gkey
		gkey += 1
		self.key = gkey
	def __enter__(self):
		# TODO: it's better to ask for forgiveness than permission
		if not os.path.exists(self.path + '/.fetula'):
			self.data = {}
		else:
			with open(self.path + '/.fetula', 'r') as file:
				self.data = load(file)

		return self.data

	def __exit__(self, a, b, c):
		with open(self.path + '/.fetula', 'w') as file:
			dump(self.data, file)


def update():
	if not os.path.exists(FOLDER + '/.fetula') or (datetime.now() - datetime.fromtimestamp(os.path.getmtime(FOLDER + '/.fetula'))).seconds > 3600:
		album_structure()
		get_models()