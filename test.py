# new run for 52 parcellation on 20240816
# run from sss maxfiltered data after talk with Chet on 20240928
import os
# from dask.distributed import Client
from osl import source_recon, utils
from a_preprocessing import search_files
import osl.source_recon as osl_sr
osl_sr.setup_fsl(directory='/media/avitech/CODE/Kiennd/2_MGL_MS/fsl')


# (0) define directories
# setup_file = "M3_010_002_setup.py"
# with open(setup_file) as f:
#     code = f.read()
#     exec(code)
path_preproc = r"/media/avitech/MyPassport/Kien/MEG_data/1_meg_preproc"
path_mri = r"/media/avitech/MyPassport/Kien/MEG_data/0_mri_test"

dir_preproc = search_files(path_preproc, type = '.fif', sub_name=sub_nums)
dir_smri = search_files(path_mri, type= "T1.nii", sub_name=sub_nums)    
dir_coregis = r"/media/avitech/MyPassport/Kien/MEG_data/2_meg_coregis"

sub_nums = ['sub-CC110033']

# (1) prepare coregistration
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

# (2) run coregistration
utils.logger.set_up(level="INFO")
# client = Client(n_workers=16, threads_per_worker=1)

# Run coregistration
source_recon.run_src_batch(
    config,
    outdir=dir_coregis,
    subjects=sub_nums,
    preproc_files=dir_preproc,
    smri_files=dir_smri,
    dask_client = False,
)