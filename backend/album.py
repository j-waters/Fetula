import os

from sqlalchemy import orm, func

from CONFIG import *
from database import db
from photo import Photo


class Album(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)

	cover_id = db.Column(db.Integer, db.ForeignKey('photo.id'))
	cover = db.relationship('Photo', foreign_keys=[cover_id], post_update=True)

	parent_id = db.Column(db.Integer, db.ForeignKey('album.id'), nullable=True)
	parent = db.relationship('Album', backref=db.backref('albums', lazy=True), remote_side=[id])

	def __init__(self, name, parent):
		self.name = name

		if parent is not None:
			parent.albums.append(self)

		self.loaded()
		self.scan()
		self.cover = self.photos[0]

	@orm.reconstructor
	def loaded(self):
		if self.parent == None:
			self.path = FOLDER + '/' + self.name
		else:
			self.path = self.parent.path + '/' + self.name

		self.size = db.session.query(func.count(Photo.id)).filter(Photo.album_id == self.id).scalar()

	def scan(self):
		if not os.path.exists(self.path):
			print("does not exist", self.path)
			for photo in Photo.query.filter_by(album=self).all():
				photo.update_modified()
			db.session.delete(self)
			db.session.commit()
			return
		files = []
		folders = []
		for dirpath, dirnames, filenames in os.walk(self.path):
			files.extend(filenames)
			folders.extend(dirnames)
			break
		files = [file.replace('\\', '/') for file in files if file.split('.')[-1] in ['jpg', 'png', 'JPG']]

		for file in files:
			if Photo.query.filter_by(album=self, file=file).first() is None:
				p = Photo(file, self)
				db.session.add(p)

		for folder in folders:
			if Album.query.filter_by(parent=self, name=folder).first() is None:
				a = Album(folder, self)
				db.session.add(a)

		for photo in Photo.query.filter_by(album=self).all():
			photo.update_modified()
		db.session.commit()

	def __repr__(self):
		return '<Album %r>' % self.name


	def data(self, mode):
		if mode == 'l':
			return {'name': self.name, 'photos': [p.id for p in self.photos], 'albums': [a.id for a in self.albums], 'size': self.size, 'range': self.range()}
		if mode == 'm':
			return {'name': self.name, 'highlights': list(self.highlights()), 'albums': [a.id for a in self.albums], 'size': self.size, 'range': self.range()}
		if mode == 's':
			return {'name': self.name, 'size': self.size, 'range': self.range(), 'cover': self.photos[0].id,
			        'ratio': self.photos[0].ratio}

	def highlights(self):
		photos = self.photos
		for photo in photos:
			if photo.star or (int(photo.id) % int(self.size / 8 + 1)) == 0:
				yield photo.id

	def range(self):
		p1 = self.photos[0]
		p2 = self.photos[-1]
		return [p1.date, p2.date]

	def update(self, data):
		for k, v in data.items():
			if k == "name":
				self.name = v
				if self.parent == None:
					pdir = FOLDER + '/'
				else:
					pdir = self.parent.path + '/'
				os.rename(self.path, pdir + v)
		db.session.commit()