import face_recognition
import cv2
import os
from structure import data_file
from CONFIG import *

def fetch_models():
	with data_file(FOLDER) as dat:
		faces = dat['faces']
	return faces.keys(), faces.values()

def get_faces(path):
	known_names, known_faces = fetch_models()
	SCALE = 0.25
	image = face_recognition.load_image_file(path)
	small_image = cv2.resize(image, (0, 0), fx=SCALE, fy=SCALE)
	height, width, channels = small_image.shape

	face_locations = face_recognition.face_locations(small_image)
	face_encodings = face_recognition.face_encodings(small_image, face_locations)

	face_names = []
	for face_encoding in face_encodings:
		# See if the face is a match for the known face(s)
		matches = face_recognition.compare_faces(known_faces, face_encoding)
		name = "Unknown"

		# If a match was found in known_face_encodings, just use the first one.
		if True in matches:
			first_match_index = matches.index(True)
			name = known_names[first_match_index]

		face_names.append(name)
	face_coords = [(l[3], l[0], l[1] - l[3], l[2] - l[0]) for l in face_locations]
	face_percents = [tuple((round(l[0]/width * 100, 2), round(l[1]/height * 100, 2), round(l[2]/width * 100, 2), round(l[3]/height * 100, 2))) for l in face_coords]
	return zip(face_percents, face_names)