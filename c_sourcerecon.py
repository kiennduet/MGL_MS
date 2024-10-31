import os
# test after meeting with Mark on 25 Sep 2024
from side_function import search_files
# from dask.distributed import Client
from osl import source_recon, utils
# # (0) define directories


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