#%% Import packages
print("Importing packages")
from osl_dynamics.analysis import power, connectivity
from osl_dynamics.utils import plotting
import os
import pickle
import numpy as np
from osl_dynamics.analysis import spectral
from osl_dynamics.data import Data


# post meeting with Mark 20240925

# (0) define directories
# setup_file = "M300_010_005_setup_20240925a.py"
# setup_file = "M3_010_002_setup.py"
# with open(setup_file) as f:
#     code = f.read()
#     exec(code)


#%% Directories
# dir_models = '/home/gnagels/Data/DPhilData/analyses/TDE-HMM_20240806a/models'

dir_models = r"/media/avitech/MyPassport/Kien/MEG_data/6_models"
dir_training = r"/media/avitech/MyPassport/Kien/MEG_data/5_meg_training"
dir_before_pca = r"/media/avitech/MyPassport/Kien/MEG_data/4_meg_embedded"


dir_model = dir_models + '/model_2201'
dir_figures = dir_model + "/results/figures"
os.makedirs(dir_figures, exist_ok=True)
print(dir_figures)

dir_inf_params = dir_model + '/results/data'
dir_spectra = dir_model + '/spectra'
os.makedirs(dir_spectra, exist_ok=True)
networks_dir = dir_model + "/networks"
os.makedirs(networks_dir, exist_ok=True)
mask_file = "MNI152_T1_8mm_brain.nii.gz"

# parcellation_file = "fmri_d100_parcellation_with_PCC_reduced_2mm_ss5mm_ds8mm.nii.gz"


data = Data(dir_before_pca, n_jobs=16)
original_data = data.time_series(prepared=False)
prepared_data = data.time_series()
data_trimmed = data.trim_time_series(n_embeddings=15, sequence_length=1000)
from osl_dynamics.models import load
model = load(dir_model)

# State probabilities
alpha = pickle.load(open(f"{dir_inf_params}/alpha.pkl", "rb"))

# # Sanity check: the first axis should have the same number of time points
# for x, a in zip(data_trimmed, alpha):
#   print(x.shape, a.shape)

#%% Calculate multitaper
f, psd, coh, w = spectral.multitaper_spectra(
    data=data_trimmed,
    alpha=alpha,
    sampling_frequency=250,
    time_half_bandwidth=4,
    n_tapers=7,
    frequency_range=[1, 45],
    return_weights=True,  # weighting for each subject when we average the spectra
    n_jobs=16,  # parallelisation, if you get a RuntimeError set to 1
)

np.save(f"{dir_spectra}/f.npy", f)
np.save(f"{dir_spectra}/psd.npy", psd)
np.save(f"{dir_spectra}/coh.npy", coh)
np.save(f"{dir_spectra}/w.npy", w)

# #%% Load spectra
# f = np.load(f"{dir_spectra}/f.npy")  # (n_freq,)
# psd = np.load(f"{dir_spectra}/psd.npy")  # (n_subjects, n_states, n_parcels, n_freq)
# coh = np.load(f"{dir_spectra}/coh.npy")  # (n_subjects, n_states, n_parcels, n_parcels, n_freq)
# w = np.load(f"{dir_spectra}/w.npy")  # (n_subjects,)
# wb_comp = np.load(f"{dir_spectra}/nnmf_2.npy")  # (n_components, n_freq)

from osl_dynamics.utils import plotting
psd_mean = np.mean(psd, axis=(0,2))
print(psd_mean.shape)
n_states = psd_mean.shape[0]
plotting.plot_line(
    [f] * n_states,
    psd_mean,
    labels=[f"State {i}" for i in range(1, n_states + 1)],
    x_label="Frequency (Hz)",
    y_label="PSD (a.u.)",
    x_range=[f[0], f[-1]],
    filename=dir_figures +'/state_power_spectra.png',
)
print("\nState Power Spectra saved\n")



from osl_dynamics.analysis import power
p = power.variance_from_spectra(f, psd)
p_mean = np.mean(p, axis=0)

power.save(
        p_mean,
        filename=dir_figures + '/state_power_maps.png',
        combined=True,
        mask_file="/media/avitech/MyPassport/Kien/MEG_data/0_sample_file/MNI152_T1_1mm_brain.nii.gz",
        parcellation_file="/media/avitech/MyPassport/Kien/MEG_data/0_sample_file/Glasser52_binary_space-MNI152NLin6_res-8x8x8_8mm.nii.gz",
        plot_kwargs={"symmetric_cbar": True},
        subtract_mean=True,
    )
print("\nState Power Maps saved\n")

    

# mean_values = np.mean(p_mean, axis=1, keepdims=True)
# result = p_mean - mean_values

# Takes a few seconds for the power maps to appear
# fig, ax = (
# power.save(
#     p_mean,
#     filename=dir_figures +'/state_power_maps.png',
#     combined=True,
#     mask_file="MNI152_T1_8mm_brain.nii.gz",
#     parcellation_file="/home/gnagels/Data/DPhilData/parcellations/Glasser/Glasser52_binary_space-MNI152NLin6_res-8x8x8.nii.gz",
# )




#
#
#
##################################3
#%% Plot power spectra
# Calculate the group average power spectrum for each state
# gpsd = np.average(psd, axis=0, weights=w)
# # Plot
# for i in range(gpsd.shape[0]):
#     p = np.mean(gpsd[i], axis=0)  # mean over parcels
#     e = np.std(gpsd[i]) / np.sqrt(gpsd[i].shape[0])  # standard error on the mean
#     plotting.plot_line(
#         [f],
#         [p],
#         errors=[[p - e], [p + e]],
#         x_label="Frequency (Hz)",
#         y_label="PSD (a.u.)",
#         x_range=[f[0], f[-1]],
#         filename=f"{networks_dir}/psd_{i:02d}.png",
#     )

# #%% Plot power maps
# # Calculate the group average power spectrum for each state
# gpsd = np.average(psd, axis=0, weights=w)
# # Calculate the power map by integrating the power spectra over a frequency range
# p = power.variance_from_spectra(f, gpsd, wb_comp)
# # Plot
# power.save(
#     p,
#     mask_file=mask_file,
#     parcellation_file=parcellation_file,
#     subtract_mean=True,
#     component=0,
#     plot_kwargs={"symmetric_cbar": True},
#     filename=f"{networks_dir}/pow_.png",
# )
#
# #%% Plot coherence networks
#
# # Calculate the group average
# gcoh = np.average(coh, axis=0, weights=w)
# # Calculate the coherence network by averaging over a frequency range
# c = connectivity.mean_coherence_from_spectra(f, gcoh, wb_comp)
# # Threshold the top 2% of connections
# c = connectivity.threshold(c, percentile=98, subtract_mean=True)
# # Plot
# connectivity.save(
#     c,
#     parcellation_file=parcellation_file,
#     component=0,
#     filename=f"{networks_dir}/coh_.png",
# )