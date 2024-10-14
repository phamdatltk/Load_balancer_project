import matplotlib.pyplot as plt
import pandas as pd

# Đường dẫn tới file filtered_log_0.txt
file_path = 'filtered_log_0.txt'

# Đọc file và lưu vào DataFrame
data = []
with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        # Tách dòng thành timestamp và weight
        parts = line.split(' - Weight 0: ')
        if len(parts) == 2:
            timestamp = parts[0].strip()  # Lấy thời gian
            weight = int(parts[1].strip())  # Lấy trọng số
            data.append([timestamp, weight])

# Tạo DataFrame từ dữ liệu
df = pd.DataFrame(data, columns=['Timestamp', 'Weight'])

# Chuyển cột 'Timestamp' thành định dạng thời gian
df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%Y-%m-%d %H:%M:%S')

# Vẽ biểu đồ
plt.figure(figsize=(10, 6))
plt.plot(df['Timestamp'], df['Weight'], marker='o', linestyle='-', color='b')
plt.xlabel('Time')
plt.ylabel('Weight 0')
plt.title('Weight 0 over Time')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()

# Lưu biểu đồ thành file ảnh
plt.savefig('chart_0.png')

print("Biểu đồ đã được lưu thành công với tên 'chart_0.png'.")


# Đường dẫn tới file filtered_log_1.txt
file_path = 'filtered_log_1.txt'

# Đọc file và lưu vào DataFrame
data = []
with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        # Tách dòng thành timestamp và weight
        parts = line.split(' - Weight 1: ')
        if len(parts) == 2:
            timestamp = parts[0].strip()  # Lấy thời gian
            weight = int(parts[1].strip())  # Lấy trọng số
            data.append([timestamp, weight])

# Tạo DataFrame từ dữ liệu
df = pd.DataFrame(data, columns=['Timestamp', 'Weight'])

# Chuyển cột 'Timestamp' thành định dạng thời gian
df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%Y-%m-%d %H:%M:%S')

# Vẽ biểu đồ
plt.figure(figsize=(10, 6))
plt.plot(df['Timestamp'], df['Weight'], marker='o', linestyle='-', color='b')
plt.xlabel('Time')
plt.ylabel('Weight 1')
plt.title('Weight 1 over Time')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()

# Lưu biểu đồ thành file ảnh
plt.savefig('chart_1.png')

print("Biểu đồ đã được lưu thành công với tên 'chart_1.png'.")


# Đường dẫn tới file filtered_log_2.txt
file_path = 'filtered_log_2.txt'

# Đọc file và lưu vào DataFrame
data = []
with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        # Tách dòng thành timestamp và weight
        parts = line.split(' - Weight 2: ')
        if len(parts) == 2:
            timestamp = parts[0].strip()  # Lấy thời gian
            weight = int(parts[1].strip())  # Lấy trọng số
            data.append([timestamp, weight])

# Tạo DataFrame từ dữ liệu
df = pd.DataFrame(data, columns=['Timestamp', 'Weight'])

# Chuyển cột 'Timestamp' thành định dạng thời gian
df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%Y-%m-%d %H:%M:%S')

# Vẽ biểu đồ
plt.figure(figsize=(10, 6))
plt.plot(df['Timestamp'], df['Weight'], marker='o', linestyle='-', color='b')
plt.xlabel('Time')
plt.ylabel('Weight 2')
plt.title('Weight 2 over Time')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()

# Lưu biểu đồ thành file ảnh
plt.savefig('chart_2.png')

print("Biểu đồ đã được lưu thành công với tên 'chart_2.png'.")