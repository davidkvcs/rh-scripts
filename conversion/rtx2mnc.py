import pyminc.volumes.factory as pyminc
from skimage.draw import polygon2mask
import numpy as np
import pydicom
import os
from glob import glob
import argparse
from rhscripts.conversion import rtx_to_mnc

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