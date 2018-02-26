from django import forms


# Form for the check directories script
#class CheckDirForm(forms.Form):
    #dir = forms.CharField(initial="/data")

# Form for the avi inputs
class AVIForm(forms.Form):
    #Core Features
    dcm_compressed = forms.BooleanField(initial=True, required=False)
    anonymize = forms.BooleanField(initial=True, required=False, widget=forms.CheckboxInput(attrs={'onclick': 'aviAnonymizeOptions()'}))
    image_thresholding = forms.ChoiceField(choices=[('1', 'binary'), ('2', 'Otsu')], initial='binary', required=False, help_text='image_thresholding_tr')
    cleaning_threshold = forms.FloatField(initial=.0000001, required=False, help_text='cleaning_threshold_tr')
    crop = forms.BooleanField(initial=True, required=False)
    resize = forms.BooleanField(initial=True, required=False, widget=forms.CheckboxInput(attrs={'onclick': 'aviResizeOptions()'}))
    r_dim = forms.IntegerField(initial=400, required=True, help_text='r_dim_tr')  # only required if resize == True
    c_dim = forms.IntegerField(initial=608, required=True, help_text='c_dim_tr')  # only required if resize == True
    rgb = forms.BooleanField(initial=False, required=False)
    output_type = forms.ChoiceField(choices=[('1', 'avi'), ('2', 'mpeg')], initial='.avi', required=False)
    #Advanced Features
    image_increment = forms.IntegerField(initial=10, required=False)
    fps = forms.IntegerField(initial=10, required=False)
    gamma = forms.FloatField(initial=4, required=False, help_text='gamma_tr')
    verbose = forms.BooleanField(initial=False, required=False)

# Form for the pickle inputs
class PickleForm(forms.Form):
    #Core features
    dcm_compressed = forms.BooleanField(initial=True, required=False)
    anonymize = forms.BooleanField(initial=True, required=False, widget=forms.CheckboxInput(attrs={'onclick': 'pickleAnonymizeOptions()'}))
    image_thresholding = forms.ChoiceField(choices=[('1','binary'), ('2','Otsu')], initial='binary', required=False, help_text='image_thresholding_tr')
    cleaning_threshold = forms.FloatField(initial=.0000001, required=False, help_text='cleaning_threshold_tr')
    crop = forms.BooleanField(initial=True, required=False)
    resize = forms.BooleanField(initial=True, required=False, widget=forms.CheckboxInput(attrs={'onclick': 'pickleResizeOptions()'}))
    r_dim = forms.IntegerField(initial=240, required=False, help_text='r_dim_tr')
    c_dim = forms.IntegerField(initial=320, required=False, help_text='c_dim_tr')
    rgb = forms.BooleanField(initial=True, required=False)
    pickle_file = forms.CharField(initial='out.p', required=False)
    #Advanced features
    image_increment = forms.IntegerField(initial=10, required=False)
    verbose = forms.BooleanField(initial=False, required=False)

# Form for the HDF5 inputs
class HDF5Form(forms.Form):
    #Core features
    dcm_compressed = forms.BooleanField(initial=True, required=False)
    anonymize = forms.BooleanField(initial=True, required=False, widget=forms.CheckboxInput(attrs={'onclick': 'hdf5AnonymizeOptions()'}))
    image_thresholding = forms.ChoiceField(choices=[('1','binary'), ('2','Otsu')], initial='binary', required=False, help_text='image_thresholding_tr')
    cleaning_threshold = forms.FloatField(initial=.0000001, required=False, help_text='cleaning_threshold_tr')
    crop = forms.BooleanField(initial=True, required=False)
    resize = forms.BooleanField(initial=True, required=False, widget=forms.CheckboxInput(attrs={'onclick': 'hdf5ResizeOptions()'}))
    r_dim = forms.IntegerField(initial=240, required=False, help_text='r_dim_tr')
    c_dim = forms.IntegerField(initial=320, required=False, help_text='c_dim_tr')
    rgb = forms.BooleanField(initial=True, required=False)
    h5_file = forms.CharField(initial='out.hdf', required=False)
    #Advanced features
    image_increment = forms.IntegerField(initial=10, required=False)
    compression = forms.ChoiceField(choices=[('1','gzip'), ('2','lzf')], initial='gzip', required=False)
    verbose = forms.BooleanField(initial=True, required=False)
