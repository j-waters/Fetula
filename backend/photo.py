import os

from PIL import Image
import hashlib
from timeit import timeit
from random import randint
import exifread
from datetime import datetime
from timeit import default_timer as timer
import inspect
from profiler import profile
import io
from fractions import Fraction
from CONFIG import *
from database import db
from sqlalchemy import orm
import face_recognition
from person import Person, Face, Encoding
from dateutil.parser import parse
import cv2
from sqlalchemy import func
#from classify import classify_image
from tag import Object



"""
curframe = inspect.currentframe()
calframe = inspect.getouterframes(curframe, 2)
print('caller name:', calframe[1][3])
"""

class Photo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	file = db.Column(db.String(80), nullable=False)
	star = db.Column(db.Boolean, default=False)
	modified = db.Column(db.DateTime, nullable=False)
	date = db.Column(db.DateTime, nullable=False)

	face_detect = db.Column(db.Boolean, default=False)
	object_detect = db.Column(db.Boolean, default=False)

	width = db.Column(db.Integer, nullable=False)
	height = db.Column(db.Integer, nullable=False)

	album_id = db.Column(db.Integer, db.ForeignKey('album.id'), nullable=False)
	album = db.relationship('Album', backref=db.backref('photos', lazy=True), foreign_keys=[album_id])

	def __init__(self, file, album):
		self.file = file
		album.photos.append(self)

		self.loaded()
		self.modified = datetime.fromtimestamp((os.path.getmtime(self.path)))
		self.date = self.get_date()

		exif = self.exif()
		self.width = exif['EXIF ExifImageLength'][0]
		self.height = exif['EXIF ExifImageWidth'][0]

	@orm.reconstructor
	def loaded(self):
		self.path = self.album.path + '/' + self.file

	def __repr__(self):
		return '<Photo {}>'.format(self.file)

	def get_date(self):
		try:
			date = self.get_exif('EXIF DateTimeOriginal')
		except KeyError:
			date = self.get_exif('Image DateTime')

		return datetime.strptime(date, '%Y:%m:%d %H:%M:%S')

	def resize(self, mode):
		SIZES = {'xs': 16, 's': 128, 'm': 256, 'l': 770}
		# SIZES = {'xs': 15, 's': 120, 'm': 240, 'l': 770}
		baseheight = SIZES[mode]
		if baseheight < 200:
			img = self.get_thumbnail()
			method = Image.NEAREST
		else:
			img = Image.open(self.path)
			method = Image.ANTIALIAS
		img = self.rotate(img)
		hpercent = (baseheight / float(img.size[1]))
		wsize = int((float(img.size[0]) * float(hpercent)))
		img = img.resize((wsize, baseheight), method)
		return img

	"""def ratio(self):
		exif = self.exif()
		h = exif['EXIF ExifImageLength'][0]
		w = exif['EXIF ExifImageWidth'][0]
		o = exif['Image Orientation'][0]
		f =  Fraction(w, h)
		if o in [6, 8]:
			f = 1/f
		return str(f.numerator) + "x" + str(f.denominator)"""

	def rotate(self, img):
		ORIENTATIONS = {
			3: ("Rotated 180 degrees", Image.ROTATE_180),
			6: ("Rotated 90 degrees", Image.ROTATE_270),
			8: ("Rotated 270 degrees", Image.ROTATE_90)
		}
		try:
			orientation = self.get_exif('Image Orientation')[0]
		except KeyError:
			return img
		if orientation in [3, 6, 8]:
			degrees = ORIENTATIONS[orientation][1]
			img = img.transpose(degrees)
			return img
		else:
			return img

	def rename(self):
		if self.path.split(".")[-1] in ['jpg', 'JPG']:
			ext = 'jpg'
		else:
			ext = self.path.split(".")[-1]
		name = self.date.strftime("%Y_%m_%d %H-%M-%S") + "." + ext
		if name != self.file:
			for add in ['a', 'b', 'c', 'd', 'e', 'f', 'g']:
				try:
					os.rename(self.path, self.album.path + '/' + name)
					return
				except FileExistsError:
					name = self.date.strftime("%Y_%m_%d %H-%M-%S") + add + "." + ext

	def exif(self):
		with open(self.path, 'rb') as f:
			return {k: v.values for k,v in exifread.process_file(f, details=False).items()}

	def get_exif(self, tag):
		with open(self.path, 'rb') as f:
			return exifread.process_file(f, details=False, stop_tag=tag)[tag].values

	def get_thumbnail(self):
		with open(self.path, 'rb') as f:
			t =  exifread.process_file(f, details=True, stop_tag='JPEGThumbnail')['JPEGThumbnail']
			return Image.open(io.BytesIO(t))

	def gen_hash(self):
		img = Image.open(self.path).convert('RGBA')
		m = hashlib.md5()
		m.update(img.tobytes())
		self.hash = m.hexdigest()

	def get_faces(self):
		if not self.face_detect:
			self.face_detect = True
			encodings = Encoding.query.all()
			known_faces = [p.encoding for p in encodings]

			SCALE = 0.25
			image = face_recognition.load_image_file(self.path)
			small_image = cv2.resize(image, (0, 0), fx=SCALE, fy=SCALE)
			height, width, channels = small_image.shape

			face_locations = face_recognition.face_locations(small_image)
			face_encodings = face_recognition.face_encodings(small_image, face_locations)
			if len(face_encodings) == 0:
				return


			face_coords = [(l[3], l[0], l[1] - l[3], l[2] - l[0]) for l in face_locations]
			face_percents = [tuple((round(l[0] / width * 100, 2), round(l[1] / height * 100, 2),
			                        round(l[2] / width * 100, 2), round(l[3] / height * 100, 2))) for l in face_coords]
			matches = [False for i in face_locations]
			for i in range(len(known_faces)):
				known_face_encoding = known_faces[i]
				distances = list(face_recognition.face_distance(face_encodings, known_face_encoding))
				sorted_distances = sorted(distances)
				shortest_distance = sorted_distances[0]
				if shortest_distance < 0.6:
					index = distances.index(shortest_distance)
					location = face_percents[index]
					matches[index] = True
					person = encodings[i].person
					existing = Face.query.filter_by(photo_id=self.id, x=location[0], y=location[1], width=location[2], height=location[3]).first()
					if existing is not None:
						if existing.distance > shortest_distance:
							db.session.delete(existing)
							existing = None
					if existing is None:
						with db.session.no_autoflush:
							f = Face(self, person, location, shortest_distance)
							db.session.add(f)
			for i in range(len(matches)):
				if not matches[i]:
					l = face_locations[i]
					location = face_percents[i]
					distance = 0
					face_img = image[l[0] * 4: l[2] * 4, l[3] * 4: l[1] * 4]
					maxid = db.session.query(func.max(Person.id)).first()[0] + 1
					os.mkdir('faces/Unknown {}'.format(maxid))
					cv2.imwrite('faces/Unknown {}/1.jpg'.format(maxid), cv2.cvtColor(face_img, cv2.COLOR_RGB2BGR))
					with db.session.no_autoflush:
						p = Person('Unknown {}'.format(maxid))
						db.session.add(p)
						f = Face(self, p, location, distance)
						db.session.add(f)
						db.session.commit()
			db.session.commit()

	def exif_data(self):
		self.get_faces()
		exif = self.exif()
		#self.classify()
		out = {}
		out['id'] = self.id
		out['date'] = self.date
		out['make'] = exif['Image Make']
		out['model'] = exif['Image Model']
		out['height'] = exif['EXIF ExifImageLength'][0]
		out['width'] = exif['EXIF ExifImageWidth'][0]
		out['mp'] = round(out['height'] * out['width'] / 1000000, 1)
		out['size'] = os.stat(self.path).st_size
		out['fstop'] = eval(str(exif['EXIF FNumber'][0]))
		out['ISOspeed'] = exif['EXIF ISOSpeedRatings'][0]
		out['flength'] = eval(str(exif['EXIF FocalLength'][0]))
		out['exposure'] = str(exif['EXIF ExposureTime'][0])
		out['name'] = self.file
		out['album'] = {}
		out['album']['name'] = self.album.name
		out['album']['path'] = self.album.path
		out['album']['id'] = self.album.id
		out['album']['range'] = self.album.range()
		out['album']['size'] = self.album.size
		out['album']['cover'] = self.album.cover.id
		out['people'] = [f.data() for f in self.faces]
		out['tags'] = [o.data() for o in self.objects]
		return out

	def update(self, data):
		for k, v in data.items():
			if k == "star":
				self.star = v
			if k == "addPerson":
				person = Person.query.filter_by(name=v['name']).first()
				if person is not None:
					with db.session.no_autoflush:
						f = Face(self, person, [0, 0, 0, 0], 1)
						db.session.add(f)
			if k == "delPerson":
				person = Person.query.filter_by(name=v['name']).first()
				face = Face.query.filter_by(person_id=person.id, photo_id=self.id).first()
				if face is not None:
					db.session.delete(face)
			if k == "changePerson":
				new_person = Person.query.filter_by(name=v['newName']).first()
				old_person = Person.query.filter_by(name=v['oldName']).first()
				face = Face.query.filter_by(person_id=old_person.id, photo_id=self.id).first()
				face.person = new_person

		db.session.commit()

	def classify(self):
		self.object_detect = True
		print("classifying...", self.path)
		objects = classify_image(self.path)
		with db.session.no_autoflush:
			for obj in objects:
				o = Object(self, obj[0], obj[1], obj[2])
				db.session.add(o)
				db.session.commit()
