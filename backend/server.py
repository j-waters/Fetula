import flask
from flask_cors import CORS
from album import Album
from photo import Photo
import structure
from io import BytesIO
app = flask.Flask(__name__)
from timeit import default_timer as timer
from profiler import profile
from CONFIG import *


CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/api/albums')
def get_albums():
	print("albums")
	#structure.album_structure()
	struct = structure.get_albums(1)
	albums = []
	for album in struct:
		albums.append(album.key)

	print(albums)

	return flask.jsonify(albums)

@app.route('/api/album_data/<int:albumid>/<mode>')
#4y@profile(sort_args=['cumulative'], )
def album_data(albumid, mode):
	album = Album(albumid)
	return flask.jsonify(album.metadata(mode))


def serve_image(image, name):
	byte_io = BytesIO()
	image.save(byte_io, 'PNG')
	byte_io.seek(0)

	return flask.send_file(byte_io, attachment_filename=name)

tim = 0
@app.route('/api/image/<album>/<image>/<mode>')
#@profile(sort_args=['cumulative'], )
def fetch_image(album, image, mode):
	t = timer()
	p = Photo(int(album), image)
	img = p.resize(mode)
	global tim
	tim += timer() - t
	#print(tim)
	return serve_image(img, p.file)

@app.route('/api/person_image/<name>')
def person_image(name):
	return flask.send_file('faces/' + name + '.jpg')

tim = 0
@app.route('/api/metadata/<album>/<image>/<mode>')
#@profile(sort_args=['cumulative'], )
def metadata(album, image, mode):
	t = timer()
	p = Photo(int(album), image)
	if mode == 's':
		out = {'date': p.date.isoformat()}
	if mode == 'n':
		out = p.exif_data()
		out['star'] = p.star
	global tim
	tim += timer() - t
	#print(tim)
	return flask.jsonify(out)

@app.route('/api/update/<album>/<image>', methods=['POST'])
def update(album, image):
	p = Photo(int(album), image)
	data = flask.request.json
	p.update(data)
	return ""


if __name__ == "__main__":
	structure.update()
	app.run(debug=True, threaded=False)