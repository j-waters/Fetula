from flask import Blueprint, jsonify, send_file, request
from io import BytesIO
from timeit import default_timer as timer

from album import Album
from photo import Photo
from photo import Person, Face
import structure
from database import db

from CONFIG import *

api = Blueprint('api', __name__)

@api.route('/api/albums')
def get_albums():
	albums = [a.id for a in Album.query.filter_by(parent=None).all()]
	print(albums)
	return jsonify(albums)

@api.route('/api/database/create')
def create_database():
	db.create_all()
	return "Done"

@api.route('/api/album_data/<int:albumid>/<mode>')
#4y@profile(sort_args=['cumulative'], )
def album_data(albumid, mode):
	album = Album.query.filter_by(id=albumid).first()
	return jsonify(album.data(mode))

def serve_image(image, name):
	byte_io = BytesIO()
	image.save(byte_io, 'PNG')
	byte_io.seek(0)

	return send_file(byte_io, attachment_filename=name)

tim = 0
@api.route('/api/image/<image>/<mode>')
#@profile(sort_args=['cumulative'], )
def fetch_image(image, mode):
	t = timer()
	p = Photo.query.filter_by(id=image).first()
	img = p.resize(mode)
	global tim
	tim += timer() - t
	#print(tim)
	return serve_image(img, p.file)

@api.route('/api/person_image/<name>')
def person_image(name):
	person = Person.query.filter_by(name=name).first()
	return send_file('faces/' + name + '/' + person.cover.file)

@api.route('/api/person_data/<name>')
def person_data(name):
	photos = Photo.query.join(Photo.faces).join(Face.person).filter_by(name=name).all()
	person = Person.query.filter_by(name=name).first()
	return jsonify({'photos': [p.id for p in photos], 'id': person.id})

@api.route('/api/person_names')
def person_names():
	people = Person.query.all()
	return jsonify({'names': [p.name for p in people]})

tim = 0
@api.route('/api/metadata/<image>/<mode>')
#@profile(sort_args=['cumulative'], )
def metadata(image, mode):
	t = timer()
	p = Photo.query.filter_by(id=image).first()
	if mode == 's':
		out = {'date': p.date.isoformat()}
	if mode == 'n':
		out = p.exif_data()
		out['star'] = p.star
	global tim
	tim += timer() - t
	#print(tim)
	return jsonify(out)

@api.route('/api/update_image/<image>', methods=['POST'])
def update_image(image):
	p = Photo.query.filter_by(id=image).first()
	data = request.json
	p.update(data)
	return ""

@api.route('/api/update_album/<album>', methods=['POST'])
def update_album(album):
	a = Album.query.filter_by(id=album).first()
	data = request.json
	a.update(data)
	return ""

@api.route('/api/update_person/<person>', methods=['POST'])
def update_person(person):
	a = Person.query.filter_by(id=person).first()
	data = request.json
	a.update(data)
	return ""