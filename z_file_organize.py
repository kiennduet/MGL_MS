import os

# (0) directories
dir_fif = "/home/gnagels/Data/DPhilData/startdata/rawfifs/P300_sss"
dir_smri = '/home/gnagels/Data/DPhilData/startdata/sMRI'

date = "20241007a"
dir_base = "/home/gnagels/Data/DPhilData/analyses/M300_" + date
os.makedirs(dir_base, exist_ok=True)
dir_preproc = dir_base + '/sss_PreProc_'+ date
os.makedirs(dir_preproc, exist_ok=True)

dir_src = dir_base + '/sss_src_'+ date
os.makedirs(dir_src, exist_ok=True)
dest_dir = dir_base + '/sss_parc_'+ date
os.makedirs(dest_dir, exist_ok=True)
dir_flipped = dir_base + '/training_flat_'+ date
os.makedirs(dir_flipped, exist_ok=True)
dest_dir = dir_base + '/sss_parc_'+ date
os.makedirs(dest_dir, exist_ok=True)
dir_training = dir_base +'/sss_train'+ date
os.makedirs(dir_training, exist_ok=True)
dir_before_pca = dir_base +'/sss_dir_before_pca_'+ date
os.makedirs(dir_before_pca, exist_ok=True)
log_file_path = dir_base + '/sss_log_'+ date + '.txt'
pickle_directory = dir_base + '/Pickled_files_'+ date
os.makedirs(dir_flipped, exist_ok=True)
dir_models = dir_base + '/models'
os.makedirs(dir_models, exist_ok=True)
dir_save_model = dir_models + '/model_1001'
os.makedirs(dir_save_model, exist_ok=True)

# (1) files
# codes_sss = ['0947', '0987', '0988', '0992', '0995', '0996', '0997', \
#              '0999', '1000', '1001', '1002', '1005', '1006', '1007', \
#              '1008', '1009', '1010', '1017', '1018', '1023', '1024', \
#              '1025', '1028', '1031', '1033', '1035', '1037', '1052', \
#              '1053', '1059', '1062', '1073', '1078', '1080', '1082', \
#              '1097', '1098', '1106', '2096', '2102', '2103', '2121', \
#              '2122', '2143', '2144', '2147', '2150', '2151', '2163', \
#              '2164', '2169', '2170', '2172', '2173', '2174', '2179', \
#              '2180', '2189', '2190', '2192', '2193', '2194', '2201', \
#              '2202', '2203', '2206', '2211', '2215', '2219', '2220', \
#              '2221', '2224', '2226', '2227', '2228', '2233', '2234', \
#              '2235', '2238', '2239', '2241', '2252', '2257', '2264', \
#              '2266', '2267', '2268', '2277', '2278', '2297', '2298', \
#              '2300', '2304', '2305', '2306', '2307', '2311', '2312', \
#              '2313', '2314', '2317', '2318', '2319', '2324', '2325', \
#              '2327', '2328', '2341', '2342', '2343', '2346', '2357', \
#              '2359', '2363', '2364', '2371', '2376', '2377', '2378', \
#              '2379', '2381', '2386', '2388', '2396', '2399', '2410', \
#              '2412', '2413', '2414', '2416', '2421', '2426', '2427', \
#              '2431', '2440', '2447', '2448']
#
# subjects_to_remove = ['0995', '2241'] # did not make it through preprocessing
# codes_sss = [code for code in codes_sss if code not in subjects_to_remove]
#
# # # weird coregistration results:
# # codes_sss = ['1098', '2103', '2174', '2324', '2201', '2228', '2431']
#
# subjects_to_remove = ['1098', '2103', '2174', '2324', '2201', '2228', '2431']
# codes_sss = [code for code in codes_sss if code not in subjects_to_remove]

# these files went through source recon and parcellation
codes_sss =  ['0947', '0987', '0988', '0992', '0996', '0997', '0999', '1000', \
              '1001', '1002', '1005', '1006', '1007', '1008', '1009', '1010', \
              '1017', '1018', '1023', '1024', '1025', '1028', '1031', '1033', \
              '1035', '1037', '1052', '1053', '1062', '1073', '1078', '1080', \
              '1082', '1097', '1106', '2102', '2121', '2122', '2143', '2144', \
              '2147', '2150', '2151', '2163', '2164', '2169', '2170', '2172', \
              '2173', '2179', '2180', '2189', '2190', '2192', '2193', '2194', \
              '2202', '2203', '2206', '2211', '2215', '2219', '2220', '2221', \
              '2224', '2226', '2227', '2233', '2234', '2235', '2238', '2239', \
              '2252', '2257', '2264', '2266', '2267', '2268', '2277', '2278', \
              '2297', '2298', '2300', '2304', '2305', '2306', '2307', '2311', \
              '2312', '2313', '2314', '2317', '2318', '2319', '2325', '2327', \
              '2328', '2341', '2342', '2343', '2346', '2357', '2359', '2363', \
              '2364', '2371', '2376', '2377', '2378', '2379', '2381', '2386', \
              '2388', '2396', '2399', '2410', '2412', '2413', '2414', '2416', \
              '2421', '2426', '2427', '2440', '2447', '2448']



files_fif = []
# codes = [f"{number:04}" for number in code_meg_id]
for sub in codes_sss:
     files_fif.append(f"{dir_fif}/{sub}_P300_sss.fif")

files_MRI = []
for sub in codes_sss:
    filename = f"MEG_{sub}_cMRI_T1.nii.gz"
    file_path = os.path.join(dir_smri, filename)
    if os.path.isfile(file_path):
        files_MRI.append(file_path)
    else:
        files_MRI.append(f"no MRI for subject {sub}")

files_preproc = []
for sub in codes_sss:
    files_preproc.append(f"{dir_preproc}/{sub}_P300_sss/{sub}_P300_sss_preproc-raw.fif")

subject_directories = codes_sss
subject_directories_full = [f"{dir_src}/{code}" for code in codes_sss]

codes=codes_sss

# (1) files


# range = slice(1, 10)
# codes = codes[range]
# codes_sss = codes_sss[range]
# files_fif = files_fif[range]
# files_MRI = files_MRI[range]
# files_preproc = files_preproc[range]
# subject_directories = subject_directories[range]
# subject_directories_full = subject_directories_full[range]