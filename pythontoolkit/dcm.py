#!/usr/bin/env python
import os
try:
    import pydicom as dicom
except ImportError:
    import dicom
import configparser
from rhscripts.conversion import findExtension

def get_description(file):
    """Get the SeriesDescription of a dicom file

    Parameters
    ----------
    file : string
        Path to the dicom file
    """
    return dicom.read_file(file).SeriesDescription

def get_seriesnumber(file):
    """Get the SeriesNumber of a dicom file

    Parameters
    ----------
    file : string
        Path to the dicom file
    """
    return dicom.read_file(file).SeriesNumber

def get_patientid(file):
    """Get the PatientID of a dicom file

    Parameters
    ----------
    file : string
        Path to the dicom file
    """
    return dicom.read_file(file).PatientID

def get_patientname(file):
    """Get the PatientName of a dicom file

    Parameters
    ----------
    file : string
        Path to the dicom file
    """
    return dicom.read_file(file).PatientName

def get_studydate(file):
    """Get the StudyDate of a dicom file

    Parameters
    ----------
    file : string
        Path to the dicom file
    """
    return dicom.read_file(file).StudyDate

def get_kvp(file):
    """Get the KVP of a dicom file

    Parameters
    ----------
    file : string
        Path to the dicom file
    """
    return dicom.read_file(file).KVP

def get_age(file):
    """Get the patient age of a dicom file

    Parameters
    ----------
    file : string
        Path to the dicom file
    """
    return dicom.read_file(file).PatientAge

def get_weight(file):
    """Get the patient weight of a dicom file

    Parameters
    ----------
    file : string
        Path to the dicom file
    """
    return dicom.read_file(file).PatientWeight

def get_gender(file):
    """Get the patient gender of a dicom file

    Parameters
    ----------
    file : string
        Path to the dicom file
    """
    return dicom.read_file(file).PatientSex

def get_dose(file):
    """Get the radionuclide total dose of a dicom file

    Parameters
    ----------
    file : string
        Path to the dicom file
    """
    return dicom.read_file(file).RadiopharmaceuticalInformationSequence[0].RadionuclideTotalDose

def get_inj_time(file):#from pet dicom file - radiopharmaceutical info
    """Get the radiopharmaceutical start time of a dicom file

    Parameters
    ----------
    file : string
        Path to the dicom file
    """
    return dicom.read_file(file).RadiopharmaceuticalInformationSequence[0].RadiopharmaceuticalStartTime

def get_scan_time(file):
    """Get the acquisition time of a dicom file

    Parameters
    ----------
    file : string
        Path to the dicom file
    """
    return dicom.read_file(file).AcquisitionTime

def get_modality(file):
    """Get the study modality of a dicom file

    Parameters
    ----------
    file : string
        Path to the dicom file
    """
    return dicom.read_file(file, force = True).Modality

def get_series_instance_uid(file):
    """Get the study series UID of a dicom file

    Parameters
    ----------
    file : string
        Path to the dicom file
    """
    return dicom.read_file(file).SeriesInstanceUID

def get_rtx_referenced_series_instance_uid(file):
    """Get which series instance UID the RTSTRUCT references

    Parameters
    ----------
    file : string
        Path to the dicom file
    """
    return dicom.read_file(file).ReferencedFrameOfReferenceSequence[0].RTReferencedStudySequence[0].RTReferencedSeriesSequence[0].SeriesInstanceUID


def send_data(folder, server=None, checkForEndings=True):
    """Send a dicom dataset to a dicom node

    Parameters
    ----------
    folder : string
        Path to the dicom files
    server : string, optional
        Name of the server to send to
    checkForEndings : boolean, optional
        Check if folder contains any files with dicom endings
    
    """

    f = findExtension(folder)
    if not checkForEndings or isinstance(f,str):
        
        # Setup
        caai_dir = os.environ['CAAI']
        config_path = '%s/share/config.ini' % caai_dir
        if not os.path.exists(config_path):
            print('You do not have a config.ini file in %s' % caai_dir)
            return
        config = configparser.ConfigParser()
        config.sections()
        config.read(config_path)
        
        if not server:
            print('You need to select a server from config.ini')
            return
        
        server = server.lower()
        
        if not server in config:
            print('config.ini does not contain %s' % server)
            return
        
        
        cmd = 'storescu --scan-directories -aet %s -aec %s %s %s %s' % (
                config['DEFAULT']['AET'], 
                config[server]['AEC'], 
                config[server]['addr'], 
                config[server]['port'], 
                folder)
        
        os.system(cmd)