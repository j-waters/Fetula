import os

import piexif
from PIL import Image, ImageFile

import filelock

ImageFile.LOAD_TRUNCATED_IMAGES = True
import hashlib
import exifread
from datetime import datetime
import io
from fractions import Fraction
from database import db
from sqlalchemy import orm
import face_recognition
from person import Person, Face, Encoding
import imagehash
import cv2
from sqlalchemy import func
from sqlalchemy.orm import deferred
from tag import Object, Tag
from assistant import Similar, PredictedOrientation
from detect_blur import detect_blur

pcount = 0

class Photo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	file = db.Column(db.String(80), nullable=False)
	star = db.Column(db.Boolean, default=False)
	removed = db.Column(db.Boolean, default=False)
	modified = db.Column(db.DateTime, nullable=False)
	date = db.Column(db.DateTime, nullable=False)

	width = db.Column(db.Integer, nullable=False)
	height = db.Column(db.Integer, nullable=False)
	ratio = db.Column(db.String, nullable=False)

	version = db.Column(db.Integer, nullable=False)

	thumbnail = deferred(db.Column(db.String))

	perception_hash = db.Column(db.String(16))

	predicted_orientation = db.relationship("PredictedOrientation", uselist=False, back_populates="photo")

	face_detect = db.Column(db.Boolean, default=False)
	object_detect = db.Column(db.Boolean, default=False)
	rotation_detect = db.Column(db.Boolean, default=False)

	album_id = db.Column(db.Integer, db.ForeignKey('album.id'), nullable=False)
	album = db.relationship('Album', backref=db.backref('photos', lazy=True), foreign_keys=[album_id])

	def __init__(self, file, album):
		self.version = 0
		self.file = file
		album.photos.append(self)

		self.loaded()
		self.gen_basic()

	def gen_basic(self):
		self.version += 1
		self.modified = self.get_modified()
		self.date = self.get_date()
		self.rename()

		with Image.open(self.path) as img:
			self.width = img.size[0]
			self.height = img.size[1]
		self.ratio = self.get_ratio()
		db.session.commit()

	def gen_advanced(self, options={}, force=False):
		opts = {
			'scan': False,
			'thumbnails': False,
			'hashes': False,
			'similar': False,
			'faces': False,
			'objects': False,
			'rotation': False,
			'force': False
		}
		opts.update(options)
		options = opts
		if options['force']: force = True
		if not self.removed:
			if options['faces']: self.gen_faces(force)
			if options['objects']: self.gen_tags(force)
			if options['rotation']: self.detect_orientation(force)
			if options['hashes']:
				self.perception_hash = self.get_perception_hash()
			if options['similar']:
				self.gen_similar()
			if options['thumbnails']:
				self.set_thumbnail(force)
			db.session.commit()

	@orm.reconstructor
	def loaded(self):
		if self.removed:
			self.path = 'bin/' + self.file
		else:
			self.path = self.album.path + '/' + self.file
		if self.perception_hash is not None:
			self.hash = imagehash.hex_to_hash(self.perception_hash)

	def update_modified(self, force=False):
		if not os.path.exists(self.path):
			print("does not exist", self.path)
			db.session.delete(self)
			db.session.commit()
			return
		if self.modified != self.get_modified() or force:
			self.gen_basic()
			self.set_thumbnail()

	def __repr__(self):
		return '<Photo {}>'.format(self.file)

	def get_date(self):
		try:
			date = self.get_exif_tag('EXIF DateTimeOriginal')
		except KeyError:
			date = self.get_exif_tag('Image DateTime')

		return datetime.strptime(date, '%Y:%m:%d %H:%M:%S')

	def get_modified(self):
		return datetime.fromtimestamp((os.path.getmtime(self.path)))

	def resize(self, mode):
		self.orientation()
		SIZES = {'xs': 16, 's': 128, 't': 160, 'm': 256, 'ml': 512, 'l': 770, 'o': 1000}
		# SIZES = {'xs': 15, 's': 120, 'm': 240, 'l': 770}
		baseheight = SIZES[mode]
		if baseheight < 200 and self.ratio != "614x135" and mode != 't':
			img = self.get_thumbnail()
			method = Image.ANTIALIAS
		else:
			img = Image.open(self.path)
			method = Image.ANTIALIAS
		if mode == 'o': return img
		hpercent = (baseheight / float(img.size[1]))
		wsize = int((float(img.size[0]) * float(hpercent)))
		img = img.resize((wsize, baseheight), method)
		return img

	def get_ratio(self):
		f = Fraction(self.width, self.height)
		return str(f.numerator) + "x" + str(f.denominator)

	def set_thumbnail(self, force=True):
		if force or self.thumbnail is None:
			im = self.resize('t')
			output = io.BytesIO()
			im.save(output, 'jpeg')
			output = output.getvalue()
			self.thumbnail = output

	def get_thumbnail(self):
		if self.thumbnail is None:
			self.set_thumbnail()
		return Image.open(io.BytesIO(self.thumbnail))

	def lock(self):
		lockFile = self.path + '.lock'
		self.lock_file = filelock.FileLock(lockFile)
		self.lock_file.acquire(None, 0.05)

	def unlock(self):
		self.lock_file.release()

	def detect_orientation(self, force=False):
		from detect_rotation import predict_rotation
		if not self.rotation_detect or force:
			self.rotation_detect = True
			if PredictedOrientation.query.filter_by(photo_id=self.id).first() is not None:
				if force:
					PredictedOrientation.query.filter_by(photo_id=self.id).delete()
				else:
					return
			angle = predict_rotation(self.path)
			if 60 < angle < 300:
				po = PredictedOrientation(self, angle)
				if po.distance() < 20:
					db.session.add(po)

	def orientation(self, rotate=None):
		self.lock()
		with Image.open(self.path) as im:
			exif_dict = piexif.load(im.info["exif"])
			if rotate is None:
				try:
					orientation = exif_dict["0th"][piexif.ImageIFD.Orientation]
				except KeyError:
					orientation = 1
			else:
				self.rotation_detect = True
				if rotate == "right":
					orientation = 6
				elif rotate == "left":
					orientation = 8
				elif rotate == "flip":
					orientation = 4
				elif rotate == "semi":
					orientation = 3
				else:
					orientation = 1

			if orientation == 1:
				self.unlock()
				return
			elif orientation == 2:
				# Vertical Mirror
				mirror = im.transpose(Image.FLIP_LEFT_RIGHT)
			elif orientation == 3:
				# Rotation 180°
				mirror = im.transpose(Image.ROTATE_180)
			elif orientation == 4:
				# Horizontal Mirror
				mirror = im.transpose(Image.FLIP_TOP_BOTTOM)
			elif orientation == 5:
				# Horizontal Mirror + Rotation 90° CCW
				mirror = im.transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.ROTATE_90)
			elif orientation == 6:
				# Rotation 270°
				mirror = im.transpose(Image.ROTATE_270)
			elif orientation == 7:
				# Horizontal Mirror + Rotation 270°
				mirror = im.transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.ROTATE_270)
			elif orientation == 8:
				# Rotation 90°
				mirror = im.transpose(Image.ROTATE_90)

			exif_dict["0th"][piexif.ImageIFD.Orientation] = 1
			w, h = mirror.size
			exif_dict["0th"][piexif.ImageIFD.XResolution] = (w, 1)
			exif_dict["0th"][piexif.ImageIFD.YResolution] = (h, 1)
			exif_bytes = piexif.dump(exif_dict)
			mirror.save(self.path, exif=exif_bytes)
			mirror.close()
			self.gen_basic()
			self.set_thumbnail()
		self.unlock()

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
					self.file = name
					self.loaded()
					return
				except FileExistsError:
					name = self.date.strftime("%Y_%m_%d %H-%M-%S") + add + "." + ext

	def get_exif(self):
		with open(self.path, 'rb') as f:
			return {k: v.values for k,v in exifread.process_file(f, details=False).items()}

	def get_exif_tag(self, tag):
		with open(self.path, 'rb') as f:
			return exifread.process_file(f, details=False, stop_tag=tag)[tag].values

	def get_crypto_hash(self):
		img = Image.open(self.path).convert('RGBA')
		m = hashlib.md5()
		m.update(img.tobytes())
		return m.hexdigest()

	def get_perception_hash(self, force=False):
		return str(imagehash.phash(Image.open(self.path)))

	def get_blur(self):
		return detect_blur(self.path)

	def gen_faces(self, force=False):
		if not self.face_detect or force:
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
					face_img = image[l[0] * 4 - 5: l[2] * 4 + 10, l[3] * 4 - 5: l[1] * 4 + 10]
					maxid = db.session.query(func.max(Person.id)).first()[0] + 1
					print("lowest id is", maxid)
					os.mkdir('faces/Unknown {}'.format(maxid))
					cv2.imwrite('faces/Unknown {}/1.jpg'.format(maxid), cv2.cvtColor(face_img, cv2.COLOR_RGB2BGR))
					with db.session.no_autoflush:
						p = Person('Unknown {}'.format(maxid))
						print("create person with id", maxid)
						db.session.add(p)
						f = Face(self, p, location, distance)
						db.session.add(f)
						db.session.commit()
			db.session.commit()

	def exif_data(self):
		print("exif", self.width, self.height, self.ratio)
		self.get_blur()
		self.gen_faces()
		self.gen_similar()
		exif = self.get_exif()
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
		out['path'] = os.path.abspath(self.path)
		out['version'] = self.version

		pos = self.album.photos.index(self)
		if pos >= 0:
			out['album']['prev'] = self.album.photos[pos - 1].id
		else:
			out['album']['prev'] = None
		if pos + 1 < self.album.size:
			out['album']['next'] = self.album.photos[pos + 1].id
		else:
			out['album']['next'] = None
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

			if k == "tags":
				current_tags = db.session.query(Tag).filter(Object.tag_id == Tag.id).filter(Object.photo_id == self.id)
				rem_tag = current_tags.filter(~Tag.name.in_(v)).first()
				if rem_tag is not None:
					Object.query.filter_by(tag_id=rem_tag.id, photo_id=self.id).delete()
				else:
					for tag in v:
						if current_tags.filter_by(name=tag).first() is None:
							with db.session.no_autoflush:
								o = Object(self, tag, 1, [0, 0, 0, 0])
								db.session.add(o)

			if k == "delete":
				self.delete()

			if k == "rotate":
				if v == "auto":
					if self.predicted_orientation is None:
						self.detect_orientation(force=True)

					if self.predicted_orientation.rotation() == 90:
						self.orientation(rotate='right')
					elif self.predicted_orientation.rotation() == 270:
						self.orientation(rotate='left')
					elif self.predicted_orientation.rotation() == 180:
						self.orientation(rotate='semi')
				elif v == "delete":
					pass
				else:
					self.orientation(rotate=v)
				if self.predicted_orientation is not None:
					db.session.delete(self.predicted_orientation)


		db.session.commit()

	def gen_tags(self, force=False):
		from classify import classify_image
		if not self.object_detect or force:
			self.object_detect = True
			print("classifying...", self.path)
			objects = classify_image(self.path)
			with db.session.no_autoflush:
				for obj in objects:
					tag = Tag.query.filter_by(name=obj[0]).first()
					if tag is None or Object.query.filter_by(tag_id=tag.id, score=obj[1]).first() is None:
						o = Object(self, obj[0], obj[1], obj[2])
						db.session.add(o)
						db.session.commit()
					else:
						print("Exists:", str(obj[0]))

	def get_similar(self):
		return Similar.query.filter((Similar.photo_id == self.id) | (Similar.similar_id == self.id)).all()

	def gen_similar(self):
		if not self.removed:
			if self.perception_hash is None:
				self.perception_hash = self.get_perception_hash()
			photos = Photo.query.filter(Photo.id != self.id).filter(Photo.removed == False).all()
			existing = Similar.query.filter((Similar.photo_id == self.id) | (Similar.similar_id == self.id))
			for photo in photos:
				if photo.perception_hash is not None:
					distance = self.hash - photo.hash
					if distance < 16:
						if existing.filter((Similar.photo_id == photo.id) | (
									Similar.similar_id == photo.id)).first() is None:
							s = Similar(self, photo)
							db.session.add(s)
			db.session.commit()

	def delete(self):
		if not os.path.exists('bin'):
			os.mkdir('bin')
		os.rename(self.path, 'bin/' + self.file)
		self.removed = True
		Similar.query.filter((Similar.photo_id == self.id) | (Similar.similar_id == self.id)).delete()
		self.path = 'bin/' + self.file
