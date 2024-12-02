import os
from osl_dynamics.data import Data

# test post meeting Mark 20240925

# # (0) define directories
# setup_file = "M3_010_002_setup.py"
# with open(setup_file) as f:
#     code = f.read()
#     exec(code)

print("\nHMM step\n")

dir_training = r"/media/avitech/MyPassport/Kien/MEG_data/5_meg_training"
dir_models = r"/media/avitech/MyPassport/Kien/MEG_data/7_models_full"

for i in range(2201, 2202):   # Loop from 301 to 310  dir_save_model = f"/home/gnagels/Data/DPhilData/analyses/TDE-HMM_20240806a/model_{i}"
    dir_save_model = f"{dir_models}/model_{i}"
    os.makedirs(dir_save_model, exist_ok=True)
    print(f"Running code with dir_save_model = {dir_save_model}")

    # (2) load TDE prepared data for further processing
    data = Data(dir_training)

    # (3) define and run TDE HMM model
    from osl_dynamics.models.hmm import Config
    # Create a config object
    config = Config(
        n_states=6,
        n_channels=120,
        sequence_length=1000,
        learn_means=False,
        learn_covariances=True,
        batch_size=16,
        learning_rate=0.01,
        n_epochs=20,
    )
    from osl_dynamics.models.hmm import Model

    model = Model(config)
    model.summary()
    init_history = model.random_state_time_course_initialization(data, n_epochs=1, n_init=3)

    history = model.fit(data)
    model.save(dir_save_model)
