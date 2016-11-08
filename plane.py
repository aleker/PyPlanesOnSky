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

	# DILATION
	# working_image = image
	# image = morphology.dilation (working_image)

	# Contrast stretching (smaller range on black)
	# im mniejszy range tym bardziej gubią się w chmurach
	p_low, p_heigh = np.percentile (image, (0, 30))  # 0, 40
	image = exposure.rescale_intensity (image, in_range=(p_low, p_heigh))

	# # DETECT EDGES:
	# image = feature.canny(image, 4)	# 5
	#
	# # DILATION
	# working_image = image
	# image = morphology.dilation (working_image)
	#
	# # Adaptive Equalization
	# image = exposure.equalize_adapthist(image, clip_limit=0.8) # after canny 0.07

	return image


def is_close(beginning, ending):
	boundary = 30
	if beginning[0] > ending[0] and (beginning[0] > (ending[0] + boundary)):
		return False
	elif beginning[0] < ending[0] and (beginning[0] + boundary < ending[0]):
		return False
	elif beginning[1] > ending[1] and (beginning[1] > (ending[1] + boundary)):
		return False
	elif beginning[1] < ending[1] and (beginning[1] + boundary < ending[1]):
		return False
	else:
		return True


def contour_filter(image, original_image):
	# CONTOURS
	#contours = measure.find_contours(image, 0.8, fully_connected='high')
	my_contours = []
	# im wyższe tym bardziej reaguje na jasne (robią się pojedyncze krawedzie ale czasem promienie wchodza na samolot
	for contour in measure.find_contours(image, 0.5, fully_connected='high'):
		if len(contour) > 400 and (is_close(contour[0], contour[-1])) is True:
			my_contours.append(contour)
	print(len(my_contours), '\n')

	# PLOT
	figure = plt
	fig, ax = figure.subplots()
	ax.imshow (image, interpolation='nearest', cmap=plt.cm.gray)
	for n, contour in enumerate (my_contours):
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

	image = contour_filter(image, original_image)
	# SAVING OUTPUT:
	output_path = os.path.join(os.getcwd(), "output_2/")
	if not os.path.exists(output_path):
		os.mkdir(output_path)
	new_path = os.path.join(output_path, os.path.basename(file_name) + parameters.name)
	image.savefig(new_path)


def read_files ():
	files_list = glob.glob ("planes/*.jpg")
	for file in files_list:
		file_processing(file)
	#file_processing("planes/samolot04.jpg")



if __name__ == '__main__':
	read_files ()
