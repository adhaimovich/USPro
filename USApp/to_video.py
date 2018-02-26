import glob
import os
from . import image_process
import shutil
import skimage
import skvideo.io
import numpy as np
from scipy import stats


def to_video(settings):
    messages = []

    settings['dir'] = '/data'

    if settings.get('verbose'):
        for set in settings: print(set + ' : ' + str(settings.get(set)))

    # Establish directory names
    folders = next(os.walk(settings.get('dir')+'/'))[1]


    if 'Videos' in folders: folders.remove('Videos')
    if 'Processed' in folders: folders.remove('Processed')
    if not os.path.exists(settings.get('dir') + '/Videos'):
        os.makedirs(settings.get('dir') + '/Videos')
    else:
        shutil.rmtree(settings.get('dir') + '/Videos')
        os.makedirs(settings.get('dir') + '/Videos')

    target_directories = []
    for folder in folders:

        if settings.get('verbose'): print("Creating output folder " + str(folder))
        messages.append("Creating output folder " + str(folder))
        target_directory = settings.get('dir')+'/Videos/'+ folder
        if not os.path.exists(target_directory):
            os.makedirs(target_directory)
        target_directories.append(target_directory)

    # Get input and output filenames
    percent_mod = []
    for i in range(len(folders)):
        in_folder = folders[i]
        out_folder = target_directories[i]
        files = glob.glob(settings.get('dir') + '/' + in_folder + '/*.dcm')

        for file in files:
            if settings.get('verbose'): print(file)
            messages.append('File: {}'.format(file))
            base = os.path.basename(file)
            print(base)
            if settings.get('output_type') == '1':
                outfile = out_folder + '/' + os.path.splitext(base)[0] + '.avi'
            elif settings.get('output_type') == '2':
                outfile = out_folder + '/' + os.path.splitext(base)[0] + '.mpeg'
            mat, percent_mod_single = image_process.process_DICOM(file, settings)
            percent_mod.append(percent_mod_single)
            
            writer = skvideo.io.FFmpegWriter(outfile)
            for i in range(mat.shape[0]):
                out_mat = np.stack([mat,mat,mat],axis=-1)
                writer.writeFrame(out_mat[i, :, :,:])
            writer.close()
    print('Mean')
    print(np.mean(percent_mod))
    print('Std')
    print(np.std(percent_mod))
    return messages

