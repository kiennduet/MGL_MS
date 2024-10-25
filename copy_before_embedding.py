############################################
# collate all the files
# import os


import os
import shutil

# Lists to store successful and failed directories
dir_src = r"/media/avitech/CODE/Kiennd/2_MGL_MS/MEG_data_test/2_meg_coregis"
dir_flipped = r"/media/avitech/CODE/Kiennd/2_MGL_MS/MEG_data_test/3_meg_flipped"
sub_nums = ['sub-CC110033', 'sub-CC110037', 'sub-CC110045', 'sub-CC110056']
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