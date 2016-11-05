import skimage
from skimage import data
from skimage import io
from skimage import measure
from skimage import morphology
from skimage.filters import roberts, sobel, scharr, prewitt
from skimage import feature
from skimage import exposure
import os
import numpy as np
from matplotlib import pyplot as plt
import glob
import parameters


def filter(image):

	for i in range(parameters.dil_ero_range):
		working_image = image
		image = morphology.dilation (working_image)
		working_image = image
		image = morphology.erosion (working_image)  # Erosion shrinks bright regions and enlarges dark regions

	p_low, p_heigh = np.percentile (image, (0, 50))
	image = exposure.rescale_intensity (image, in_range=(p_low, p_heigh))

	image = roberts (image)
	#image = sobel (image)
	# image = feature.canny(image, parameters.sigma)

	p_low, p_heigh = np.percentile (image, (98, 100))
	image = exposure.rescale_intensity(image, in_range=(p_low, p_heigh))
	#image = exposure.equalize_hist (image)
	image = exposure.equalize_adapthist(image, clip_limit=0.7)
	for i in range(3):
		working_image = image
		image = morphology.dilation (working_image)
		working_image = image
		image = morphology.erosion (working_image)  # Erosion shrinks bright regions and enlarges

	return image


def contour_filter(image):
	for i in range(parameters.dil_ero_range):
		working_image = image
		image = morphology.dilation (working_image)
		working_image = image
		image = morphology.erosion (working_image)  # Erosion shrinks bright regions and enlarges dark regions

	p_low, p_heigh = np.percentile (image, (0, 50))
	image = exposure.rescale_intensity (image, in_range=(p_low, p_heigh))

	#image = exposure.equalize_adapthist(image, clip_limit=0.7)

	# # Contours
	# contours = measure.find_contours(image, 0.3)
	# figure = plt
	# fig, ax = figure.subplots ()
	# #ax.imshow (image, interpolation='nearest', cmap=plt.cm.gray)
	# for n, contour in enumerate (contours):
	# 	ax.plot (contour[:, 1], contour[:, 0], linewidth=2)
	# ax.set_xticks ([])
	# ax.set_yticks ([])
	# figure.savefig(image)
	return image

def separate_figure (file_name):
	filename = os.path.join (os.getcwd (), file_name)
	original_image = io.imread (filename)
	image = io.imread (filename, as_grey=True)
	image_1 = filter(image)
	image_2 = contour_filter(image)
	image = image_2

	# SAVING OUTPUT:
	output_path = os.path.join(os.getcwd(), "output/")
	if not os.path.exists(output_path):
		os.mkdir(output_path)
	new_path = os.path.join(output_path, os.path.basename(file_name) + parameters.name)
	io.imsave(new_path, image)


def read_files ():
	files_list = glob.glob ("planes/*.jpg")
	for file in files_list:
		separate_figure(file)
	#separate_figure("planes/samolot04.jpg")



if __name__ == '__main__':
	read_files ()
