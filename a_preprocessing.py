import os
import mne
from osl import preprocessing
import matplotlib
import matplotlib.pyplot as plt



def search_files(directory, type):
    fif_file_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(type):
                fif_file_paths.append(os.path.join(root, file))
    return fif_file_paths

def plot_meg(fif_path, selected_channels=None):

    raw = mne.io.read_raw_fif(fif_path, preload=True)
    print(raw.info)

    # Tạo tên file từ fif_path
    base_name = os.path.basename(fif_path)  # Lấy tên file từ đường dẫn
    file_name, _ = os.path.splitext(base_name)  # Tách tên file và phần mở rộng

    # Vẽ PSD chỉ cho các kênh đã chọn
    if selected_channels is not None:
        picks = mne.pick_types(raw.info, meg='mag', eeg=False)  # Chọn các kênh MEG
        selected_picks = picks[:selected_channels]  # Chọn một số kênh
    else:
        selected_picks = None  # Nếu không chỉ định, vẽ tất cả

    raw.plot_psd(fmin=0.1, fmax=100, tmin=0, tmax=None, picks=selected_picks, show=False)
    plt.savefig(f'{file_name}_psd.png')
    plt.close()

input_file_paths = r"D:\1_Work\6_MGL_MS\meg_analysis\data\aamod_meg_maxfilt_00002"
preproc_file_paths = r"D:\1_Work\6_MGL_MS\meg_analysis\data\preprocessed"

input_files = search_files(input_file_paths, '.fif')
preproc_files = search_files(preproc_file_paths, '.fif')

if preproc_files:
    print("Preprocessed files already exist. Do you want to overwrite them? (y/n) ")
    overwrite = True if input().lower() in ["y", "yes"] else False

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
