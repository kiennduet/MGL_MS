import os
import mne
import matplotlib
import matplotlib.pyplot as plt
from side_function import search_files, get_subject_list, search_files_v3

path_meg = r"/media/avitech/My Passport/Kien/MEG_data/camcan/cc700/meg/pipeline/release005/BIDSsep/derivatives_rest/aa/AA_movecomp/aamod_meg_maxfilt_00002"
path_preproc = r"/media/avitech/CODE/Kiennd/2_MGL_MS/MEG_data_test/1_meg_prepro"

sub_nums = get_subject_list(file_path=r"/media/avitech/My Passport/Kien/MEG_data/updated_participants.tsv", data_type=[1])
dir_meg,_ = search_files_v3(directory=path_meg, file_type='.fif', sub_name=sub_nums, title="Raw MEG files matched")