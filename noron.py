# --- BƯỚC 1: NẠP CÁC THƯ VIỆN CẦN THIẾT [cite: 21-32] ---
import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.neural_network import MLPClassifier

# --- BƯỚC 2: TẢI VÀ KHÁM PHÁ DỮ LIỆU [cite: 40-47] ---
# Load the iris dataset
iris = datasets.load_iris()
X = iris.data
y = iris.target

print("Dữ liệu mẫu (5 dòng đầu):")
print(X[:5,:])
print("Nhãn mẫu (5 dòng đầu):")
print(y[:5])

# --- BƯỚC 3: PHÂN CHIA DỮ LIỆU TRAIN/TEST [cite: 70-74] ---
# Chia tập dữ liệu: 80% train, 20% test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=1)

print(f"Kích thước tập train: {X_train.shape}") # [cite: 76]
print(f"Kích thước tập test: {X_test.shape}")   # [cite: 78]

# --- BƯỚC 4: SỬ DỤNG NHÃN NGUYÊN [cite: 85-88] ---
# MLPClassifier có thể xử lý nhãn nguyên
train_labels = y_train
test_labels = y_test

print("Nhãn (5 dòng đầu):")
print(train_labels[:5]) # [cite: 91]

# --- BƯỚC 5: TẠO VÀ HUẤN LUYỆN MÔ HÌNH [cite: 102-109] ---
# Khởi tạo mô hình MLPClassifier với kiến trúc tương tự
network = MLPClassifier(hidden_layer_sizes=(32, 64, 128), activation='relu', solver='adam', max_iter=1000, random_state=1)

# Hiển thị tóm tắt mô hình
print("Mô hình MLPClassifier:")
print(f"Hidden layers: {network.hidden_layer_sizes}")
print(f"Activation: {network.activation}")
print(f"Solver: {network.solver}")

# Huấn luyện mô hình (Training) [cite: 144-146]
print("\nBắt đầu huấn luyện...")
network.fit(X_train, train_labels)

# --- BƯỚC 6: ĐÁNH GIÁ MÔ HÌNH [cite: 172, 186-192] ---
print("\nĐánh giá trên tập kiểm thử (Test set):")
test_acc = network.score(X_test, test_labels)

print('Test Accuracy: ', test_acc)