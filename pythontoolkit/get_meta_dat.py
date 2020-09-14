from rhscripts import dcm
import pandas as pd
from os.path import dirname, join, isdir, basename, isfile
from CAAI.preprocess_dicom_dgk import get_rtstruct_ct_pet_filepath
import numpy as np
from datetime import datetime
import glob
from rhscripts import minc_stats


def get_dicom_header_dat_population(folder_name):
	df = get_dicom_header_dat()
	for path in glob.glob(folder_name+'/*'):
		if isdir(path):
			rtx_file, ct_file, pt_file = get_rtstruct_ct_pet_filepath(join(path,'dicom'))
			df_tmp = get_dicom_header_dat(pt_file, ct_file, rtx_file)
			df = df.append(df_tmp, ignore_index = True)
	save_filename = join(folder_name, 'dicom_header_dat_population.csv') 
	df.to_csv(save_filename, index = False)
	print(df)

def get_minc_image_dat_population(folder_name):
	df = get_minc_image_dat()
	for path in glob.glob(folder_name+'/*'):
		pt_minc_file = join(path, 'minc/PTsuv_rsl.mnc')
		ct_minc_file = join(path, 'minc/CT256.mnc')
		rtx_minc_file = join(path, 'minc/RS_Region_1_rsl.mnc')

		pt_exists = 0
		ct_exits = 0
		rtx_exists = 0

		pt_exists = 1 if isfile(pt_minc_file) else print(pt_minc_file + ' did not exist.')
		ct_exits = 1 if isfile(ct_minc_file) else print(ct_minc_file + ' did not exist.')
		rtx_exists = 1 if isfile(rtx_minc_file) else print(rtx_minc_file + ' did not exist.')

		if ((pt_exists == 1)&(ct_exits == 1)&(rtx_exists == 1)):
			print('All necessary files existed at ' + basename(path) + '. Now processesing.')
			df_tmp = get_minc_image_dat(pt_minc_file, ct_minc_file, rtx_minc_file)
			df = df.append(df_tmp, ignore_index = True)

		print('---------------------------------------')
		#break
	save_filename = join(folder_name, 'minc_image_dat_population.csv')
	df.to_csv(save_filename, index = False)
	print(df)

def calc_suv_constant(pt_acq_time, pt_inj_time, pt_dose_inj, half_life, pt_weight):
    inj_to_acq_time_s = pt_acq_time-pt_inj_time
    inj_to_acq_time_s = np.round(inj_to_acq_time_s.total_seconds())
    pt_dose_scan_time = pt_dose_inj*np.exp(np.log(2)/half_life*(-inj_to_acq_time_s))
    suv_constant = 1./(pt_dose_scan_time/pt_weight)
    return inj_to_acq_time_s, pt_dose_scan_time, suv_constant

def get_dicom_header_dat(pt_file = None, ct_file = None, rtx_file = None):
	if pt_file == None:
		df = pd.DataFrame(
			columns = [
			'pt_folder_name',
			'pt_file_descrip', 
			'ct_file_descrip', 
			'rtx_file_descrip', 
			'pt_age', 
			'study_date',
			'pt_weight',
			'pt_dose_inj',
			'pt_inj_time',
			'ct_acq_time',
			'pt_acq_time',
			'half_life',
			'inj_to_acq_time_s',
			'pt_dose_scan_time',
			'suv_constant',
			'ct_series_uid',
			'pt_series_uid',
			'rtx_series_ref_uid'
			])
	else:
		pt_folder_name = basename(dirname(dirname(pt_file)))
		pt_file_descrip = dcm.get_description(pt_file)
		ct_file_descrip = dcm.get_description(ct_file)
		rtx_file_descrip = dcm.get_description(rtx_file)
		study_date = dcm.get_studydate(ct_file)
		pt_weight = dcm.get_weight(pt_file)
		pt_age = dcm.get_age(ct_file)
		pt_dose_inj = dcm.get_dose(pt_file)
		pt_inj_time = dcm.get_inj_time(pt_file)
		ct_acq_time = dcm.get_scan_time(ct_file)
		pt_acq_time = dcm.get_scan_time(pt_file)
		half_life = dcm.get_half_life(pt_file)
		ct_series_uid = dcm.get_series_instance_uid(ct_file)
		pt_series_uid = dcm.get_series_instance_uid(pt_file)
		rtx_series_ref_uid = dcm.get_rtx_referenced_series_instance_uid(rtx_file)
		inj_to_acq_time_s, pt_dose_scan_time, suv_constant = calc_suv_constant(pt_acq_time, pt_inj_time, pt_dose_inj, half_life, pt_weight)#, pt_dose_scan_time, suv_constant 

		list_of_vars = [[
			pt_folder_name,		
			pt_file_descrip, 
			ct_file_descrip, 
			rtx_file_descrip, 
			pt_age, 
			study_date,
			pt_weight,
			pt_dose_inj,
			pt_inj_time,
			ct_acq_time,
			pt_acq_time,
			half_life,
			inj_to_acq_time_s,
			pt_dose_scan_time,
			suv_constant,
			ct_series_uid,
			pt_series_uid,
			rtx_series_ref_uid
			]]

		df = pd.DataFrame(list_of_vars, 
			columns = [
			'pt_folder_name',
			'pt_file_descrip', 
			'ct_file_descrip', 
			'rtx_file_descrip', 
			'pt_age', 
			'study_date',
			'pt_weight',
			'pt_dose_inj',
			'pt_inj_time',
			'ct_acq_time',
			'pt_acq_time',
			'half_life',
			'inj_to_acq_time_s',
			'pt_dose_scan_time',
			'suv_constant',
			'ct_series_uid',
			'pt_series_uid',
			'rtx_series_ref_uid'
			])
	return df
	#save_file =join(dirname(dirname(pt_file)), 'meta_dat.csv') 
	#df.to_csv(save_file, index = False)
	#a = pd.read_csv(save_file)
	#print(a)

