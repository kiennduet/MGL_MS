import os
from osl import source_recon, utils

import osl.source_recon as osl_sr
osl_sr.setup_fsl(directory='/media/avitech/CODE/Kiennd/2_MGL_MS/fsl')


def search_files(directory, type, sub_name=None):
    file_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(type):
                if sub_name is None or any(name in file for name in sub_name):
                    file_paths.append(os.path.join(root, file))
    return file_paths

path_preproc = r"/media/avitech/MyPassport/Kien/MEG_data/1_meg_preproc"
path_mri = r"/media/avitech/MyPassport/Kien/MEG_data/0_mri_test"

sub_nums = ['sub-CC110033']

dir_preproc = search_files(path_preproc, type = '.fif', sub_name=sub_nums)
dir_smri = search_files(path_mri, type= "T1.nii", sub_name=sub_nums)    
dir_coregis = r"/media/avitech/MyPassport/Kien/MEG_data/2_meg_coregis"


print(dir_preproc)
print(dir_smri)


# Settings
config = """
    source_recon:
    - extract_polhemus_from_info: {}  
    - remove_stray_headshape_points: {}
    - compute_surfaces:
        include_nose: False
    - coregister:
        use_nose: False
        use_headshape: True
        allow_smri_scaling: True
"""


# config = """
#     source_recon:
#     - extract_polhemus_from_info: {}  
#     - remove_stray_headshape_points: {}
#     - compute_surfaces:
#         include_nose: False
#     - coregister:
#         use_nose: False
#         use_headshape: True
#         allow_smri_scaling: True
#         #n_init: 2
# """

utils.logger.set_up(level="INFO")
source_recon.run_src_batch(
    config,
    outdir=dir_coregis,
    subjects=sub_nums,
    preproc_files=dir_preproc,
    smri_files=dir_smri,

)

