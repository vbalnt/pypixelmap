import numpy as np
import random
import operator
import itertools
from matplotlib.patches import ConnectionPatch
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.ticker import LinearLocator
from matplotlib.patches import ConnectionStyle

def render_pixel_map(image,number_of_lines_to_draw,filename_to_save):
	image = image.astype(np.uint8)
	if (len(image.shape)==2):
		is_grayscale = True
		non_annotated_labels_font_size = 11
		annotated_labels_font_size = 11
	elif (len(image.shape)==3 and image.shape[2]==3):
		is_grayscale = False
		non_annotated_labels_font_size = 8
		annotated_labels_font_size = 8
	else:
		raise ValueError("The image argument must be either a 2d (grayscale) of a 3d (rgb) image.")
	w,h =image.shape[0:2]
	fig = plt.figure(1, figsize=(10,8),frameon=False)
	plt.subplots_adjust(wspace=0.05, hspace=0.05)
	plt.rc('font', family='serif')
	plt.rc('font', weight='normal')
	image_axis = plt.subplot(121)
	image_axis.set_title(r'$Image$ $pixels$')

	if is_grayscale:
		image_axis.imshow(image,interpolation='nearest',cmap = cm.Greys_r,aspect = 'equal',vmin = 0, vmax = 255)
	else:
		image_axis.imshow(image,interpolation='nearest',aspect = 'equal')
	image_axis.get_xaxis().set_ticks([])
	image_axis.get_yaxis().set_ticks([])

	pixel_map = 255*np.ones((image.shape[0],image.shape[1]))
	pixel_map_axis = plt.subplot(122)

	pixel_map_axis.imshow(pixel_map,interpolation='nearest',cmap = cm.Greys_r,aspect = 'equal',vmin = 0, vmax = 255)
	pixel_map_axis.xaxis.set_major_locator(LinearLocator(image.shape[0]+1))
	pixel_map_axis.yaxis.set_major_locator(LinearLocator(image.shape[1]+1))
	plt.grid(axis='both')
	pixel_map_axis.get_xaxis().set_ticklabels([])
	pixel_map_axis.get_yaxis().set_ticklabels([])
	pixel_map_axis.set_title(r'$Pixel$ $values$')

	random_selection_rows = random.sample( xrange( image.shape[0] ), number_of_lines_to_draw )
	random_selection_columns = np.array( random.sample( xrange( image.shape[1] ), number_of_lines_to_draw ))
	annotated_pixels = list(itertools.izip(random_selection_rows, random_selection_columns))

	all_pixels = list(itertools.product(range(image.shape[0]),range(image.shape[1])))
	non_annotated_pixels = [x for x in all_pixels if x not in annotated_pixels]

	#plot all except the ones that will have arrows
	for pixel in non_annotated_pixels:
		#no line annotation, just the pixel value
		if is_grayscale:
			pixel_map_axis.annotate(str(image[pixel]), xy=list(reversed(pixel)),ha="center", va="center",size = non_annotated_labels_font_size,alpha = 0.6)
		else:
			r,g,b  = image[pixel]
			pixel_map_axis.annotate(str(r), xy=(np.array(list(reversed(pixel)))-np.array([0.0,0.3])),alpha = 0.5,ha="center", va="center",size = non_annotated_labels_font_size,color='r')
			pixel_map_axis.annotate(str(g), xy=list(reversed(pixel)),alpha = 0.5,ha="center", va="center",size = non_annotated_labels_font_size,color='g')
			pixel_map_axis.annotate(str(b), xy=(np.array(list(reversed(pixel)))+np.array([0.0,0.3])),alpha = 0.5,ha="center", va="center",size = non_annotated_labels_font_size,color='b')

	#draw the arrows and annotate the pixels that have arrows in a different way
	for pixel in annotated_pixels:
		if is_grayscale:
			pixel_map_axis.annotate(str(image[pixel]), xy=tuple(reversed(pixel)),ha="center", va="center",size = annotated_labels_font_size)
		else:
			r,g,b  = image[pixel]
			pixel_map_axis.annotate(str(r), xy=(np.array(list(reversed(pixel)))-np.array([0.0,0.3])),ha="center", va="center",size = annotated_labels_font_size,color='r')
			pixel_map_axis.annotate(str(g), xy=list(reversed(pixel)),ha="center", va="center",size = 9,color='g')
			pixel_map_axis.annotate(str(b), xy=(np.array(list(reversed(pixel)))+np.array([0.0,0.3])),ha="center", va="center",size = annotated_labels_font_size,color='b')
		coords_image = ( 1-(pixel[0]+0.5)/float(w) , (pixel[1]+0.5)/float(h) )
		coords_pixels = ( 1-(pixel[0]+0.5)/float(w) , (pixel[1]+0.25)/float(h) )
		coords_image = tuple(reversed(coords_image))
		coords_pixels = tuple(reversed(coords_pixels))
		#randomize the arc for a better plot
		arc = str("Arc3, rad="+str(random.uniform(-0.08, 0.08))+"")
		con = ConnectionPatch(xyA=coords_image, xyB=coords_pixels, coordsA="axes fraction", coordsB="axes fraction",
		  			  axesA=image_axis, axesB=pixel_map_axis,arrowstyle='->',connectionstyle=ConnectionStyle(arc))
		pixel_map_axis.add_artist(con)
	plt.draw()
	fig.savefig(filename_to_save, bbox_inches='tight',pad_inches = 0.2)
	plt.close()


def main():
    gray = np.random.randint(0,255,(10,10))
    rgb = np.random.randint(0,255,(10,10,3))
    render_pixel_map(gray, number_of_lines_to_draw =5, filename_to_save = 'pixelmap_gray.pdf')
    render_pixel_map(rgb ,number_of_lines_to_draw =5, filename_to_save = 'pixelmap_rgb.pdf')


if __name__ == "__main__":
    main()


