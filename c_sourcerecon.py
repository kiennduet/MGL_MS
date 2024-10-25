import os
# test after meeting with Mark on 25 Sep 2024
from side_function import search_files
# from dask.distributed import Client
from osl import source_recon, utils
# # (0) define directories


path_preproc = r"/media/avitech/CODE/Kiennd/2_MGL_MS/MEG_data_test/1_meg_prepro"
path_smri = r"/media/avitech/CODE/Kiennd/2_MGL_MS/MEG_data_test/0_smri"

sub_nums = ['sub-CC110033', 'sub-CC110037', 'sub-CC110045', 'sub-CC110056']
dir_preproc = search_files(path_preproc, type = '.fif', sub_name=sub_nums)
dir_smri = search_files(path_smri, type= "T1w.nii.gz", sub_name=sub_nums)    
dir_coregis = r"/media/avitech/CODE/Kiennd/2_MGL_MS/MEG_data_test/2_meg_coregis"
dir_src = dir_coregis


# Settings
config = """
    source_recon:
    - forward_model:
        model: Single Layer
    - beamform_and_parcellate:
        freq_range: [0.5, 45]
        chantypes: [mag, grad]
        rank: {meg: 60}
        parcellation_file: /media/avitech/CODE/Kiennd/2_MGL_MS/MEG_data_test/sample_file/Glasser52_binary_space-MNI152NLin6_res-8x8x8_8mm.nii.gz
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