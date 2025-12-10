from config import RESULTS_DIR
import pickle

# set up 
sub = f'sub-{argv[1]}'
output_dir = '~/results/HCPtaskfMRI'

# 1) Load TPLS model and hyperparameters 
# Predict on train data
print("[INFO] Building final model...")
with open(os.path.join(RESULTS_DIR, 'HCP_loneliness_mdl.pkl'), 'rb') as f:
    mdl = pickle.load(f)
compval = 10
threshval = 0.2
betamap_final, intercept_final = mdl.makePredictor(compval, threshval)

# 2) Load parcellated task fMRI data, create functional connectivity matrices, and apply loneliness siguate
# tasks = ['tfMRI_EMOTION', 'tfMRI_GAMBLING', 'tfMRI_LANGUAGE', 'tfMRI_MOTOR', 'tfMRI_RELATIONAL']

all_results = []
for scan in ['tfMRI_EMOTION', 'tfMRI_GAMBLING', 'tfMRI_LANGUAGE', 'tfMRI_MOTOR', 'tfMRI_RELATIONAL']:
    file_list = natsorted(glob(opj(output_dir, f'parcellation/sub-*taskDiadXconvoX{scan}*hdf5')))
    
    for f in file_list:
        sub = os.path.basename(f).split('_')[0]
        #print(sub)
        roi = Brain_Data(f)
                
        # create FC matrix
        run_dat = np.nan_to_num(roi.data, nan=0.0, posinf=1.0, neginf=-1.0)
        fc_matrix = np.corrcoef(run_dat)
        fc_vector = fc_matrix[np.tril_indices(fc_matrix.shape[0], k=-1)]
      
        # Clip to avoid infinities in Fisher transform
        X_clipped = np.clip(fc_vector, -0.999999, 0.999999)
        fc_vector_z = np.arctanh(X_clipped)
        
        # Apply signature to functional connectivity
        loneliness_expression = intercept_final + fc_vector_z @ betamap_final 

        all_results.append({
            "id": f"0{sub[4:6]}-{sub[-1]}",
            "task": scan,
            "loneliness_expression": loneliness_expression[0][0]
                })
    print(f'Done: {sub}-{scan}.')
        
# Merge data into pandas dataframe
subject_results = pd.DataFrame(all_results)      
subject_results.to_csv(opj(output_dir, sub f'{sub}_loneliness_expression_tfMRI.csv'))
