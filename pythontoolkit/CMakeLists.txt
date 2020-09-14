
cmake_minimum_required(VERSION 2.8)


INSTALL(PROGRAMS

  __init__.py
  version.py  
  conversion.py
  utils.py
  dcm.py
  kbq2suv_dgk.py
  quick_plot.py
  get_meta_dat.py
  minc_stats.py

  DESTINATION rhscripts )

# Legacy from when script had a conflicting name
if(EXISTS "${CMAKE_INSTALL_PREFIX}/rhscripts/dicom.py")
	message("Removing legacy file: rhscripts/dicom.py")
	file(REMOVE "${CMAKE_INSTALL_PREFIX}/rhscripts/dicom.py")
endif()