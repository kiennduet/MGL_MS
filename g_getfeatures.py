import os
from osl_dynamics.data import Data
from osl_dynamics.models import load
from osl_dynamics.inference import modes
import pickle

dir_models = "/media/avitech/MyPassport/Kien/MEG_data/7_models_full"
dir_training = r"/media/avitech/MyPassport/Kien/MEG_data/5_meg_training"

for i_model_number in range(2201, 2202):  

    print(i_model_number)
    dir_model = f"{dir_models}/model_{i_model_number}" 
    os.makedirs(dir_model + "/results/data", exist_ok=True)

    # get alpha values
    model = load(dir_model)
    data = Data(dir_training, picks="misc", reject_by_annotation="omit")
    alpha = model.get_alpha(data)
    pickle.dump(alpha, open(dir_model + "/results/data/alpha.pkl", "wb"))



# # get alpha values
# model_Kien = load("/home/data/open_source/directory_for_Kien/6_models_146/model_2201")
# data = Data(dir_training, picks="misc", reject_by_annotation="omit")
# alpha = model_Kien.get_alpha(data)

# # Calculate state time courses stc
# stc = modes.argmax_time_courses(alpha)
# # Calculate fractional occupancy (FO) across subjects
# fo = modes.fractional_occupancies(stc)
# # Calculate mean lifetimes (in seconds)
# mlt = modes.mean_lifetimes(stc, sampling_frequency=250)
# mlt *= 1000  # Convert to ms
# # Calculate mean intervals (in seconds)
# mintv = modes.mean_intervals(stc, sampling_frequency=250)

# # Bundle features into a dictionary
# features = {
#     "state_time_courses": stc,
#     "fractional_occupancies": fo,
#     "mean_lifetimes": mlt,
#     "mean_intervals": mintv
# }

# # Save to a pickle file
# with open("features_Kien_146.pkl", "wb") as f:
#     pickle.dump(features, f)

   