import os
from json import dump, load
from album import Album

FOLDER = 'images'

def album_structure():
	albums = []
	for dirpath, dirnames, filenames in os.walk(FOLDER):
		if dirpath != FOLDER:
			albums.append(dirpath)
	data = {i: albums[i] for i in range(len(albums))}
	with open(FOLDER + '/.fetula', 'w') as file:
		dump(data, file)

def get_albums(depth=1):
	with open(FOLDER + '/.fetula', 'r') as file:
		struct = load(file)
	return [Album(k) for k,v in struct.items() if len(v.split('\\')) == depth + 1]