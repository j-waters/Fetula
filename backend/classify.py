print("[object detector]", 'starting')
from timeit import default_timer as timer
t = timer()
import numpy as np
import os
import six.moves.urllib as urllib
import tarfile
import tensorflow as tf

from PIL import Image

# This is needed since the notebook is stored in the object_detection folder.
from object_detection.utils import ops as utils_ops
# ## Env setup

# In[9]:


# This is needed to display the images.

###get_ipython().magic('matplotlib inline')

# ## Object detection imports
# Here are the imports from the object detection module.

# In[10]:


from object_detection.utils import label_map_util

# # Model preparation

# ## Variables
#
# Any model exported using the `export_inference_graph.py` tool can be loaded here simply by changing `PATH_TO_CKPT` to point to a new .pb file.
#
# By default we use an "SSD with Mobilenet" model here. See the [detection model zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md) for a list of other models that can be run out-of-the-box with varying speeds and accuracies.

# In[11]:


# What model to download.
MODEL_NAME = 'faster_rcnn_inception_resnet_v2_atrous_lowproposals_oid_2018_01_28'#'ssd_mobilenet_v1_coco_2017_11_17'
MODEL_FILE = MODEL_NAME + '.tar.gz'
DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = 'object_detection/' + MODEL_NAME + '/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join('object_detection/data', 'oid_bbox_trainable_label_map.pbtxt')

NUM_CLASSES = 545

# ## Download Model

# In[12]:
if False:
	print("[object detector]", 'beginning download')

	opener = urllib.request.URLopener()
	opener.retrieve(DOWNLOAD_BASE + MODEL_FILE, 'object_detection/' + MODEL_FILE)
	tar_file = tarfile.open('object_detection/' + MODEL_FILE)
	for file in tar_file.getmembers():
		file_name = os.path.basename(file.name)
		if 'frozen_inference_graph.pb' in file_name:
			tar_file.extract(file, os.getcwd() + '/object_detection')

# ## Load a (frozen) Tensorflow model into memory.

# In[13]:
print("[object detector]", 'loading graph')

detection_graph = tf.Graph()
with detection_graph.as_default():
	od_graph_def = tf.GraphDef()
	with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
		serialized_graph = fid.read()
		od_graph_def.ParseFromString(serialized_graph)
		tf.import_graph_def(od_graph_def, name='')

# ## Loading label map
# Label maps map indices to category names, so that when our convolution network predicts `5`, we know that this corresponds to `airplane`.  Here we use internal utility functions, but anything that returns a dictionary mapping integers to appropriate string labels would be fine

# In[14]:
print("[object detector]", 'mapping labels')

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                            use_display_name=True)
category_index = label_map_util.create_category_index(categories)

print("[object detector]", 'Done in', timer() - t, 'seconds')

def load_image_into_numpy_array(image):
	(im_width, im_height) = image.size
	return np.array(image.getdata()).reshape(
		(im_height, im_width, 3)).astype(np.uint8)

def run_inference_for_single_image(image, graph):
	with graph.as_default():
		with tf.Session() as sess:
			# Get handles to input and output tensors
			ops = tf.get_default_graph().get_operations()
			all_tensor_names = {output.name for op in ops for output in op.outputs}
			tensor_dict = {}
			for key in [
				'num_detections', 'detection_boxes', 'detection_scores',
				'detection_classes', 'detection_masks'
			]:
				tensor_name = key + ':0'
				if tensor_name in all_tensor_names:
					tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(
						tensor_name)
			if 'detection_masks' in tensor_dict:
				# The following processing is only for single image
				detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
				detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])
				# Reframe is required to translate mask from box coordinates to image coordinates and fit the image size.
				real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
				detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
				detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
				detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
					detection_masks, detection_boxes, image.shape[0], image.shape[1])
				detection_masks_reframed = tf.cast(
					tf.greater(detection_masks_reframed, 0.5), tf.uint8)
				# Follow the convention by adding back the batch dimension
				tensor_dict['detection_masks'] = tf.expand_dims(
					detection_masks_reframed, 0)
			image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

			# Run inference
			output_dict = sess.run(tensor_dict,
			                       feed_dict={image_tensor: np.expand_dims(image, 0)})

			# all outputs are float32 numpy arrays, so convert types as appropriate
			output_dict['num_detections'] = int(output_dict['num_detections'][0])
			output_dict['detection_classes'] = output_dict[
				'detection_classes'][0].astype(np.uint8)
			output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
			output_dict['detection_scores'] = output_dict['detection_scores'][0]
			if 'detection_masks' in output_dict:
				output_dict['detection_masks'] = output_dict['detection_masks'][0]
	return output_dict


def resize(img):
	baseheight = 800
	hpercent = (baseheight / float(img.size[1]))
	wsize = int((float(img.size[0]) * float(hpercent)))
	img = img.resize((wsize, baseheight))
	return img

def classify_image(image_path):
	image = Image.open(image_path)
	image = resize(image)
	# the array based representation of the image will be used later in order to prepare the
	# result image with boxes and labels on it.
	image_np = load_image_into_numpy_array(image)
	# Expand dimensions since the model expects images to have shape: [1, None, None, 3]
	# image_np_expanded = np.expand_dims(image_np, axis=0)
	# Actual detection.
	output_dict = run_inference_for_single_image(image_np, detection_graph)
	"""
	output_dict['detection_boxes'],
		output_dict['detection_classes'],
		output_dict['detection_scores'],
	"""
	for i in range(len(output_dict['detection_classes'])):
		if output_dict['detection_scores'][i] > 0.1:
			print("Detected object:", str(category_index[output_dict['detection_classes'][i]]['name']),
			      float(output_dict['detection_scores'][i]) * 100)
			obj = (category_index[output_dict['detection_classes'][i]]['name'], output_dict['detection_scores'][i], output_dict['detection_boxes'][i])
			yield obj
		else:
			print("Discarded object:", str(category_index[output_dict['detection_classes'][i]]['name']),
			      float(output_dict['detection_scores'][i]) * 100)
	# Visualization of the results of a detection.
	##plt.figure(figsize=IMAGE_SIZE)
	##plt.imshow(image_np)
