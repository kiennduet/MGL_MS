import os
import pickle
from side_function import search_subnums

dir_flipped = r"/media/avitech/MyPassport/Kien/MEG_data/3_meg_flipped" #edit

# Extract subject codes using the `search_subnums` function
sub_nums = search_subnums(
    directory=dir_flipped,
    prefix="sub",
    separator="-",
    id_length=8
)

# Path to save the .pkl file
subnums_path = 'sub_nums.pkl'
with open(subnums_path, 'wb') as file:
    pickle.dump(sub_nums, file)
print(f"Saved subject codes to file: {subnums_path}")

