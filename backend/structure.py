from __future__ import division

import os
from json import dumps
from multiprocessing import Pool, Value
from time import sleep

from CONFIG import *
from album import Album
from database import db
from person import Person
from photo import Photo


def album_structure():
	albums = []
	for dirpath, dirnames, filenames in os.walk(FOLDER):
		albums.extend(dirnames)
		break
	for album in albums:
		cur_alb = Album.query.filter_by(name=album).first()
		if cur_alb is None:
			a = Album(album, None)
			db.session.add(a)

	for album in Album.query.all():
		album.scan()
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


progress = None


def init_worker(args):
	''' store the progress for later use '''
	global progress
	progress = args


def worker(data):
	from server import app
	with app.app_context():
		with db.session.no_autoflush:
			photo = Photo.query.filter_by(id=data['photo']).first()
			options = data['options']
			photo.gen_advanced(options)
			global progress
			# += operation is not atomic, so we need to get a lock:
			with progress.get_lock():
				progress.value += 1


def update():
	if False:
		initdb()
		print("[startup] Generated database\nGetting face models...")
		get_models()
	else:
		pass
	print("[startup] generating album structure")
	album_structure()
	print("[startup] generated album structure")


def compute(options):
	if options['scan']:
		album_structure()
	photos = db.session.query(Photo.id).distinct().all()
	count = len(photos)

	work = [{'photo': p[0], 'options': options} for p in photos]
	global progress
	progress = Value('i', 0)
	yield "data: " + dumps({'done': 0, 'count': count, 'time': 0}) + "\n\n"

	pool = Pool(4, initializer=init_worker, initargs=(progress,))
	pool.map_async(worker, work)

	time = 0
	old_progress = 0
	while True:
		try:
			sleep(1)
			time += 1
			if old_progress != progress.value:
				old_progress = progress.value
				yield "data: " + dumps({'done': progress.value, 'count': count, 'time': time}) + "\n\n"
				if progress.value == count:
					break
		except GeneratorExit:
			# Could use this to continue in background
			pool.terminate()
			pool.join()
			print("STOPPED POOL")
			return

	pool.close()
	pool.join()
	pool.close()
	"""photo.gen_advanced(options)
	yield "data: " + dumps({'id': photo.id, 'count': count,
	                        'people': [{'name': f.person.name, 'confidence':  round((1-f.distance) * 100)} for f in photo.faces],
	                        'tags': [{'name': o.tag.name, 'confidence': round(o.score * 100)} for o in photo.objects],
	                        'similar': 0,
	                        'time': timer() - t}) + "\n\n"
if options['similar']:
	for photo in photos:
		t = timer()
		photo.gen_similar()
		yield "data: " + dumps({'id': photo.id, 'count': count,
		                        'people': [],
		                        'tags': [],
		                        'similar': len(photo.get_similar()),
		                        'time': timer() - t}) + "\n\n"
		                        """
	yield "data: STOP\n\n"
