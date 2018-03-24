import os
from datetime import datetime
from json import dump, loads, load
from json.decoder import JSONDecodeError
import random
from timeit import default_timer as timer
from database import db

from album import Album
from person import Person


from CONFIG import *

def album_structure():
	albums = []
	for dirpath, dirnames, filenames in os.walk(FOLDER):
		albums.extend(dirnames)
		break
	for album in albums:
		if Album.query.filter_by(name=album).first() is None:
			a = Album(album, None)
			db.session.add(a)
	db.session.commit()

def get_models():
	names = []
	for dirpath, dirnames, filenames in os.walk('faces'):
		names.extend(dirnames)
		break
	faces = {}
	for n in names:
		if Person.query.filter_by(name=n).first() is None:
			p = Person(n)
			db.session.add(p)
	db.session.commit()

def initdb():
	db.reflect()
	db.drop_all()
	db.create_all()
	db.session.commit()


def update(app):
	if False:
		with app.app_context():
			initdb()
			album_structure()
			get_models()
	else:
		pass
