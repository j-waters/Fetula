from io import BytesIO
from timeit import default_timer as timer

from flask import Blueprint, jsonify, send_file, request, Response, stream_with_context

import structure
from album import Album
from assistant import get_similar_groups, PredictedOrientation, create_animation
from database import db
from photo import Person, Face
from photo import Photo
from tag import Tag

api = Blueprint('api', __name__)

@api.route('/api/albums')
def get_albums():
	albums = [a.id for a in Album.query.filter_by(parent=None).all()]
	return jsonify(albums)


@api.route('/api/home')
def home():
	notifications = len(get_similar_groups())
	notifications += len(PredictedOrientation.query.all())
	return jsonify({'notifications': notifications})


@api.route('/api/assistant')
def assistant():
	similar = get_similar_groups()
	rotations = [r.data() for r in PredictedOrientation.query.all()]
	return jsonify({'similar': similar, 'rotations': rotations})

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


@api.route('/api/tag_names')
def tag_names():
	tags = Tag.query.all()
	return jsonify({'names': [t.name for t in tags]})

tim = 0
@api.route('/api/metadata/<image>/<mode>')
#@profile(sort_args=['cumulative'], )
def metadata(image, mode):
	t = timer()
	p = Photo.query.filter_by(id=image).first()
	p.update_modified()
	if mode == 's':
		out = {'date': p.date.isoformat(), 'ratio': p.ratio, 'version': p.version}
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


@api.route('/api/gen_image/<image>/tags')
def gen_image_tags(image):
	p = Photo.query.filter_by(id=image).first()  # type: Photo
	p.gen_tags(force=True)
	return jsonify([o.data() for o in p.objects])


@api.route('/api/gen_image/<image>/people')
def gen_image_faces(image):
	p = Photo.query.filter_by(id=image).first()  # type: Photo
	p.gen_faces(force=True)
	return jsonify([f.data() for f in p.faces])

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


@api.route('/api/process')
def process():
	options = dict(request.args)
	options = {k: v[0] == 'true' for k, v in options.items()}
	r = Response(stream_with_context(structure.compute(options)), mimetype='text/event-stream')
	return r


@api.route('/api/create_animation', methods=['POST'])
def make_animation():
	data = request.json
	photos = [Photo.query.filter_by(id=p).first().path for p in data['photos']]
	create_animation(photos, 16)
	return ''


@api.before_app_first_request
def initialise():
	structure.update()
	return "Done"
