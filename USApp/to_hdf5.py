import numpy as np
import h5py
import glob
from . import image_process
import os
import contextlib

def delete_file(filename):

    with contextlib.suppress(FileNotFoundError): os.remove(filename)

def process_and_save_3(files, label, userVars):

    frames = []
    output_file = userVars.get('dir') +'/'+userVars.get('h5_file')
    if userVars.get('compression') == '1': compression = 'gzip'
    elif userVars.get('compression') == '2': compression = 'lzf'

    f = h5py.File(output_file, 'a')

    file = files.pop(0) # Use first file
    print('Processing file {}'.format(file))
    x = image_process.process_DICOM(file, userVars)
    fr, r, c = x.shape[0:3]

    if userVars.get('rgb'):

        dset = f.create_dataset(str(label), data=x, chunks=(1, r, c, 3), maxshape=(None, r, c, 3), compression=compression)
        frames.append(fr)

        for file in files:
            print('Processing file {}'.format(file))
            x = image_process.process_DICOM(file, userVars)
            fr, r, c = x.shape[0:3]
            frames.append(fr)
            f_current = dset.shape[0]
            dset.resize((fr + f_current, r, c, 3))
            dset[f_current:, :, :] = x

    else:

        dset = f.create_dataset(str(label), data=x, chunks=(1, r, c), maxshape=(None, r, c),
                                compression=compression)
        frames.append(fr)
        for file in files:
            print('Processing file {}'.format(file))
            x = image_process.process_DICOM(file, userVars)
            frames.append(fr)
            f_current = dset.shape[0]
            dset.resize((fr + f_current, r, c))
            dset[f_current:, :, :] = x


    dset = f.create_dataset(str(label)+'_frames', data=frames, compression=compression)

def process_and_save(files, label, userVars):

    frames = []
    output_file = userVars.get('dir') +'/'+userVars.get('h5_file')
    if userVars.get('compression') == '1': compression = 'gzip'
    elif userVars.get('compression') == '2': compression = 'lzf'

    f = h5py.File(output_file, 'a')

    file = files.pop(0) # Use first file
    print('Processing file {}'.format(file))
    x,percent_modified = image_process.process_DICOM(file, userVars)
    fr, r, c = x.shape

    dset = f.create_dataset(str(label), data=x, chunks=(1, r, c), maxshape=(None, r, c),
                            compression=compression)
    frames.append(fr)
    for file in files:
        print('Processing file {}'.format(file))
        x,percent_modified = image_process.process_DICOM(file, userVars)
        f_current = dset.shape[0]
        fr = x.shape[0]
        frames.append(fr)
        dset.resize((fr + f_current, r, c))
        dset[f_current:, :, :] = x


    dset = f.create_dataset(str(label)+'_frames', data=frames, compression=compression)

def to_hdf5(settings):

    settings['dir'] = '/data'
    settings['resize'] = True
    messages = []

    output_file = settings.get('dir') + '/' + settings.get('h5_file')
    delete_file(output_file)

    if settings.get('verbose'):
        for set in settings: print(set+' : ' + str(settings.get(set)))

    folders = next(os.walk(settings.get('dir')))[1]
    if 'Processed' in folders: folders.remove('Processed')
    if 'Videos' in folders: folders.remove('Videos')

    print('Found {} classes'.format(len(folders)))
    messages.append('Found {} classes'.format(len(folders)))

    for i in range(len(folders)):
        print('Class {} assigned label {}'.format(folders[i],i))
        messages.append('Class {} assigned label {}'.format(folders[i],i))

    total_frames = []
    total_labels = []
    for i in range(len(folders)):
        folder = folders[i]
        print('Currently processing folder {}'.format(folder))
        files = glob.glob(settings.get('dir') + '/' + folder + '/*.dcm')
        process_and_save(files,i,settings)

    print('Data have been saved to {}'.format(settings.get('h5_file')))
    messages.append('Data have been saved to {}'.format(settings.get('h5_file')))
    return messages
