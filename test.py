import os
from osl_dynamics.data import Data
from osl_dynamics.models.hmm import Config, Model

# (1) Định nghĩa các thư mục
dir_training = r"/media/avitech/MyPassport/Kien/MEG_data/5_meg_training"
dir_models = r"/media/avitech/MyPassport/Kien/MEG_data/7_models_full"
os.makedirs(dir_models, exist_ok=True)

# Liệt kê các tệp dữ liệu
files = [os.path.join(dir_training, f) for f in os.listdir(dir_training)]

# Chia nhỏ các tệp dữ liệu thành batch (ví dụ: 10 tệp mỗi batch)
batch_size = 130
batches = [files[i:i + batch_size] for i in range(0, len(files), batch_size)]

# (2) Cấu hình mô hình HMM
config = Config(
    n_states=6,
    n_channels=120,
    sequence_length=1000,
    learn_means=False,
    learn_covariances=True,
    batch_size=16,
    learning_rate=0.01,
    n_epochs=15,  # Huấn luyện 5 epoch mỗi batch
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
    model.save(os.path.join(dir_models, f"model_batch_{i+1}"))

# Lưu mô hình cuối cùng
final_model_path = os.path.join(dir_models, "final_model")
model.save(final_model_path)
print(f"Đã lưu mô hình cuối cùng tại {final_model_path}")
