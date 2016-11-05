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
	image = filters.gaussian (image, sigma=0.4)
	for i in range(parameters.dil_ero_range):
		working_image = image
		image = morphology.dilation (working_image)
		working_image = image
		image = morphology.erosion (working_image)  # Erosion shrinks bright regions and enlarges dark regions

	# Contrast stretching (smaller range on black)
	p_low, p_heigh = np.percentile (image, (0, 40))		#0, 40
	image = exposure.rescale_intensity (image, in_range=(p_low, p_heigh))

	
	# # # DETECT EDGES:
	# # image = roberts (image)
	# #image = sobel (image)
	# image = feature.canny(image, 6)	# 5
	#
	# # Contrast stretching (smaller range on white)
	# # p_low, p_heigh = np.percentile (image, (90, 100))	#98, 100
	# # image = exposure.rescale_intensity(image, in_range=(p_low, p_heigh))
	#
	# # Adaptive Equalization
	# image = exposure.equalize_adapthist(image, clip_limit=0.1) # 0.07

	return image


def contour_filter(image, original_image):
	# Contours
	contours = measure.find_contours(image, 0.95, fully_connected='high')
	print(len(contours), '\n')
	figure = plt
	fig, ax = figure.subplots()
	ax.imshow (original_image, interpolation='nearest', cmap=plt.cm.gray)
	for n, contour in enumerate (contours):
		ax.plot (contour[:, 1], contour[:, 0], linewidth=2)
	ax.axis ('off')
	return figure


def file_processing (file_name):
	filename = os.path.join (os.getcwd (), file_name)
	original_image = io.imread (filename)
	image = io.imread (filename, as_grey=True)

	image = filter(image)
	# SAVING OUTPUT:
	output_path = os.path.join(os.getcwd(), "output/")
	if not os.path.exists(output_path):
		os.mkdir(output_path)
	new_path = os.path.join(output_path, os.path.basename(file_name) + parameters.name)
	io.imsave(new_path, image)

	# image = contour_filter(image, original_image)
	# # SAVING OUTPUT:
	# output_path = os.path.join(os.getcwd(), "output_2/")
	# if not os.path.exists(output_path):
	# 	os.mkdir(output_path)
	# new_path = os.path.join(output_path, os.path.basename(file_name) + parameters.name)
	# image.savefig(new_path)


def read_files ():
	files_list = glob.glob ("planes/*.jpg")
	for file in files_list:
		file_processing(file)
	#file_processing("planes/samolot04.jpg")



if __name__ == '__main__':
	read_files ()
