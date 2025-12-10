#!/bin/bash

# Run within pipeline code/ directory:
# sbatch slurm_parcellate_hcp.sh

# Set partition
#SBATCH --partition=all

# How long is the job (HH:MM:SS)?
#SBATCH --time=01:00:00 

#SBATCH --cpus-per-task=1  # Adjust CPU allocation based on your needs
#SBATCH --mem-per-cpu=2G  # Memory allocation per CPU

# Name of jobs?
#SBATCH --job-name=parcellate

# Where to output log files?
#SBATCH --output='~/code/logs/parcellate-%A_%a.log'

# Number jobs to run in parallel, pass index subject ID (e.g. sub-0**)
#SBATCH --array=032,371,052,322,221,021,242,251,361,051,312,131,481,181,551,231,601,031,171,441,461,472,422,502,272,511,492,571,541,401,462,062,081,592,412,302,292,522,432,261,392,252,351,151,222,311,192,121,201,092,122,202,381,271,191,111,101,172,301,042,281,572,411,091,431,262,332,491,071,041,232,072,291,581,082,532,591,061,552,442,402,482,022,352,372,182,331,342,602,452,382,421,112,282,162,542,211,341,471,521,321,561,391,582,562,132,531,212,102,501,451,512,161,241,362,152

# Update with your email 
#SBATCH --mail-user=####@####.edu
#SBATCH --mail-type=BEGIN,END,FAIL

module purge
# Print job submission info

echo "======================================"
echo "Starting Slurm job ID:" $SLURM_JOB_ID
echo "Slurm array task ID:" $SLURM_ARRAY_TASK_ID
date
echo "Parcellating task fMRI data files..."
echo "======================================"

# Set subject ID based on array index
printf -v subj "%03d" $SLURM_ARRAY_TASK_ID

# Step 1: Apply parcellation atlas
echo "[STEP 1] Running..."
python parcellate_HCP.py "$subj"
echo "[STEP 1] Done."
date

# Step 2: Apply loneliness signature and calculate expression
echo "[STEP 2] Running..."
python loneliness_signature_HCP.py "$subj"
echo "[STEP 2] Done."
date

