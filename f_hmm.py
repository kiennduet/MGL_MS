# import os
# from osl_dynamics.data import Data

# # test post meeting Mark 20240925

# # # (0) define directories
# # setup_file = "M3_010_002_setup.py"
# # with open(setup_file) as f:
# #     code = f.read()
# #     exec(code)

# print("\nHMM step\n")

# dir_training = r"/media/avitech/MyPassport/Kien/MEG_data/5_meg_training"
# dir_models = r"/media/avitech/MyPassport/Kien/MEG_data/7_models_full"

# for i in range(2201, 2202):   # Loop from 301 to 310  dir_save_model = f"/home/gnagels/Data/DPhilData/analyses/TDE-HMM_20240806a/model_{i}"
#     dir_save_model = f"{dir_models}/model_{i}"
#     os.makedirs(dir_save_model, exist_ok=True)
#     print(f"Running code with dir_save_model = {dir_save_model}")

#     # (2) load TDE prepared data for further processing
#     # data = Data(dir_training,
#     #             n_batches=10,  # Sử dụng 10 batch để giảm tải RAM
#     #             standardize=True  # Chuẩn hóa dữ liệu khi load từng batch
#     # )

#     data = Data(dir_training)
#     data.prepare(n_batches=10) 

#     # (3) define and run TDE HMM model
#     from osl_dynamics.models.hmm import Config
#     # Create a config object
#     config = Config(
#         n_states=6,
#         n_channels=120,
#         sequence_length=1000,
#         learn_means=False,
#         learn_covariances=True,
#         batch_size=16, #16
#         learning_rate=0.01,
#         n_epochs=20, #20
#     )

#     from osl_dynamics.models.hmm import Model

#     model = Model(config)
#     model.summary()
#     init_history = model.random_state_time_course_initialization(data, n_epochs=1, n_init=3)

#     history = model.fit(data)
#     model.save(dir_save_model)

import os
import numpy as np
from osl_dynamics.data import Data
from osl_dynamics.models.hmm import Config, Model

# (1) Định nghĩa các thư mục
dir_training = r"/media/avitech/MyPassport/Kien/MEG_data/5_meg_training"
dir_models = r"/media/avitech/MyPassport/Kien/MEG_data/7_models_full"

num_model = 120524
dir_save_model = f"{dir_models}/model_{num_model}"
os.makedirs(dir_save_model, exist_ok=True)
batch_models_dir = os.path.join(dir_models, "batch_models")
os.makedirs(batch_models_dir, exist_ok=True)

files = [os.path.join(dir_training, f) for f in os.listdir(dir_training) if f.endswith(".npy")]
if not files:
    raise ValueError(f"Không có tệp dữ liệu hợp lệ trong thư mục {dir_training}.")

num_splits = 5 #Seperate data into 5 parts
batches = [batch for batch in np.array_split(files, num_splits) if len(batch) > 0]

# (2) Cấu hình mô hình HMM
config = Config(
    n_states=6,
    n_channels=120,
    sequence_length=1000,
    learn_means=False,
    learn_covariances=True,
    batch_size=16,
    learning_rate=0.01,
    n_epochs=10,
)

# (3) Khởi tạo mô hình
model = Model(config)

# Huấn luyện theo từng batch
for i, batch in enumerate(batches):
    print(f"Đang huấn luyện trên batch {i+1}/{len(batches)}...")
    
    # Load dữ liệu của batch
    data = Data(batch)
    
    # Nếu đây là batch đầu tiên, thực hiện khởi tạo mô hình
    if i == 0:
        model.random_state_time_course_initialization(data, n_epochs=1, n_init=3)
    
    # Huấn luyện mô hình trên batch
    history = model.fit(data)

    # Lưu mô hình sau mỗi batch 
    batch_model_path = os.path.join(batch_models_dir, f"model_batch_{i+1}")
    model.save(batch_model_path)
    print(f"Đã lưu mô hình batch {i+1} tại {batch_model_path}")

# Lưu mô hình cuối cùng
model.save(dir_save_model)
print(f"Đã lưu mô hình cuối cùng tại {dir_save_model}")
