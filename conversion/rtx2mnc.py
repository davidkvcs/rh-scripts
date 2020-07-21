import pyminc.volumes.factory as pyminc
from skimage.draw import polygon2mask
import numpy as np
import pydicom
import os
from glob import glob
import argparse

def rtx_to_mnc(dcm_file,mnc_file,outdir):

    mnc = pyminc.volumeFromFile(mnc_file)
    d = pydicom.read_file(dcm_file)
    for roival, rs in enumerate(d.ROIContourSequence):
        print( outdir + '/RS_' +d.StructureSetROISequence[roival][0x3006, 0x0026].value.replace(" ", "_")+'.mnc')
        if not hasattr(rs, 'ContourSequence'):
            print("Skipping...")
            continue
        print( )
        out = pyminc.volumeLikeFile(mnc_file, outdir + '/RS_' +d.StructureSetROISequence[roival][0x3006, 0x0026].value.replace(" ", "_")+'.mnc')
        out.data[:] = 0.0
        for cs in rs.ContourSequence:

            data = cs.ContourData
    
            # Fill
            voxel_coordinates_inplane = np.zeros((cs.NumberOfContourPoints,2))
    
            k = -1
            for i in range(cs.NumberOfContourPoints):
                j=i*3
                xyz_world = [-data[j],-data[j+1],data[j+2]]
                xyz_voxel = mnc.convertWorldToVoxel(xyz_world)
                k = int(round(xyz_voxel[0]))
    
                # Fill
                voxel_coordinates_inplane[i,:] = [xyz_voxel[1],xyz_voxel[2]] # this order for polygon2mask - reverse for opencv
            current_slice_inner = np.zeros((mnc.getSizes()[1],mnc.getSizes()[2]),dtype=np.uint8)
            
            #assert data[:3] == data[-3:],"{} vs {}".format(data[:3],data[-3:])
    
            current_slice_inner = polygon2mask((mnc.getSizes()[1],mnc.getSizes()[2]),voxel_coordinates_inplane)
            
            out.data[k] += current_slice_inner
        out.data = np.where(out.data % 2 == 0, 0, 1)
        out.writeFile()
        out.closeVolume()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='RTX2MNC.')
    parser.add_argument('RTX', help='Path to the DICOM RTX file', nargs='?')
    parser.add_argument('MINC', help='Path to the MINC container file', nargs='?')
    parser.add_argument('RTMINC', help='Output directory', nargs='?')

    args = parser.parse_args()

    if not args.RTX or not args.MINC or not args.RTMINC:
        parser.print_help()
        print('Too few arguments')
        exit(-1)

    rtx_to_mnc(args.RTX, args.MINC, args.RTMINC)