'''
Scans subdirectories of variable data_directory, looks for .dcm files.
Reports number of files found in each directory.

'''

import os
import glob
import subprocess

def check_dirs(data_directory):
    messages = []
    folders = next(os.walk(data_directory))[1]

    if 'Videos' in folders: folders.remove('Videos')
    if 'Processed' in folders: folders.remove('Processed')

    num_classes = len(folders)
    if num_classes == 0:
        messages.append('No directories found.')
        messages.append('If directory has data, it likely was mounted incorrectly. Please refer to readme.')
        return messages
    else: messages.append('Number of classes identified is: ' + str(num_classes))

    all_files = []

    for folder in folders:
        files = glob.glob(data_directory+'/'+folder+'/*.dcm')
        messages.append('Class ' + folder + ' contains ' + str(len(files)) + ' files.')
        all_files = all_files+files
    print(messages)

    return messages
