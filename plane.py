from skimage import io
from skimage import measure
from skimage import morphology
from skimage import feature
from skimage import exposure
from skimage import filters
from skimage.draw import polygon
import os
import numpy as np
from matplotlib import pyplot as plt
import glob


# change name of files for testing (add name at the end of file)
name = ''


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


def filter(image):
	# GAUSSIAN
	image = filters.gaussian (image, sigma=0.4)
	# EROSION
	working_image = image
	image = morphology.erosion (working_image)  # Erosion shrinks bright regions and enlarges dark regions
	# DETECT EDGES (CANNY)
	image = feature.canny (image, sigma=4)
	# Adaptive Equalization
	image = exposure.equalize_adapthist (image, clip_limit=0.1)  # after canny
	return image

	# unused configuration
	# # GAUSSIAN
	# image = filters.gaussian (image, sigma=3)
	# # DETECT EDGES (CANNY)
	# image = feature.canny (image, sigma=2)
	# # DILATION
	# working_image = image
	# image = morphology.dilation (working_image)
	# # Adaptive Equalization
	# image = exposure.equalize_adapthist (image, clip_limit=0.1)  # after canny
	# return image

def contour_filter(image, original_image):
	# GAUSSIAN
	image = filters.gaussian (image, sigma=0.5)

	# EROSION
	working_image = image
	image = morphology.erosion (working_image)  # Erosion shrinks bright regions and enlarges dark regions

	# Contrast stretching (smaller range on black)
	# smaller range - they lose in clouds
	p_low, p_heigh = np.percentile (image, (0, 30))  # 0, 40
	image = exposure.rescale_intensity (image, in_range=(p_low, p_heigh))

	# EROSION x2
	for i in range(1):
		working_image = image
		image = morphology.erosion (working_image)  # Erosion shrinks bright regions and enlarges dark regions

	# CONTOURS
	my_contours = []
	centroids = []
	# if higher than there is more reaction on brighter pixels (but rows tuck in plane)
	for contour in measure.find_contours(image, 0.5, fully_connected='high'):
		if len(contour) > 400 and (is_close(contour[0], contour[-1])) is True:
			my_contours.append(contour)
			# CENTROID:
			rr, cc = polygon([x[0] for x in contour[:]], [y[1] for y in contour[:]])
			zeros_image = np.zeros((len(image), len(image[0])))
			zeros_image[rr, cc] = 1
			m = measure.moments(zeros_image)
			cr = m[0, 1] / m[0, 0]
			cc = m[1, 0] / m[0, 0]
			point = [cc, cr]
			centroids.append(point)

	# PLOT
	figure = plt
	fig, ax = figure.subplots()
	ax.imshow (original_image, interpolation='nearest', cmap=plt.cm.gray)
	for n, contour in enumerate (my_contours):
		ax.plot (contour[:, 1], contour[:, 0], linewidth=2)
		ax.plot (centroids[n][0], centroids[n][1], 'wo', linewidth=2)
	ax.axis ('off')
	return figure


def file_processing (file_name):
	filename = os.path.join (os.getcwd (), file_name)
	original_image = io.imread (filename)
	image = io.imread (filename, as_grey=True)
	working_image = image	# this one will be unchanged

	# 1) excercise for 3
	image = filter(working_image)
	# SAVING OUTPUT:
	output_path = os.path.join(os.getcwd(), "output_3/")
	if not os.path.exists(output_path):
		os.mkdir(output_path)
	new_path = os.path.join(output_path, os.path.basename(file_name) + name)
	io.imsave(new_path, image)
	good_pictures = ['samolot01.jpg', 'samolot07.jpg', 'samolot08.jpg', 'samolot09.jpg',
					 'samolot12.jpg', 'samolot17.jpg']
	create_mosaic(good_pictures)

	# 2) exercise for 5
	image = contour_filter(working_image, original_image)
	# SAVING OUTPUT:
	output_path = os.path.join(os.getcwd(), "output_5/")
	if not os.path.exists(output_path):
		os.mkdir(output_path)
	new_path = os.path.join(output_path, os.path.basename(file_name) + name)
	image.savefig(new_path, bbox_inches='tight')


def create_mosaic(chosen_pictures):
	f, ((ax_1, ax_2), (ax_3, ax_4), (ax_5, ax_6)) = plt.subplots(3,2, dpi=350)
	list = [ax_1, ax_2, ax_3, ax_4, ax_5, ax_6]
	for n, name in enumerate(chosen_pictures):
		filename = os.path.join (os.getcwd (), 'output_3/', name)
		original_image = io.imread (filename)
		list[n].imshow (original_image, interpolation='nearest', cmap=plt.cm.gray)
		list[n].axis('off')
	f.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
	f.savefig('output_3/collage.jpg')


def read_files ():
	files_list = glob.glob ("planes/*.jpg")
	for file in files_list:
		file_processing(file)


if __name__ == '__main__':
	read_files ()
