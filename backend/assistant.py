import os

import cv2

from database import db


class Similar(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	distance = db.Column(db.Float, nullable=False)

	photo_id = db.Column(db.Integer, db.ForeignKey('photo.id'), nullable=False)
	photo = db.relationship('Photo', foreign_keys=[photo_id])

	similar_id = db.Column(db.Integer, db.ForeignKey('photo.id'), nullable=False)
	similar = db.relationship('Photo', foreign_keys=[similar_id])

	unique_similarity = db.UniqueConstraint('photo_id', 'similar_id', name='unique_similarity')

	def __init__(self, photo, similar):
		self.photo = photo
		self.similar = similar
		self.distance = self.photo.hash - self.similar.hash


def get_similar_groups():
	groups = []
	sims = list(Similar.query.all())
	for s in sims:
		group = [s]
		photos = [s.photo, s.similar]
		for s2 in Similar.query.filter(Similar.id != s.id).all():
			if s2.photo in photos:
				if s2.similar not in photos:
					group.append(s2)
					photos.extend([s2.similar])
				sims.remove(s2)
		groups.append({'parent': group[0].photo.id, 'similar': [(g.similar.id, g.distance) for g in group]})

	print(groups)
	return groups


class PredictedOrientation(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	angle = db.Column(db.Float, nullable=False)

	photo_id = db.Column(db.Integer, db.ForeignKey('photo.id'), nullable=False)
	photo = db.relationship('Photo', foreign_keys=[photo_id])

	def __init__(self, photo, angle):
		self.photo = photo
		self.angle = angle

	def rotation(self):
		if 60 < self.angle < 135:
			return 90
		if 135 < self.angle < 225:
			return 180
		if 225 < self.angle < 300:
			return 270

	def distance(self):
		return abs(self.angle - self.rotation())

	def data(self):
		return {'photo': self.photo.id, 'distance': self.distance(), 'rotation': self.rotation()}


def create_animation(images, fps=15):
	dir_path = '.'
	ext = '.mp4'

	# Determine the width and height from the first image
	image_path = os.path.join(dir_path, images[0])
	frame = cv2.imread(image_path)
	cv2.imshow('video', frame)
	height, width, channels = frame.shape

	# Define the codec and create VideoWriter object
	fourcc = cv2.VideoWriter_fourcc(*'mpv4')  # Be sure to use lower case
	out = cv2.VideoWriter('animation.mp4', fourcc, 6.0, (width, height))

	for image in images:

		image_path = os.path.join(dir_path, image)
		frame = cv2.imread(image_path)

		out.write(frame)  # Write out frame to video

		cv2.imshow('video', frame)
		if (cv2.waitKey(1) & 0xFF) == ord('q'):  # Hit `q` to exit
			break

	# Release everything if job is finished
	out.release()
	cv2.destroyAllWindows()
	print('dunzo')
