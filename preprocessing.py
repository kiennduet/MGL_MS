import os
import mne
from osl import preprocessing
import matplotlib.pyplot as plt

plt.show = lambda *args, **kwargs: None

def search_fif_files(directory):
    fif_file_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.fif'):
                fif_file_paths.append(os.path.join(root, file))
    return fif_file_paths


    raw = mne.io.read_raw_fif(fif_path, preload=True)
    print(raw.info)

    base_name = os.path.basename(fif_path)
    file_name, _ = os.path.splitext(base_name)  

    if selected_channels is not None:
        picks = mne.pick_types(raw.info, meg='mag', eeg=False) 
        selected_picks = picks[:selected_channels]  
    else:
        selected_picks = None 

    raw.plot_psd(fmin=0.1, fmax=100, tmin=0, tmax=None, picks=selected_picks, show=False)
    plt.savefig(f'{file_name}_psd.png')
    plt.close()



input_file_paths = r"/media/avitech/MyPassport/Kien/MEG_data/aamod_meg_maxfilt_00002"
preproc_file_paths = r"/media/avitech/MyPassport/Kien/MEG_data/meg_preproc"

input_files = search_fif_files(input_file_paths)

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
    input_files,
    outdir=preproc_file_paths,
    overwrite=False,
    )
