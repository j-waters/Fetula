from database import db

class Tag(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30), nullable=False)

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return "<Tag {}>".format(self.name)

class Object(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	x = db.Column(db.Float, nullable=False)
	y = db.Column(db.Float, nullable=False)
	width = db.Column(db.Float, nullable=False)
	height = db.Column(db.Float, nullable=False)
	score = db.Column(db.Float, nullable=False)

	tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), nullable=False)
	tag = db.relationship('Tag', backref=db.backref('objects', lazy=True), foreign_keys=[tag_id])

	photo_id = db.Column(db.Integer, db.ForeignKey('photo.id'), nullable=False)
	photo = db.relationship('Photo', backref=db.backref('objects', lazy=True), foreign_keys=[photo_id])

	def __init__(self, photo, name, score, location):
		tag = Tag.query.filter_by(name=name).first()
		if tag == None:
			tag = Tag(name)
			db.session.add(tag)
		tag.objects.append(self)
		photo.objects.append(self)

		# [ymin, xmin, ymax, xmax]
		self.score = score
		self.x = location[1] * 100
		self.y = location[0] * 100
		self.width = (location[3] - location[1]) * 100
		self.height = (location[2] - location[0]) * 100

	def data(self):
		return {'name': self.tag.name, 'position': (self.x, self.y, self.width, self.height),
		        'confidence': round(self.score * 100)}
