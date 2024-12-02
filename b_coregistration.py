import os
from osl import source_recon, utils
# from dask.distributed import Client
from side_function import search_files, search_subnums, get_subject_list

path_preproc = r"/media/avitech/MyPassport/Kien/MEG_data/1_meg_preproc"
path_smri = r"/media/avitech/MyPassport/Kien/MEG_data/camcan/cc700/mri"

sub_nums = get_subject_list(file_path=r"/media/avitech/My Passport/Kien/MEG_data/updated_participants.tsv", data_type=0)

dir_preproc, sub_nums = search_files(path_preproc, file_type = '.fif', sub_name=sub_nums, title="Preprocessing files")
dir_smri, sub_nums= search_files(path_smri, file_type = "T1w.nii.gz", sub_name=sub_nums, title="MRI files")    
dir_coregis = r"/media/avitech/MyPassport/Kien/MEG_data/2_meg_coregis"


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

