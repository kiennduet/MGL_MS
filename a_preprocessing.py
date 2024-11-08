import os
import mne
from osl import preprocessing
import matplotlib
import matplotlib.pyplot as plt
from side_function import search_files

path_meg = r"/media/avitech/CODE/Kiennd/2_MGL_MS/MEG_data_test/0_meg"
path_preproc = r"/media/avitech/CODE/Kiennd/2_MGL_MS/MEG_data_test/1_meg_prepro"

dir_meg = search_files(path_meg, '.fif')
print(dir_meg)

config = """
    preproc:
    - set_channel_types: {EOG061: eog, EOG062: eog, ECG063: ecg}
    - filter: {l_freq: 0.1, h_freq: 125, method: iir, iir_params: {order: 5, ftype: butter}}
    - notch_filter: {freqs: 50 100}
    - resample: {sfreq: 250}
    - bad_segments: {segment_len: 500, picks: mag}
    - bad_segments: {segment_len: 500, picks: grad}
    - bad_segments: {segment_len: 500, picks: mag, mode: diff}
    - bad_segments: {segment_len: 500, picks: grad, mode: diff}
    - bad_channels: {picks: meg}
    - interpolate_bads: {}
"""
output = preprocessing.run_proc_batch(
    config, 
    dir_meg,
    outdir=path_preproc,
    overwrite=False,
    )
