import numpy as np
from skimage.filters import threshold_otsu
from skimage.measure import label, regionprops
from skimage.morphology import closing, square
import scipy
import os
import SimpleITK

def DICOMtoImages(inpt):

    img = SimpleITK.ReadImage(inpt)

    if 'YBR' in img.GetMetaData('0028|0004'):
        mat = SimpleITK.GetArrayFromImage(img)[:, :, :, 0]
    elif img.GetMetaData('0028|0004') == 'RGB':
        mat = np.dot(SimpleITK.GetArrayFromImage(img)[:, :, :, :], [0.2989, 0.5870, 0.1140])
    return mat

def Anonymize_Mat(mat, userVars):
    threshold = userVars.get('cleaning_threshold')
    increment = userVars.get('image_increment')
    f = mat.shape[0]
    r = mat.shape[1]
    c = mat.shape[2]
    std_dev_mat = np.zeros([r, c])

    # Calculate std dev over increments
    for i in range(0, f - increment, increment):
        std_dev_mat = std_dev_mat + np.std(mat[i:increment + i, :, :], 0)

    # Use the std dev < threshold to delete pixels as needed
    modified_pixels = 0
    for rows in range(r):
        for cols in range(c):
            if std_dev_mat[rows, cols] < threshold:
                modified_pixels += 1
                mat[:, rows, cols] = 0
    print('Pixels modified ' + str(modified_pixels))
    print('Percent pixels modified ' + str(modified_pixels * 100 / (r * c)))
    return mat, std_dev_mat

def crop_to_boundaries_thresh(mat, userVars, ori_mat):

    grayscale = mat[0, :, :]
    # apply threshold
    threshold_method = userVars.get('image_thresholding')

    if threshold_method == '1': threshold = 0 #userVars.get('cleaning_threshold')
    elif threshold_method == '2': threshold = threshold_otsu(grayscale)

    bw = closing(grayscale > threshold, square(3))

    # label image regions
    label_image = label(bw)

    # regions
    regions = regionprops(label_image)
    areas = []
    for reg in regions:
        areas.append(reg.area)
    max_index = areas.index(max(areas))
    minr, minc, maxr, maxc = regions[max_index].bbox
    coords = regions[max_index].coords

    if userVars.get('rebuild'):
        print('Rebuilding')
        mat = Rebuild_Mat(mat, ori_mat, coords)
    if userVars.get('crop'):
        mat = mat[:,minr:maxr, minc:maxc]
        ori = ori_mat[:,minr:maxr, minc:maxc]
    else: ori = ori_mat

    return mat, coords, ori

# Downsample to desired h/w dimensions
def Resize_Mat(mat,userVars):
    r_out = userVars.get('r_dim', 240)
    c_out = userVars.get('c_dim', 320)
    num_frames = mat.shape[0]
    if len(mat.shape) == 3:
        outpt = np.empty([num_frames,r_out,c_out],dtype='uint8')
        for i in range(num_frames):
            outpt[i, :, :] = scipy.misc.imresize(mat[i, :, :], (r_out, c_out))

    elif len(mat.shape) == 4:
        outpt = np.empty([num_frames,r_out,c_out,3],dtype='uint8')
        for i in range(num_frames):
            outpt[i,:,:,:] = scipy.misc.imresize(mat[i, :, :, :], (r_out, c_out, 3))

    return outpt


# Optionally identify number of "cone" pixels wiped
def analyze_cone(std_dev_mat, coords, userVars):
    counter = 0
    for coord in coords:
        r, c = coord
        if std_dev_mat[r, c] < userVars.get('cleaning_threshold'): counter += 1

    print('Cone pixels modified '+ str(counter))
    print('Percent of cone pixels modified ' + str(counter / len(coords) * 100))

    return (counter / len(coords) * 100)

# Rebuild pixels in US cone from original data
def Rebuild_Mat(mat, ori, coords):

    pixels_restored = 0

    for coord in coords:
        if not (mat[:, coord[0], coord[1]] == ori[:, coord[0], coord[1]]).all():
            pixels_restored += 1
            for f in range(mat.shape[0]):
                mat[f, coord[0], coord[1]] = ori[f, coord[0], coord[1]]


    print('Pixels restored: '+ str(pixels_restored))
    print('Percent of cone pixels restored ' + str(pixels_restored / len(coords) * 100))
    return mat


def process_DICOM(*vars):

    filename = vars[0]
    userVars = vars[1]
    userVars['rebuild'] = False
    #userVars['crop'] = False

    mat = DICOMtoImages(filename)
    ori_mat = mat.copy()

    if userVars.get('anonymize'):
        mat, std_dev_mat = Anonymize_Mat(mat, userVars)
        mat, coords, ori = crop_to_boundaries_thresh(mat, userVars, ori_mat)
        percent_modified = analyze_cone(std_dev_mat, coords, userVars)

    elif not userVars.get('anonymize'):
        percent_modified = 0
        mat, coords, ori = crop_to_boundaries_thresh(mat, userVars, ori_mat)

    if userVars.get('resize'): mat = Resize_Mat(mat, userVars)

    return mat.astype(np.uint8), percent_modified