from side_function import search_subnums, search_files, get_subject_list


sub_nums = search_subnums(directory="/media/avitech/MyPassport/Kien/MEG_data/2_meg_coregis")
sub_nums1 = search_subnums(directory="/media/avitech/MyPassport/Kien/MEG_data/1_meg_preproc")
sub_nums2 = get_subject_list(file_path=r"/media/avitech/My Passport/Kien/MEG_data/updated_participants.tsv", data_type= [0,1])