def get_minc_image_dat(pt_file = None, ct_file = None, rtx_file = None):

	if pt_file == None:
		df = pd.DataFrame(
			columns = [
			'pt_folder_name',
			'suv_max_image',
			'suv_min_image',
			'suv_mean_image',
			'suv_median_image',
			'hu_max_image',
			'hu_min_image',
			'hu_mean_image',
			'hu_median_image',
			'suv_max_tumour',
			'suv_min_tumour',
			'suv_mean_tumour',
			'suv_median_tumour',
			'hu_max_tumour',
			'hu_min_tumour',
			'hu_mean_tumour',
			'hu_median_tumour',
			't_size',
			'n_blobs'
			])
	else:
		pt_folder_name = basename(dirname(dirname(pt_file)))

		hu_max_image, hu_min_image, hu_mean_image, hu_median_image = minc_stats.get_stats_image(ct_file)
		suv_max_image, suv_min_image, suv_mean_image, suv_median_image = minc_stats.get_stats_image(pt_file)
		suv_max_tumour, suv_min_tumour, suv_mean_tumour, suv_median_tumour = minc_stats.get_stats_in_vol(pt_file, rtx_file)
		hu_max_tumour, hu_min_tumour, hu_mean_tumour, hu_median_tumour = minc_stats.get_stats_in_vol(ct_file, rtx_file)
		
		t_size = minc_stats.get_volume(rtx_file)
		n_blobs = minc_stats.get_n_subvolumes(rtx_file)
		

		print(pt_folder_name)
		list_of_vars = [[
			pt_folder_name,
			suv_max_image,
			suv_min_image,
			suv_mean_image,
			suv_median_image,
			hu_max_image,
			hu_min_image,
			hu_mean_image,
			hu_median_image,
			suv_max_tumour,
			suv_min_tumour,
			suv_mean_tumour,
			suv_median_tumour,
			hu_max_tumour,
			hu_min_tumour,
			hu_mean_tumour,
			hu_median_tumour,
			t_size,
			n_blobs
			]]

		df = pd.DataFrame(list_of_vars, 
			columns = [
			'pt_folder_name',
			'suv_max_image',
			'suv_min_image',
			'suv_mean_image',
			'suv_median_image',
			'hu_max_image',
			'hu_min_image',
			'hu_mean_image',
			'hu_median_image',
			'suv_max_tumour',
			'suv_min_tumour',
			'suv_mean_tumour',
			'suv_median_tumour',
			'hu_max_tumour',
			'hu_min_tumour',
			'hu_mean_tumour',
			'hu_median_tumour',
			't_size',
			'n_blobs'
			])
	return df

if __name__ == '__main__':
	folder_name = '/homes/kovacs/project_data/hnc-auto-contouring/pt_data_19_256_2'
	pt_minc_file = join(folder_name, 'minc/PTsuv_rsl.mnc')
	ct_minc_file = join(folder_name, 'minc/CT256.mnc')
	rtx_minc_file = join(folder_name, 'minc/RS_Region_1_rsl.mnc')
	get_minc_image_dat_population(folder_name)
	#print()

	#get_minc_image_dat_population(folder_name)
