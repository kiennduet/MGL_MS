import os
import shutil
from side_function import search_files, get_subject_list


# Lists to store successful and failed directories
dir_src = r"/media/avitech/MyPassport/Kien/MEG_data/2_meg_coregis"
dir_flipped = r"/media/avitech/MyPassport/Kien/MEG_data/3_meg_flipped"

sub_nums = get_subject_list(file_path=r"/media/avitech/My Passport/Kien/MEG_data/updated_participants.tsv", data_type=[0,1])
_, sub_nums = search_files(dir_src , file_type = '.fif', sub_name=sub_nums, title="Flipped files")

subject_directories = sub_nums

successful_dirs = []
failed_dirs = []

# Iterate over subject directories and try copying files
for subdir in subject_directories:
    try:
        # Construct the old and new file paths
        old_name = f"{dir_src}/{subdir}/{subdir}_sflip_parc-raw.fif"
        new_name = f"{dir_flipped}/{subdir}_sflip_parc-raw.fif"

        # Check if the source file exists before copying
        if os.path.exists(old_name):
            shutil.copy(old_name, new_name)
            print(f"Copied {old_name} to {new_name}")
            successful_dirs.append(subdir)  # Add to success list
        else:
            print(f"Source file {old_name} does not exist.")
            failed_dirs.append(subdir)  # Add to failure list if file does not exist
    except Exception as e:
        print(f"Failed to copy {old_name} to {new_name}: {str(e)}")
        failed_dirs.append(subdir)  # Add to failure list if any error occurs

# Output the results
print("\nSuccessful directories:")
print(successful_dirs)

print("\nFailed directories:")
print(failed_dirs)