from django.shortcuts import render
from django.http import HttpResponseRedirect

# Import forms
from django import forms
#from .forms import CheckDirForm
from .forms import AVIForm
from .forms import PickleForm
from .forms import HDF5Form

# Import functions from the check_directories.py file
from . import check_directories
from .check_directories import check_dirs

# Import functions from the to_video.py file
from . import to_video
from .to_video import to_video

# Import functions from the to_pickle.py file
from . import to_pickle
from .to_pickle import to_pickle

# Import functions from the to_hdf5.py file
from . import to_hdf5
from .to_hdf5 import to_hdf5

# Import supporting script files
from . import image_process

# Create your views here.

# View for the welcome page
def welcome(request):

    return render(request, 'welcome.html')

# View for the check directory page
def chkdir(request):
    # Declare variables within loops to prevent UnboundLocalError on first call
    process = ""

    # if this is a POST request we need to process data from the form
    if request.method == 'POST':
        # create a form instance and populate it with data from the request (i.e. from the user's form)
        process = check_dirs('/data')
        #form = CheckDirForm(request.POST)

        # otherwise create a blank form (GET would mean first time to page)
    #else:
        #form = CheckDirForm()

    context = {
        #'form': form,
        'process': process,
    }
    return render(request, 'chkdir.html', context)

# View for the create AVI page
def avi(request):
    # Declare variables within loops to prevent UnboundLocalError on first call
    process = ""

    # if this is a POST request we need to process data from the form
    if request.method == 'POST':
        # create a form instance and populate it with data from the request (i.e. from the user's form)
        form = AVIForm(request.POST)
        # check if the data is valid

        if form.is_valid():
            # process data in form.cleaned_data here then redirect user
            process = to_video(form.cleaned_data)
            #return HttpResponseRedirect('/welcome/')
    # otherwise create a blank form (GET would mean first time to page)
    else:
        form = AVIForm()

    context = {
        'form': form,
        'process': process,
    }
    return render(request, 'avi.html', context)

# View for the create pickle page
def pickle(request):
    # Declare variables within loops to prevent UnboundLocalError on first call
    process = ""

    # if this is a POST request we need to process data from the form
    if request.method == 'POST':
        # create a form instance and populate it with data from the request (i.e. from the user's form)
        form = PickleForm(request.POST)
        # check if the data is valid
        if form.is_valid():
            # process data in form.cleaned_data here then redirect user
            process = to_pickle(form.cleaned_data)
            #return HttpResponseRedirect('/welcome/')
    # otherwise create a blank form (GET would mean first time to page)
    else:
        form = PickleForm()

    context = {
        'form': form,
        'process': process,
    }
    return render(request, 'pickle.html', context)

# View for the create hdf5 page
def hdf5(request):
    # Declare variables within loops to prevent UnboundLocalError on first call
    process = ""

    # if this is a POST request we need to process data from the form
    if request.method == 'POST':
        # create a form instance and populate it with data from the request (i.e. from the user's form)
        form = HDF5Form(request.POST)
        # check if the data is valid
        if form.is_valid():
            # process data in form.cleaned_data here then redirect user
            process = to_hdf5(form.cleaned_data)
            #return HttpResponseRedirect('/welcome/')
    # otherwise create a blank form (GET would mean first time to page)
    else:
        form = HDF5Form()

    context = {
        'form': form,
        'process': process,
    }

    return render(request, 'hdf5.html', context)

