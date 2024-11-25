import os
# test after meeting with Mark on 25 Sep 2024
from side_function import search_files, get_subject_list
# from dask.distributed import Client
from osl import source_recon, utils

# # (0) define directories


path_preproc = r"/media/avitech/MyPassport/Kien/MEG_data/1_meg_preproc"
path_smri = r"/media/avitech/MyPassport/Kien/MEG_data/camcan/cc700/mri"

sub_nums = get_subject_list(file_path=r"/media/avitech/My Passport/Kien/MEG_data/updated_participants.tsv", data_type=1)
print(f"Preprocessing {len(sub_nums)} subjects ...")


dir_preproc, sub_nums = search_files(path_preproc, file_type = '.fif', sub_name=sub_nums, title="Preprocessing files")
dir_smri, sub_nums= search_files(path_smri, file_type = "T1w.nii.gz", sub_name=sub_nums, title="MRI files")    
dir_coregis = r"/media/avitech/MyPassport/Kien/MEG_data/2_meg_coregis"
dir_src = dir_coregis

# Settings
config = """
    source_recon:
    - forward_model:
        model: Single Layer
    - beamform_and_parcellate:
        freq_range: [0.5, 45] o
        chantypes: [mag, grad]
        rank: {meg: 60}
        parcellation_file: /media/avitech/MyPassport/Kien/MEG_data/0_sample_file/Glasser52_binary_space-MNI152NLin6_res-8x8x8_8mm.nii.gz
        method: spatial_basis
        orthogonalisation: symmetric
"""

# parallel processing does not seem to work well
# if _name_ == "_main_":
utils.logger.set_up(level="INFO")
#client = Client(n_workers=16, threads_per_worker=1)
# Source reconstruction
# https://osl.readthedocs.io/en/latest/stubs/osl.source_recon.batch.run_src_batch.html#osl.source_recon.batch.run_src_batch
source_recon.run_src_batch(
    config,
    outdir=dir_src,
    subjects=sub_nums,
    preproc_files=dir_preproc,
    smri_files=dir_smri,
    dask_client=False,
)