import numpy as np
from keras.applications.imagenet_utils import preprocess_input
from keras.models import load_model

from rotation_detection.utils import RotNetDataGenerator, angle_error


def predict_rotation(input_path):
	model = load_model('rotation_detection/models/street_view.hdf5', custom_objects={'angle_error': angle_error})

	image_paths = [input_path]

	predictions = model.predict_generator(
		RotNetDataGenerator(
			image_paths,
			input_shape=(224, 224, 3),
			batch_size=64,
			one_hot=True,
			preprocess_func=preprocess_input,
			rotate=False,
			crop_largest_rect=True,
			crop_center=True
		),
		val_samples=len(image_paths)
	)

	predicted_angles = np.argmax(predictions, axis=1)
	return predicted_angles[0]
