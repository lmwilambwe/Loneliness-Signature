#!/usr/bin/env python3
import os
import sys
from sys import argv
from glob import glob
from os.path import join as opj
import logging
from natsort import natsorted 
from tqdm import tqdm
import numpy as np
import pandas as pd

from nltools.data import Brain_Data, Design_Matrix 
from nltools.mask import expand_mask, roi_to_brain
from nilearn import datasets
from nilearn.plotting import plot_roi
import h5py

import statsmodels.formula.api as smf
from scipy.stats import pearsonr
from scipy import stats
from scipy.stats import ttest_ind, ttest_rel



# Pull in variables (from Slurm submission)
sub = f'sub-{argv[1]}'
print(sub)

# directories
denoised_dir = '~/MNINonLinear/Results/tfMRI_EMOTION_LR'
output_dir = '~/data/taskfMRI'

# atlas that will be used for deterministic alignment
atlas_file = datasets.fetch_atlas_schaefer_2018(n_rois=400, yeo_networks=7)
atlas_img = Brain_Data(atlas_file['maps'])
atlas_x_mask= expand_mask(atlas_img)

# Set trim parameters  <--------------------- (CHANGE THIS SETUP FOR HCP); comment out if not needed
trim_start = 7
trim_end   = 7

############################# FUNCTIONS
def check_dir(folder):
    if os.path.isdir(folder) == False:
        os.makedirs(folder)

# <--------------------- (CHANGE THIS FUNCTION FOR HCP) the file structure will be different 
def make_fc(f, scan,trim_start,trim_end):
    """
    Function for creating functional connectivity matrices for conversation data
    
    """
    # get subject name and task file info
    sub = os.path.basename(f).split('_')[0]
        
    # check if file is alread processed
    outfile = opj(output_dir, f'parcellation/{sub}_{scan}_schaefer400p7n.hdf5')
        
    if os.path.exists(outfile):
        print(f"File '{outfile}' exists. Skipping the for loop.")
    else:
        print(sub)
        data = Brain_Data(f)
        
        # trim the firt and last 7TRs 
        data.data = data.data[trim_start:-trim_end,:]

        # apply parcellation and save 
        roi = Brain_Data()
        roi.data = data.extract_roi(atlas_img)
        print(f'Data shape: {roi.data.shape}')
        
        # save parcellated brain image
        roi.write(outfile)

        print(f'Done parcellating files for: {sub}-{scan}.')
        
for scan in ['tfMRI_EMOTION', 'tfMRI_GAMBLING', 'tfMRI_LANGUAGE', 'tfMRI_MOTOR', 'tfMRI_RELATIONAL']:
    
    # process the videos 
    files_tfMRI = natsorted(glob(opj(denoised_dir, sub, f'MNINonLinear/Results/{scan}*nii.gz')))
    
    for file in tqdm(files_tfMRI):
        make_fc(file, scan, trim_start,trim_end)
            
    print(f'Completed parcellating data for {sub}-{scan}.')


            
