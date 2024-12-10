import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from side_function import search_files, get_subject_list


# Đường dẫn file TSV
file_path = '/media/avitech/MyPassport/Kien/MEG_data/updated_participants.tsv' 
data = pd.read_csv(file_path, sep='\t')

path_preproc = r"/media/avitech/MyPassport/Kien/MEG_data/1_meg_preproc"
path_smri = r"/media/avitech/MyPassport/Kien/MEG_data/camcan/cc700/mri"

sub_nums = get_subject_list(file_path=r"/media/avitech/My Passport/Kien/MEG_data/updated_participants.tsv", data_type=[0,1])
print(f"Preprocessing {len(sub_nums)} subjects ...")

dir_preproc, sub_nums = search_files(path_preproc, file_type = '.fif', sub_name=sub_nums, title="Preprocessing files")
dir_smri, sub_nums= search_files(path_smri, file_type = "T1w.nii.gz", sub_name=sub_nums, title="MRI files")   


filtered_data = data[data['participant_id'].isin(sub_nums)]

# Vẽ biểu đồ phân bố
plt.figure(figsize=(10, 6))
sns.histplot(filtered_data['age'], bins=25, kde=True, color='red', label='Age Distribution')
plt.title(f'Age Distribution of {len(sub_nums)} Subjects', fontsize=16)
plt.xlabel('Age', fontsize=14)
plt.ylabel('Frequency', fontsize=14)
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()
