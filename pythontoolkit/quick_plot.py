import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
'''
Quickly plot numpy ND-array content
'''

def jaj_plot(im, mapc = 0, lim = 0, alph = 0.3, axis = 1, grid = 1, colorbar = 0, colorbar_lab = ' '):
	if lim == 0:
		lim 	= im.min(), im.max()
		#print('plot limits = ' + str(lim))
	elif lim == "soft":
		lim 	= -135, 215
		#print('plot limits 2 = ' + str(lim))
	if mapc == 0:
		mapc 	= "gray"
		#print('colormap applied = ' + str(mapc))
	fov = 500.
	v = (0, round(((fov/512)*im.shape[1])), 0, round(((fov/512)*im.shape[0]))) #rescaling the axis
	ax = plt.imshow(im, cmap = mapc, clim = lim, alpha = alph, extent = v)
	if colorbar == 1:
		cbar = plt.colorbar(ax)
		cbar.set_label(colorbar_lab)#, rotation = 90)
	#set axes
	plt.grid(color='gray', alpha = 0.5 , linestyle='-', linewidth=1.5)
	if axis == 0:
		plt.axis('off')
	if grid == 0:
		plt.grid('off')
	return ax