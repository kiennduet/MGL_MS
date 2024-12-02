from osl import source_recon
import pickle
import os
from side_function import search_files, get_subject_list

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


path_preproc = r"/media/avitech/MyPassport/Kien/MEG_data/1_meg_preproc"
path_smri = r"/media/avitech/MyPassport/Kien/MEG_data/camcan/cc700/mri"

sub_nums = get_subject_list(file_path=r"/media/avitech/My Passport/Kien/MEG_data/updated_participants.tsv", data_type=[0,1])

dir_preproc, sub_nums = search_files(path_preproc, file_type = '.fif', sub_name=sub_nums, title="Preprocessing files")
dir_smri, sub_nums = search_files(path_smri, file_type = "T1w.nii.gz", sub_name=sub_nums, title="MRI files")      

dir_coregis = r"/media/avitech/MyPassport/Kien/MEG_data/2_meg_coregis"
dir_src = dir_coregis

subject_directories = sub_nums


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