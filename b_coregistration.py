import os
from osl import source_recon, utils
# from dask.distributed import Client
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

