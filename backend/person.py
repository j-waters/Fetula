from database import db
import face_recognition
from json import dumps, loads
from sqlalchemy import orm
from numpy import array
import os


class Person(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), nullable=False)

	cover_id = db.Column(db.Integer, db.ForeignKey('encoding.id'))
	cover = db.relationship('Encoding', foreign_keys=[cover_id], post_update=True)

	def __init__(self, name):
		self.name = name
		files = []
		for dirpath, dirnames, filenames in os.walk('faces/' + name):
			files.extend(filenames)
			break
		for file in files:
			e = Encoding(self, file)

		self.cover = self.encodings[0]

	def update(self, data):
		for k, v in data.items():
			if k == "name":
				os.rename('faces/' + self.name, 'faces/' + v)
				self.name = v
		db.session.commit()

	def __repr__(self):
		return "<Person {}>".format(self.name)

class Encoding(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	face_encoding = db.Column(db.String, nullable=False)
	file = db.Column(db.String, nullable=False)

	person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
	person = db.relationship('Person', backref=db.backref('encodings', lazy=True), foreign_keys=[person_id])

	def __init__(self, person, file):
		person.encodings.append(self)
		self.file = file
		image = face_recognition.load_image_file('faces/' + self.person.name + '/' + self.file)
		encoding = face_recognition.face_encodings(image)[0]
		self.face_encoding = dumps(encoding.tolist())

		if Encoding.query.filter_by(face_encoding=self.face_encoding).first is None:
			db.session.add(self)

	@orm.reconstructor
	def loaded(self):
		self.encoding = array(loads(self.face_encoding))

	def __repr__(self):
		return "<Encoding of {}>".format(self.person)

class Face(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	x = db.Column(db.Float)
	y = db.Column(db.Float)
	width = db.Column(db.Float)
	height = db.Column(db.Float)

	distance = db.Column(db.Float, nullable=False)

	person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
	person = db.relationship('Person', backref=db.backref('faces', lazy=True), foreign_keys=[person_id])

	photo_id = db.Column(db.Integer, db.ForeignKey('photo.id'), nullable=False)
	photo = db.relationship('Photo', backref=db.backref('faces', lazy=True), foreign_keys=[photo_id])

	def __init__(self, photo, person, location, distance):
		self.x = location[0]
		self.y = location[1]
		self.width = location[2]
		self.height = location[3]
		self.distance = distance
		photo.faces.append(self)
		person.faces.append(self)

	def data(self):
		return {'name': self.person.name, 'position': (self.x, self.y, self.width, self.height)}

	def __repr__(self):
		return "<Face at {} of {}>".format((self.x, self.y, self.width, self.height), self.person)
