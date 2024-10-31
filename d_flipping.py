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

path_preproc = r"/media/avitech/MyPassport/Kien/MEG_data/1_meg_preproc"
path_smri = r"/media/avitech/MyPassport/Kien/MEG_data/camcan/cc700/mri"

sub_nums = ['sub-CC110033', 'sub-CC110037', 'sub-CC110045', 'sub-CC110056', 
            'sub-CC110069', 'sub-CC110087', 'sub-CC110098', 'sub-CC110101', 
            'sub-CC110126', 'sub-CC110174', 'sub-CC110182', 'sub-CC110187', 
            'sub-CC110319', 'sub-CC110411', 'sub-CC110606', 'sub-CC112141', 
            'sub-CC120008', 'sub-CC120049', 'sub-CC120061', 'sub-CC120065', 
            'sub-CC120120', 'sub-CC120137', 'sub-CC120166', 'sub-CC120182', 
            'sub-CC120184', 'sub-CC120208', 'sub-CC120212', 'sub-CC120218', 
            'sub-CC120264', 'sub-CC120276', 'sub-CC120309', 'sub-CC120313']

dir_preproc = search_files(path_preproc, type = '.fif', sub_name=sub_nums)
dir_smri = search_files(path_smri, type= "T1w.nii.gz", sub_name=sub_nums)     
dir_coregis = r"/media/avitech/MyPassport/Kien/MEG_data/2_meg_coregis"
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