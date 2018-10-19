import numpy as np
import pickle
import glob
from . import image_process
import os
import contextlib

def delete_file(filename):

    with contextlib.suppress(FileNotFoundError): os.remove(filename)


def process_and_save(files, label, userVars, dictionary):

    data = []
    for file in files:
        print('Processing file {}'.format(file))
        x, percent_modified = image_process.process_DICOM(file, userVars)
        data.append(x)

    dictionary[str(label)] = data

    return dictionary

def to_pickle(settings):

    #settings = set_vars()
    messages = []
    settings['dir'] = '/data'
    output_file = settings.get('dir') + '/' + settings.get('pickle_file')
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

    output= {'num_classes':len(folders)}


    for i in range(len(folders)):
        folder = folders[i]
        print('Currently processing folder {}'.format(folder))
        files = glob.glob(settings.get('dir') + '/' + folder + '/*.dcm')
        output = process_and_save(files,i,settings,output)

    with open(output_file, 'wb') as f:
        pickle.dump(output,f, protocol=4)

    print('Data have been saved to {}'.format(settings.get('pickle_file')))
    messages.append('Data have been saved to {}'.format(settings.get('pickle_file')))
    return messages

#main()