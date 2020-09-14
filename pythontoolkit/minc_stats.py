import numpy as np
from rhscripts.conversion import mnc_to_numpy
import subprocess
from scipy import ndimage

def get_image_max(file_path):
	im = mnc_to_numpy(file_path)
	val = np.amax(im)
	return val

def get_image_min(file_path):
	im = mnc_to_numpy(file_path)
	val = np.amin(im)
	return val

def get_stats_in_vol(file_path, vol_path):
	im = mnc_to_numpy(file_path)
	vol = mnc_to_numpy(vol_path).astype('int')
	values = im[vol == 1]
	vol_max = np.amax(values)
	vol_min = np.amin(values)
	vol_mean = np.mean(values)
	vol_median = np.median(values)
	return vol_max, vol_min, vol_mean, vol_median


def get_volume(vol_path):
	x,y = get_image_pixel_spacing(vol_path)
	vol = mnc_to_numpy(vol_path).astype('int')
	volume_mm = len(vol[vol == 1]) * x * y
	return volume_mm

def get_image_pixel_spacing(vol_path):
	xspace_step = subprocess.Popen('mincinfo ' + vol_path + ' -attvalue xspace:step', shell=True, stdout=subprocess.PIPE).stdout.read().decode("utf-8").rstrip()
	yspace_step = subprocess.Popen('mincinfo ' + vol_path + ' -attvalue yspace:step', shell=True, stdout=subprocess.PIPE).stdout.read().decode("utf-8").rstrip()
	return abs(float(xspace_step)), abs(float(yspace_step))


def get_stats_image(file_path):
	im = mnc_to_numpy(file_path)
	values = im
	vol_max = np.amax(values)
	vol_min = np.amin(values)
	vol_mean = np.mean(values)
	vol_median = np.median(values)
	return vol_max, vol_min, vol_mean, vol_median

def get_n_subvolumes(vol_path):
	#currently nok working as should
	#TODO: create functions that counts number of separate segments in volume
	#
	vol = mnc_to_numpy(vol_path).astype('int')
	s = ndimage.generate_binary_structure(3,3)
	labeled_array, num_features = ndimage.label(vol, structure = s)
	return num_features