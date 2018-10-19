'''
Refer to:
http://gdcm.sourceforge.net/html/gdcmconv.html

'''

import os

def use_gdcm_decompress(input, output):
    os.system("gdcmconv --raw " + input + ' ' + output)

def use_gdcm_compress(input,output, compression):
    if compression == 'losslessjpeg':
        os.system("gdcmconv --jpeg " + input + ' ' + output)
    elif compression == 'lossyjpeg':
        os.system("gdcmconv --lossy --jpeg -q 90 " + input + ' ' + output)
    elif compression == 'losslessjpegls':
        os.system("gdcmconv --jpegls " + input + ' ' + output)
    elif compression == 'losslyjpegls':
        os.system("gdcmconv --lossy --jpegls -e 2 " + input + ' ' + output)
    elif compression == 'lossyj2k':
        os.system("gdcmconv --lossy -q 55,50,45 --j2k " + input + ' ' + output)
    elif compression == 'losslessj2k':
        os.system("gdcmconv --j2k " + input + ' ' + output)
