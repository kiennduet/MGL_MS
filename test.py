import os
import numpy as np
from osl_dynamics.data import Data
from osl_dynamics.models import load
from osl_dynamics.inference import modes
import pandas as pd

# (0) Định nghĩa các thư mục
dir_models = r"/media/avitech/MyPassport/Kien/MEG_data/6_models"
dir_training = r"/media/avitech/MyPassport/Kien/MEG_data/5_meg_training"
dir_output = r"/media/avitech/MyPassport/Kien/MEG_data/features"  # Thư mục lưu đặc trưng

# Đảm bảo thư mục lưu đặc trưng tồn tại
os.makedirs(dir_output, exist_ok=True)

# Xác định số mô hình cần phân tích
i_model_number = 2201  # Số mô hình bạn muốn xử lý
dir_model = f"{dir_models}/model_{i_model_number}"

# Load model và dữ liệu
model = load(dir_model)
data = Data(dir_training, picks="misc", reject_by_annotation="omit")

# Lấy giá trị alpha (state probability time courses)
alpha = model.get_alpha(data)

# (1) Tính `stc` (State Time Course)
stc = modes.argmax_time_courses(alpha)

# (2) Tính `fo` (Fractional Occupancies)
fo = modes.fractional_occupancies(stc)

# (3) Tính `mlt` (Mean Lifetimes)
sampling_frequency = 250  # Tần số lấy mẫu (Hz)
mlt = modes.mean_lifetimes(stc, sampling_frequency=sampling_frequency)

# In thông tin cơ bản
print(f"Đã tính toán xong các đặc trưng:")
print(f"STC Shape: {stc.shape}")
print(f"FO Shape: {fo.shape}")
print(f"MLT Shape: {mlt.shape}")

# Chuyển các đặc trưng sang DataFrame và lưu dưới dạng CSV
stc_df = pd.DataFrame(stc)
fo_df = pd.DataFrame(fo, columns=[f"State_{i}" for i in range(fo.shape[1])])
mlt_df = pd.DataFrame(mlt, columns=[f"State_{i}" for i in range(mlt.shape[1])])

# Định nghĩa đường dẫn lưu file
stc_csv_path = os.path.join(dir_output, f"stc_model_{i_model_number}.csv")
fo_csv_path = os.path.join(dir_output, f"fo_model_{i_model_number}.csv")
mlt_csv_path = os.path.join(dir_output, f"mlt_model_{i_model_number}.csv")

# Lưu vào tệp CSV
stc_df.to_csv(stc_csv_path, index=False)
fo_df.to_csv(fo_csv_path, index=False)
mlt_df.to_csv(mlt_csv_path, index=False)

print("\nĐã lưu các đặc trưng vào CSV:")
print(f"STC được lưu tại: {stc_csv_path}")
print(f"FO được lưu tại: {fo_csv_path}")
print(f"MLT được lưu tại: {mlt_csv_path}")

