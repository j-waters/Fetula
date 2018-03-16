import flask
from flask_cors import CORS
from album import Album
from photo import Photo
import structure
from io import BytesIO
app = flask.Flask(__name__)
from timeit import default_timer as timer
from profiler import profile


CORS(app, resources={r"/api/*": {"origins": "*"}})

FOLDER = "images"

@app.route('/api/albums')
def get_albums():
	structure.album_structure()
	struct = structure.get_albums(1)
	albums = []
	for album in struct:
		albums.append(album.key)

	print(albums)

	return flask.jsonify(albums)

@app.route('/api/album_data/<int:albumid>')
def album_data(albumid):
	album = Album(albumid)
	return flask.jsonify(album.metadata())


def serve_image(image, name):
	byte_io = BytesIO()
	image.save(byte_io, 'PNG')
	byte_io.seek(0)

	return flask.send_file(byte_io, attachment_filename=name)

tim = 0
@app.route('/api/image/<album>/<image>/<mode>')
def fetch_image(album, image, mode):
	t = timer()
	p = Photo(int(album), image)
	img = p.resize(mode)
	global tim
	tim += timer() - t
	print(tim)
	return serve_image(img, p.file)


@app.route('/api/metadata/<album>/<image>/<mode>')
def metadata(album, image, mode):
	p = Photo(int(album), image)
	if mode == 's':
		out = {'date': p.date.isoformat()}
	if mode == 'n':
		out = p.exif_data()
		out['star'] = p.star

	return flask.jsonify(out)

@app.route('/api/update/<album>/<image>', methods=['POST'])
def update(album, image):
	p = Photo(int(album), image)
	data = flask.request.json
	p.update(data)
	return ""


if __name__ == "__main__":
	app.run(debug=True, threaded=True)