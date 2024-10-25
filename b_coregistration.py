import os
from osl import source_recon, utils
# from dask.distributed import Client
from side_function import search_files

path_preproc = r"/media/avitech/CODE/Kiennd/2_MGL_MS/MEG_data_test/1_meg_prepro"
path_smri = r"/media/avitech/CODE/Kiennd/2_MGL_MS/MEG_data_test/0_smri"

sub_nums = ['sub-CC110033', 'sub-CC110037', 'sub-CC110045', 'sub-CC110056']
dir_preproc = search_files(path_preproc, type = '.fif', sub_name=sub_nums)
dir_smri = search_files(path_smri, type= "T1w.nii.gz", sub_name=sub_nums)    
dir_coregis = r"/media/avitech/CODE/Kiennd/2_MGL_MS/MEG_data_test/2_meg_coregis"

print(dir_smri)
print(dir_preproc)

# (1) prepare coregistration
# Settings
config = """
    source_recon:
    - extract_polhemus_from_info: {}
    - remove_stray_headshape_points: {}
    - compute_surfaces:
        include_nose: False
    - coregister:
        use_nose: True
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

