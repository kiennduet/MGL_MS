import os
import platform
from osl_dynamics.data import Data
from osl_dynamics.models import load
import pickle
import numpy as np
from itertools import chain
import matplotlib.pyplot as plt

# from M300_265_004_cluster_permutation import code_group_num

# post meeting with Mark 20240925

# # (0) define directories
# # setup_file = "M300_010_005_setup_20240925a.py"
# setup_file = "M3_010_002_setup.py"
# with open(setup_file) as f:
#     code = f.read()
#     exec(code)

print("\nPlotting graphs to analyze the results \n")

# dir_models = r"/media/avitech/MyPassport/Kien/MEG_data/6_models"
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

    original_data = data.time_series(prepared=False)
    prepared_data = data.time_series()
    data_realigned = model.get_training_time_series(data, prepared=False)
    data_before_pca = Data(dir_before_pca)
    data_before_pca_trimmed = data_before_pca.trim_time_series(n_embeddings=15, sequence_length=1000)

    from osl_dynamics.analysis import spectral
    f, psd, coh = spectral.multitaper_spectra(
        data=data_before_pca_trimmed,
        alpha=alpha,
        sampling_frequency=250,
        time_half_bandwidth=4,
        n_tapers=7,
        frequency_range=[0.1, 45],
        n_jobs=16,
    )


    np.save(dir_model + "/results/data/f.npy", f)
    np.save(dir_model + "/results/data/psd.npy", psd)
    np.save(dir_model + "/results/data/coh.npy", coh)
    #

    # Plot the state probability time course for the first subject (8 seconds)
    from osl_dynamics.utils import plotting
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    plotting.plot_alpha(alpha[0], n_samples=2000)
    plot_file_path = dir_figures + '/timecourse_example_001.png'
    plt.savefig(plot_file_path)
    plt.close(fig)

    # Hard classify the state probabilities
    from osl_dynamics.inference import modes
    stc = modes.argmax_time_courses(alpha)
    # Plot the state time course for the first subject (8 seconds)
    fig, ax = plt.subplots()
    plotting.plot_alpha(stc[0], n_samples=2000)
    plt.title("State Time Course for First Subject")
    plt.savefig(f"{dir_figures}/state_time_course_first_subject.png")
    plt.close(fig)

    # Plot the distribution of fractional occupancy (FO) across subjects
    fo = modes.fractional_occupancies(stc)
    import numpy as np
    print(np.mean(fo, axis=0))
    fig, ax = plt.subplots()
    plotting.plot_violin(fo.T, x_label="State", y_label="FO")
    plt.title("Fractional occupancy across subjects")
    plt.savefig(f"{dir_figures}/frac_occ.png")
    plt.close(fig)

    # Calculate mean lifetimes (in seconds)
    mlt = modes.mean_lifetimes(stc, sampling_frequency=250)
    mlt *= 1000    # Convert to ms
    fig, ax = plt.subplots()
    plotting.plot_violin(mlt.T, x_label="State", y_label="Mean Lifetime (ms)")
    plt.title("Mean lifetimes across subjects")
    plt.savefig(f"{dir_figures}/lifetimes.png")
    plt.close(fig)

    # Calculate mean intervals (in seconds)
    mintv = modes.mean_intervals(stc, sampling_frequency=250)
    fig, ax = plt.subplots()
    plotting.plot_violin(mintv.T, x_label="State", y_label="Mean Interval (s)")
    plt.title("Mean intervals across subjects")
    plt.savefig(f"{dir_figures}/intervals.png")
    plt.close(fig)


# #____________________________________________________________________________________
# ############ compare groups

#     from osl_dynamics.analysis import statistics
#     group_diff, pvalues = statistics.group_diff_max_stat_perm(
#         fo,
#         code_group_num,
#         n_perm=10000,
#         n_jobs=16,
#     )
#     print(pvalues)




#     import numpy as np
#     from scipy import stats
#     import pandas as pd

#     data = mlt

#     # Index vector with values 1 for controls and 2 for patients
#     index_vector = code_group_num

#     # Grouping data into controls (1) and patients (2)
#     controls_data = data[index_vector == 1]
#     patients_data = data[index_vector == 2]

#     # Preparing to store results for each column
#     results = []

#     # Loop over each column to compute mean, std, and p-value for controls and patients
#     for col in range(data.shape[1]):
#         control_mean = np.mean(controls_data[:, col])
#         control_std = np.std(controls_data[:, col])

#         patient_mean = np.mean(patients_data[:, col])
#         patient_std = np.std(patients_data[:, col])

#         # Perform two-sample t-test
#         t_stat, p_value = stats.ttest_ind(controls_data[:, col], patients_data[:, col])

#         # Store the results
#         results.append({
#             'column': col,
#             'control_mean': control_mean,
#             'control_std': control_std,
#             'patient_mean': patient_mean,
#             'patient_std': patient_std,
#             'p_value': p_value
#         })

