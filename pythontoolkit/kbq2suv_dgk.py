#!/usr/bin/env python
from rhscripts.conversion import mnc_to_numpy
from rhscripts import dcm
from datetime import datetime
import numpy as np
import os
import pyminc.volumes.factory as pyminc


def kbq2suv(petfile_dicom, petfile_mnc, clobber = False):
    
    '''
    input: PET DICOM file in KBQ
    output: PET MNC file in SUV
    '''
    petfile_suv_mnc_name = os.path.join(os.path.dirname(petfile_mnc),'PTsuv.mnc')
    #check if pet suv-file already exists
    if ((os.path.isfile(petfile_suv_mnc_name)) & (clobber == False)):
        print(petfile_suv_mnc_name+' file already exists and clobber = False')
    else: 
        #get time of injection 
        inj_time = datetime.strptime(dcm.get_inj_time(petfile_dicom, out_format = 'str'),'%H%M%S.%f')
        
        #get injection dose
        inj_dose = dcm.get_dose(petfile_dicom)

        #get radiopharmaceutical half life
        half_life = dcm.get_half_life(petfile_dicom)
        
        #get patient weight in grams
        pt_weight = dcm.get_weight(petfile_dicom) * 1000
        
        #get image acquisition time
        acq_time = datetime.strptime(dcm.get_scan_time(petfile_dicom, out_format = 'str'),'%H%M%S.%f')

        #calculate time from injection of scan
        inj_to_acq_time_s = acq_time-inj_time
        inj_to_acq_time_s = np.round(inj_to_acq_time_s.total_seconds())
        inj_to_acq_time_h = inj_to_acq_time_s/3600
        
        #print suv calc data
        #print('injection time = ' + inj_time)
        print('injection dose = ' + str(inj_dose))
        print('patient weight = ' + str(pt_weight) + 'g')
        print('injection to acq time h = ' + str(inj_to_acq_time_h))
        print('half life = ' + str(half_life))

        #caclulate patient dose at acquisition time
        scan_dose = inj_dose*np.exp(np.log(2)/half_life*(-inj_to_acq_time_s))

        #open mnc file and load into numpy
        pet_vol = mnc_to_numpy(petfile_mnc, datatype = 'float32', swapaxes = False)
        pet_vol = pet_vol / (scan_dose /  pt_weight)
        print('pet volume shape: ' + str(pet_vol.shape))                                    
        print('pet vol minimum: ' + str(np.amin(pet_vol)))
        print('pet vol maximum: ' + str(np.amax(pet_vol)))


        print('pet_vol.shape = ' + str(pet_vol.shape))
        print('petfile output name = ' + petfile_suv_mnc_name)

        #print data to volume
        out_vol         = pyminc.volumeLikeFile(petfile_mnc, petfile_suv_mnc_name)
        print('pet_vol.data shape = ' + str(out_vol.data.shape))
        out_vol.data    = pet_vol 
        out_vol.writeFile()





