import os

from album import Album
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
from faces import get_faces
from structure import data_file
from CONFIG import *

"""
curframe = inspect.currentframe()
calframe = inspect.getouterframes(curframe, 2)
print('caller name:', calframe[1][3])
"""

class Photo:
	#@profile(sort_args=['cumulative'], )
	def __init__(self, album, key=None, file=None):
		self.key = key
		self.file = file
		if type(album) == int:
			self.album = Album(album)
		if type(album) == Album:
			self.album = album

		self.people = []
		self.tags = []
		self.star = False

		if self.file is not None:
			self.path = self.album.path + '/' + self.file
		else:
			if self.key == "A":
				self.key = randint(0, len(self.album.data['photos'].keys()) - 1)
			data = self.stored_data()
			self.star = data['star']
			self.file = data['file']
			self.tags = data['tags']
			self.people = data['people']
			self.path = self.album.path + '/' + self.file
		self.modified = self.get_modified()

		self.date = self.get_date()

	def stored_data(self):
		try:
			if str(self.key) in self.album.data['photos'].keys():
				return self.album.data['photos'][str(self.key)]
			"""else:
				print(self.album.data['photos'], self.key)"""
			return {}
		except KeyError:
			return {}

	def data(self):
		return {'file': self.file, 'date': self.date.strftime('%Y:%m:%d %H:%M:%S'), 'modified': self.modified, 'star': self.star, 'tags': [], 'people': []}

	def get_date(self):
		if 'date' in self.stored_data().keys():
			date = self.stored_data()['date']
		else:
			try:
				date = self.get_exif('EXIF DateTimeOriginal')
			except KeyError:
				date = self.get_exif('Image DateTime')

		return datetime.strptime(date, '%Y:%m:%d %H:%M:%S')

	def gen_hash(self):
		img = Image.open(self.path).convert('RGBA')
		m = hashlib.md5()
		m.update(img.tobytes())
		self.hash = m.hexdigest()

	def get_faces(self):
		return get_faces(self.path)

	def get_modified(self):
		return os.path.getmtime(self.path)

	#@profile(sort_args=['cumulative'], )
	def resize(self, mode):
		SIZES = {'xs': 16, 's': 128, 'm': 256, 'l': 770}
		#SIZES = {'xs': 15, 's': 120, 'm': 240, 'l': 770}
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
			
			192 × 256 
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

	def exif(self):
		with open(self.path, 'rb') as f:
			return {k: v.values for k,v in exifread.process_file(f, details=False).items()}

	def update(self, data):
		with data_file(self.album.path) as d:
			for k, v in data.items():
				d[self.key][k] = v

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

	def get_exif(self, tag):
		with open(self.path, 'rb') as f:
			return exifread.process_file(f, details=False, stop_tag=tag)[tag].values

	def get_thumbnail(self):
		with open(self.path, 'rb') as f:
			t =  exifread.process_file(f, details=True, stop_tag='JPEGThumbnail')['JPEGThumbnail']
			return Image.open(io.BytesIO(t))

	def exif_data(self):
		exif = self.exif()
		out = {}
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
		out['album']['path'] = self.album.path.replace('\\', '/')
		out['album']['id'] = self.album.key
		out['album']['range'] = self.album.range()
		out['album']['size'] = self.album.size()
		out['faces'] = self.get_faces()[0]
		return out