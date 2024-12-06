dir_models = "/media/avitech/MyPassport/Kien/MEG_data/7_models_full"
dir_training = r"/media/avitech/MyPassport/Kien/MEG_data/5_meg_training"
dir_before_pca = r"/media/avitech/MyPassport/Kien/MEG_data/4_meg_embedded"

for i_model_number in range(2201, 2202):  

# # Define both ranges and chain them together
# for i_model_number in chain(range(301, 311), range(401, 411), range(501, 511)):
    plt.close('all')
    print(i_model_number)
    dir_save_model = f"{dir_models}/model_{i_model_number}"
    dir_model = dir_save_model
    dir_figures = dir_model + '/figures'
    os.makedirs(dir_figures, exist_ok=True)
    os.makedirs(dir_model + "/results/data", exist_ok=True)
    dir_nii_files = f"{dir_model}/state_maps_nii"
    os.makedirs(dir_nii_files, exist_ok=True)

    # get alpha values
    model = load(dir_model)
    data = Data(dir_training, picks="misc", reject_by_annotation="omit")
    alpha = model.get_alpha(data)
    pickle.dump(alpha, open(dir_model + "/results/data/alpha.pkl", "wb"))