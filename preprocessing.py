import os
import mne
from osl import preprocessing
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt



def search_fif_files(directory):
    fif_file_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.fif'):
                fif_file_paths.append(os.path.join(root, file))
    return fif_file_paths

def analysis_meg(fif_path, selected_channels=None):
    # Mở file .fif và tải dữ liệu
    raw = mne.io.read_raw_fif(fif_path, preload=True)
    # In thông tin tóm tắt về dữ liệu
    print(raw.info)

    # Tạo tên file từ fif_path
    base_name = os.path.basename(fif_path)  # Lấy tên file từ đường dẫn
    file_name, _ = os.path.splitext(base_name)  # Tách tên file và phần mở rộng

    # # Vẽ dữ liệu miền thời gian
    # raw.plot(n_channels=5, scalings={'mag': 1e-12, 'grad': 4e-11, 'eeg': 1e-5}, title='Raw MEG Data', show=False)
    # plt.savefig(f'{file_name}_raw_meg_data.png')  # Lưu hình ảnh vào tệp với tên dựa trên fif_path
    # plt.close()  # Đóng hình ảnh để giải phóng bộ nhớ

    # Vẽ PSD chỉ cho các kênh đã chọn
    if selected_channels is not None:
        picks = mne.pick_types(raw.info, meg='mag', eeg=False)  # Chọn các kênh MEG
        selected_picks = picks[:selected_channels]  # Chọn một số kênh
    else:
        selected_picks = None  # Nếu không chỉ định, vẽ tất cả

    raw.plot_psd(fmin=0.1, fmax=100, tmin=0, tmax=None, picks=selected_picks, show=False)
    plt.savefig(f'{file_name}_psd_meg_data.png')  # Lưu hình ảnh vào tệp với tên dựa trên fif_path
    plt.close()  # Đóng hình ảnh

file_list = search_fif_files(r"D:\1_Work\6_MGL_MS\meg_analysis\data\aamod_meg_maxfilt_00002")

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
out_dir = r"D:\1_Work\6_MGL_MS\meg_analysis\data\preprocessed"
output = preprocessing.run_proc_batch(
    config,
    file_list,
    outdir=out_dir,
    overwrite=True,
    )

preproc_list = search_fif_files(r"D:\1_Work\6_MGL_MS\meg_analysis\data\preprocessed")
analysis_meg(file_list[0], selected_channels=5)
analysis_meg(preproc_list[0], selected_channels=5)