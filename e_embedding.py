import os
from osl_dynamics.data import Data
from side_function import search_files, get_subject_list

# test post meeting Mark 20240925

# (0) define directories
# setup_file = "M3_010_002_setup.py"
# with open(setup_file) as f:
#     code = f.read()Nay
#     exec(code)

# # (0) file locations
dir_flipped = r"/media/avitech/MyPassport/Kien/MEG_data/3_meg_flipped"
sub_nums = sub_nums = get_subject_list(file_path=r"/media/avitech/My Passport/Kien/MEG_data/updated_participants.tsv", data_type=[0,1])
_, sub_nums = search_files(dir_flipped , file_type = '.fif', sub_name=sub_nums, title="Flipped files")

dir_before_pca = r"/media/avitech/MyPassport/Kien/MEG_data/4_meg_embedded"
dir_training = r"/media/avitech/MyPassport/Kien/MEG_data/5_meg_training"


file_paths,_ = search_files(directory=dir_flipped, file_type= "sflip_parc-raw.fif", sub_name=sub_nums)

methods = {
    "tde_pca": {"n_embeddings": 15, "n_pca_components": 120},
    "standardize": {},
}

log_file_path = dir_flipped + "/log_file.txt"

with open(log_file_path, 'w') as log_file:
    for file_path in file_paths:
        try:
            with open(file_path, 'r') as file:
                data = Data(file_path, picks="misc", reject_by_annotation="omit")
                data.prepare(methods)
                print(f"File ok: {file_path}", file=log_file)
        except FileNotFoundError:
            print(f"File not found: {file_path}", file=log_file)
        except Exception as e:
            print(f"An error occurred while processing {file_path}: {e}", file=log_file)

########################

##################3

# import re
# # Define the pattern to match 1098, 1059, or 2431 before "sflip"
# pattern = re.compile(r'(1098|1059|2431)sflip')
# # Filter out the file paths
# filtered_file_paths = [file_path for file_path in file_paths if not pattern.search(file_path)]
# # Print the filtered list of file paths
# print("Filtered file paths:", filtered_file_paths)
#
#

########################

#______________________________________________________________________
# # (1) load data for further processing
from osl_dynamics.data import Data
parc_files = file_paths
data = Data(parc_files, picks="misc", reject_by_annotation="omit")
data.save(dir_before_pca)


#______________________________________________________________________



# # (1.5) save data for 126 subjects that end up in the final analysis
# base_path = "/home/gnagels/Data/DPhilData/analyses/TDE-HMM_20240806a/training_flat_20240806a"
# # parc_files = [base_path + "/" + code + "sflip_parc-raw.fif" for code in TDE_coded_codes]
# data = Data(parc_files, picks="misc", reject_by_annotation="omit")
# data.save(dir_before_pca)
# problem was in overwriting a directory that already had more files
###########################3

#______________________________________________________________________
# (2) run tde and pca
methods = {
    "tde_pca": {"n_embeddings": 15, "n_pca_components": 120},
    "standardize": {},
}
data.prepare(methods)
data.save(dir_training)
data.delete_dir()
#______________________________________________________________________