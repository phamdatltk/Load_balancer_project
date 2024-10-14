# Đường dẫn tới file log.txt
file_path = 'log.txt'

# Đọc nội dung từ file và chỉ giữ lại các dòng có chứa 'Weight'
with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Lọc các dòng chứa từ 'Weight'
filtered_lines = [line for line in lines if 'Weight' in line]

# Ghi các dòng đã lọc vào file mới hoặc file cũ
with open('filtered_log.txt', 'w', encoding='utf-8') as file:
    file.writelines(filtered_lines)

print("Đã lọc xong, các dòng có 'Weight' đã được ghi vào 'filtered_log.txt'")

# Lọc các dòng chứa từ 'Weight 0'
filtered_lines = [line for line in lines if 'Weight 0' in line]

# Ghi các dòng đã lọc vào file mới hoặc file cũ
with open('filtered_log_0.txt', 'w', encoding='utf-8') as file:
    file.writelines(filtered_lines)

print("Đã lọc xong, các dòng có 'Weight' đã được ghi vào 'filtered_log_0.txt'")

# Lọc các dòng chứa từ 'Weight 1'
filtered_lines = [line for line in lines if 'Weight 1' in line]

# Ghi các dòng đã lọc vào file mới hoặc file cũ
with open('filtered_log_1.txt', 'w', encoding='utf-8') as file:
    file.writelines(filtered_lines)

print("Đã lọc xong, các dòng có 'Weight' đã được ghi vào 'filtered_log_1.txt'")


# Lọc các dòng chứa từ 'Weight 2'
filtered_lines = [line for line in lines if 'Weight 2' in line]

# Ghi các dòng đã lọc vào file mới hoặc file cũ
with open('filtered_log_2.txt', 'w', encoding='utf-8') as file:
    file.writelines(filtered_lines)

print("Đã lọc xong, các dòng có 'Weight' đã được ghi vào 'filtered_log_2.txt'")