#     # Convert the results into a DataFrame for easy viewing
#     results_df = pd.DataFrame(results)

#     # Display the DataFrame
#     print(results_df)

#     #####################3


#     #
#     # ###################################
#     # # power analysis
#     # ###################################
#     import matplotlib.pyplot as plt
#     import numpy as np
#     f = np.load(dir_model + "/results/data/f.npy")
#     psd = np.load(dir_model + "/results/data/psd.npy")
#     from osl_dynamics.utils import plotting

#     # Average over subjects and channels
#     psd_mean = np.mean(psd, axis=(0, 2))
#     n_states = psd_mean.shape[0]
#     fig, ax = plt.subplots()
#     plotting.plot_line(
#         [f] * n_states,
#         psd_mean,
#         labels=[f"State {i}" for i in range(1, n_states + 1)],
#         x_label="Frequency (Hz)",
#         y_label="PSD (a.u.)",
#         x_range=[f[0], f[-1]],
#     )
#     plt.savefig(f"{dir_figures}/power.png")
#     plt.close(fig)
#     print(f"saved {dir_figures}/power.png for {i_model_number}")

#     # # create mean power maps for all states
#     from osl_dynamics.analysis import power
#     # Integrate the power spectra
#     p = power.variance_from_spectra(f, psd, frequency_range=[0.1, 45])
#     mean_p = np.mean(p, axis=0)
#     # Calculate the mean across the parcels (axis=1)
#     state_means = np.mean(mean_p, axis=1, keepdims=True)
#     # Subtract the mean from each corresponding state's parcel values
#     adjusted_mean_p = mean_p - state_means
#     print(f"calculated spectra for {i_model_number}")

#     fig, ax = power.save(
#     adjusted_mean_p,
#     mask_file="/home/gnagels/Data/DPhilData/parcellations/atlas/MNI152_T1_8mm_brain.nii.gz",
#     parcellation_file="/home/gnagels/Data/DPhilData/parcellations/Glasser/Glasser52_binary_space-MNI152NLin6_res-8x8x8.nii.gz",
#     subtract_mean=True,
#     filename= None,
#     plot_kwargs={'symmetric_cbar': True},
#     )
#     # save all figures
#     import matplotlib.pyplot as plt
#     for j, f in enumerate(fig):
#         f.savefig(f'{dir_figures}/state_a_{j + 1}.png')
#     for f in fig:
#         plt.close(f)
#     print(f"saved standard figures for {i_model_number}")

#     file_nii = (f"{dir_nii_files}/maps_{i_model_number}.nii.gz")
#     print(file_nii)
#     power.save(
#         adjusted_mean_p,
#         mask_file="/home/gnagels/Data/DPhilData/parcellations/atlas/MNI152_T1_8mm_brain.nii.gz",
#         parcellation_file="/home/gnagels/Data/DPhilData/parcellations/Glasser/Glasser52_binary_space-MNI152NLin6_res-8x8x8.nii.gz",
#         subtract_mean=True,
#         filename=file_nii,
#         plot_kwargs={'symmetric_cbar': True},
#     )
#     print(f"saved nii figures for {i_model_number}")
#     print(file_nii)

#     if len(fig)==6:
#         # combined plot
#         import matplotlib.pyplot as plt
#         from PIL import Image
#         # List of image filenames
#         filenames = [f'{dir_figures}/state_a_{i}.png' for i in range(1, 7)]
#         # Create a figure with 2 rows and 3 columns
#         fig, axes = plt.subplots(2, 3, figsize=(12, 8))
#         # Flatten the axes array for easy iteration
#         axes = axes.flatten()
#         # Load and display each image with a title
#         for i, ax in enumerate(axes):
#             # Load the image
#             img = Image.open(filenames[i])
#             # Display the image
#             ax.imshow(img)
#             # Add a title
#             ax.set_title(f'State {i + 1}')
#             # Remove the axis ticks
#             ax.axis('off')
#         # Adjust layout
#         plt.tight_layout()
#         # Save the combined figure if needed
#         plt.savefig(dir_figures + '/combined_figure.png')




#     file_nii = (f"{dir_figures}/maps_{i_model_number}.nii.gz")
#     print(file_nii)
#     power.save(
#         adjusted_mean_p,
#         mask_file="/home/gnagels/Data/DPhilData/parcellations/atlas/MNI152_T1_8mm_brain.nii.gz",
#         parcellation_file="/home/gnagels/Data/DPhilData/parcellations/Glasser/Glasser52_binary_space-MNI152NLin6_res-8x8x8.nii.gz",
#         subtract_mean=True,
#         filename=file_nii,
#         plot_kwargs={'symmetric_cbar': True},
#     )
#     print(f"saved nii figures for {i_model_number}")
#     print(file_nii)