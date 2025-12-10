# Loneliness-Signature
This repository contains code in support of "A generalizable neural signature of perceived loneliness".

- The code was written in Python 3.8.10
- Below I describe the contents of this repository.

## `code`
The [code](code/) folder contains code to run a slurm array to 1) format task fMRI data by applying the Schaefer 400 7-network parcelation atlas; and 2) create functional connectivity matrices from the outputs of step 1 and apply the loneliness signature onto them.

