'''
Scans subdirectories of variable data_directory, looks for .dcm files.
Reports number of files found in each directory.

'''

import os
import glob
import subprocess

def check_dirs(data_directory):
    messages = []
    if not os.path.exists(data_directory):
        messages.append('No data directory mounted.')
        return messages
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
    '''
    if len(all_files) > 0:
        file = all_files.pop()
        messages.append('Checking compression status of {}'.format(file))
        output = subprocess.check_output("gdcminfo " + file + " | grep Transf", shell=True).decode("utf-8")
        messages.append(output)
        messages.append('If the above line says "compression" in it, your data are likely compressed.')
    #ds = dicom.read_file(file)
    #print(ds)
    '''
    return messages

#def main():
#    data_directory = '/data'
    #data_directory = '/Users/adh5/Desktop/Downloaded_DICOM/Nick_data/DICOM_files_Focused_Chest_Effusion_Data_Set'
#    messages = check_dirs(data_directory)
#    for message in messages:
#        print(message)

#main()