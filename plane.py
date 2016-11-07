import skimage
from skimage import data
from skimage import io
from skimage import measure
from skimage import morphology
from skimage.filters import roberts, sobel, scharr, prewitt
from skimage import feature
from skimage import exposure
from skimage import filters
import os
import numpy as np
from matplotlib import pyplot as plt
import glob
import parameters


def filter(image):
	# GAUSSIAN
	image = filters.gaussian (image, sigma=0.4)

	# EROSION
	working_image = image
	image = morphology.erosion (working_image)  # Erosion shrinks bright regions and enlarges dark regions

	# CANNY
	image = feature.canny(image, sigma=4)

	# DILATION
	working_image = image
	image = morphology.dilation (working_image)

	# Adaptive Equalization
	image = exposure.equalize_adapthist(image, clip_limit=0.1) 	# after canny

	return image


def file_processing (file_name):
	filename = os.path.join (os.getcwd (), file_name)
	image = io.imread (filename, as_grey=True)

	image = filter(image)
	# SAVING OUTPUT:
	output_path = os.path.join(os.getcwd(), "output_for3/")
	if not os.path.exists(output_path):
		os.mkdir(output_path)
	new_path = os.path.join(output_path, os.path.basename(file_name) + parameters.name)
	io.imsave(new_path, image)


def read_files ():
	files_list = glob.glob ("planes/*.jpg")
	for file in files_list:
		file_processing(file)


if __name__ == '__main__':
	read_files ()
