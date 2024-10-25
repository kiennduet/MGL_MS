from osl import source_recon
import pickle
import os
from side_function import search_files

# test after meeting with Mark on 25 Sep 2024
# (0) define directories
# setup_file = "M3_010_002_setup.py"
# with open(setup_file) as f:
#     code = f.read()
#     exec(code)

# # files for new step:
# subjects = codes

# # files for new step:
# subject_numbers = codes
# subject_directories = [f"{code}" for code in codes]
# subject_directories_full = [f"{dir_src}/{code}" for code in codes]

from side_function import search_files

path_preproc = r"/media/avitech/CODE/Kiennd/2_MGL_MS/MEG_data_test/1_meg_prepro"
path_smri = r"/media/avitech/CODE/Kiennd/2_MGL_MS/MEG_data_test/0_smri"

sub_nums = ['sub-CC110033', 'sub-CC110037', 'sub-CC110045', 'sub-CC110056']
dir_preproc = search_files(path_preproc, type = '.fif', sub_name=sub_nums)
dir_smri = search_files(path_smri, type= "T1w.nii.gz", sub_name=sub_nums)    
dir_coregis = r"/media/avitech/CODE/Kiennd/2_MGL_MS/MEG_data_test/2_meg_coregis"
dir_src = dir_coregis

subject_directories = sub_nums

# '/media/avitech/CODE/Kiennd/2_MGL_MS/MEG_data_test/2_meg_coregis/sub-CC110033/parc'

# (1) Find a good template subject to match others to
# template = source_recon.find_template_subject(dir_output, subject_directories, standardize=True)
template = source_recon.find_template_subject(
    dir_src, subject_directories, n_embeddings=15, standardize=True
)
# subject 2220 selected on 22 July 2024
# subject 2201 selected on 5 August 2024

# (2) Run sign flipping 
config = f"""
    source_recon:
    - fix_sign_ambiguity:
        template: {template}
        n_embeddings: 15
        standardize: True
        n_init: 3               
        n_iter: 3000
        max_flips: 20
"""
# flags = source_recon.run_src_batch(config, dir_src, subject_directories[slice(1, 10)])
flags = source_recon.run_src_batch(config, dir_src, subject_directories)