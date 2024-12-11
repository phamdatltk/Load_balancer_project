# import matplotlib.pyplot as plt
# import numpy as np

# # Dữ liệu cho các giá trị RPS và Average Response Time
# rps = [100, 125, 150, 175, 200]
# round_robin = [2214, 3195, 5727, 7009, 9438]  # Giá trị cuối không có trong đề bài
# custom_algorithm = [83, 712, 3704,5338, 13762]  # Giá trị cuối không có trong đề bài

# # Vị trí của các cột trên trục x
# x = np.arange(len(rps))  # Tạo các vị trí trên trục hoành

# # Độ rộng của các cột
# width = 0.35

# # Tạo biểu đồ
# fig, ax = plt.subplots(figsize=(10, 6))

# # Vẽ các cột cho Round Robin
# bars1 = ax.bar(x - width/2, round_robin, width, label='Round Robin', color='b')

# # Vẽ các cột cho Custom Algorithm
# bars2 = ax.bar(x + width/2, custom_algorithm, width, label='Custom Algorithm', color='g')

# # Thêm các chi tiết
# ax.set_xlabel('RPS (Requests Per Second)')
# ax.set_ylabel('Average Response Time (ms)')
# ax.set_title('So sánh Average Response Time giữa Round Robin và Custom Algorithm')
# ax.set_xticks(x)
# ax.set_xticklabels(rps)
# ax.legend()

# # Hiển thị giá trị trên mỗi cột
# def autolabel(bars):
#     for bar in bars:
#         height = bar.get_height()
#         if height is not None:  # Chỉ ghi nhãn nếu không phải None
#             ax.annotate(f'{int(height)}',
#                         xy=(bar.get_x() + bar.get_width() / 2, height),
#                         xytext=(0, 3),  # Khoảng cách từ đỉnh cột
#                         textcoords="offset points",
#                         ha='center', va='bottom')

# # Thêm giá trị vào các cột
# autolabel(bars1)
# autolabel(bars2)

# # Hiển thị biểu đồ
# plt.tight_layout()
# plt.savefig('AVGCompare.png')



# # Dữ liệu cho các giá trị RPS và Error rate
# rps = [100, 125, 150, 175, 200]
# round_robin = [0, 0.1, 1, 3, 23]  # Giá trị cuối không có trong đề bài
# custom_algorithm = [0, 0, 0, 0, 0]  # Giá trị cuối không có trong đề bài

# # Vị trí của các cột trên trục x
# x = np.arange(len(rps))  # Tạo các vị trí trên trục hoành

# # Độ rộng của các cột
# width = 0.35

# # Tạo biểu đồ
# fig, ax = plt.subplots(figsize=(10, 6))

# # Vẽ các cột cho Round Robin
# bars1 = ax.bar(x - width/2, round_robin, width, label='Round Robin', color='b')

# # Vẽ các cột cho Custom Algorithm
# bars2 = ax.bar(x + width/2, custom_algorithm, width, label='Custom Algorithm', color='g')

# # Thêm các chi tiết
# ax.set_xlabel('RPS (Requests Per Second)')
# ax.set_ylabel('Error Rate (%)')
# ax.set_title('So sánh Error Rate giữa Round Robin và Custom Algorithm')
# ax.set_xticks(x)
# ax.set_xticklabels(rps)
# ax.legend()

# # Hiển thị giá trị trên mỗi cột
# def autolabel(bars):
#     for bar in bars:
#         height = bar.get_height()
#         if height is not None:  # Chỉ ghi nhãn nếu không phải None
#             ax.annotate(f'{int(height)}',
#                         xy=(bar.get_x() + bar.get_width() / 2, height),
#                         xytext=(0, 3),  # Khoảng cách từ đỉnh cột
#                         textcoords="offset points",
#                         ha='center', va='bottom')

# # Thêm giá trị vào các cột
# autolabel(bars1)
# autolabel(bars2)

# # Hiển thị biểu đồ
# plt.tight_layout()
# plt.savefig('ERCompare.png')






# # Dữ liệu cho các giá trị RPS và %CPU sử dụng của mỗi pod
# rps = [100, 125, 150, 175, 200]
# pod1_cpu = [99, 99, 99, 99, 99]  # %CPU của pod 1
# pod2_cpu = [61, 85, 98, 99, 99]  # %CPU của pod 2
# pod3_cpu = [33, 44, 51, 75, 88]  # %CPU của pod 3

# # Vị trí của các cột trên trục x
# x = np.arange(len(rps))  # Tạo các vị trí cho trục hoành

# # Độ rộng của mỗi cột
# width = 0.25

# # Tạo biểu đồ
# fig, ax = plt.subplots(figsize=(10, 6))

# # Vẽ các cột cho từng pod
# bars1 = ax.bar(x - width, pod1_cpu, width, label='Pod 1', color='b')
# bars2 = ax.bar(x, pod2_cpu, width, label='Pod 2', color='g')
# bars3 = ax.bar(x + width, pod3_cpu, width, label='Pod 3', color='r')

# # Thêm các chi tiết
# ax.set_xlabel('RPS (Requests Per Second)')
# ax.set_ylabel('%CPU Usage')
# ax.set_title('%CPU Usage của các Pod theo RPS (Round Robin)')
# ax.set_xticks(x)
# ax.set_xticklabels(rps)
# ax.legend()

# # Hiển thị giá trị trên mỗi cột
# def autolabel(bars):
#     for bar in bars:
#         height = bar.get_height()
#         ax.annotate(f'{int(height)}%',
#                     xy=(bar.get_x() + bar.get_width() / 2, height),
#                     xytext=(0, 3),  # Khoảng cách từ đỉnh cột
#                     textcoords="offset points",
#                     ha='center', va='bottom')

# # Gọi hàm để hiển thị giá trị
# autolabel(bars1)
# autolabel(bars2)
# autolabel(bars3)

# # Hiển thị biểu đồ
# plt.tight_layout()
# plt.savefig('AvgCpuRR.png')



# import matplotlib.pyplot as plt
# import numpy as np

# # Dữ liệu cho các giá trị RPS và %CPU sử dụng của mỗi pod
# rps = [100, 125, 150, 175, 200]
# pod1_cpu = [56, 56, 76, 92, 95]  # %CPU của pod 1
# pod2_cpu = [50, 62, 68, 80, 90]  # %CPU của pod 2
# pod3_cpu = [51, 70, 62, 77, 88]  # %CPU của pod 3

# # Vị trí của các cột trên trục x
# x = np.arange(len(rps))  # Tạo các vị trí cho trục hoành

# # Độ rộng của mỗi cột
# width = 0.25

# # Tạo biểu đồ
# fig, ax = plt.subplots(figsize=(10, 6))

# # Vẽ các cột cho từng pod
# bars1 = ax.bar(x - width, pod1_cpu, width, label='Pod 1', color='b')
# bars2 = ax.bar(x, pod2_cpu, width, label='Pod 2', color='g')
# bars3 = ax.bar(x + width, pod3_cpu, width, label='Pod 3', color='r')

# # Thêm các chi tiết
# ax.set_xlabel('RPS (Requests Per Second)')
# ax.set_ylabel('%CPU Usage')
# ax.set_title('%CPU Usage của các Pod theo RPS (Custom algorithm)')
# ax.set_xticks(x)
# ax.set_xticklabels(rps)
# ax.legend()

# # Hiển thị giá trị trên mỗi cột
# def autolabel(bars):
#     for bar in bars:
#         height = bar.get_height()
#         ax.annotate(f'{int(height)}%',
#                     xy=(bar.get_x() + bar.get_width() / 2, height),
#                     xytext=(0, 3),  # Khoảng cách từ đỉnh cột
#                     textcoords="offset points",
#                     ha='center', va='bottom')

# # Gọi hàm để hiển thị giá trị
# autolabel(bars1)
# autolabel(bars2)
# autolabel(bars3)

# # Hiển thị biểu đồ
# plt.tight_layout()
# plt.savefig('AvgCpuCA.png')


import matplotlib.pyplot as plt

# Dữ liệu
algorithms = ['RR', 'CA']
average_times = [6778, 142]

# Vẽ đồ thị hình cột
plt.figure(figsize=(8, 6))
plt.bar(algorithms, average_times, color=['blue', 'orange'])

# Thêm tiêu đề và nhãn trục
plt.title('Average Time Comparison Between RR and CA')
plt.xlabel('Algorithm')
plt.ylabel('Average Time (ms)')

# Hiển thị giá trị trên đỉnh cột
for i, v in enumerate(average_times):
    plt.text(i, v + 50, str(v), ha='center', fontweight='bold')

# Lưu biểu đồ thành file ảnh
plt.savefig("average_time_comparison.png", format="png", dpi=300)
plt.show()


import matplotlib.pyplot as plt
import numpy as np

# Dữ liệu
algorithms = ['RR', 'CA']
cpu1 = [99.8, 54]
cpu2 = [93.1, 47]
cpu3 = [76.9, 45]

# Thiết lập vị trí của các cột trên trục hoành
x = np.arange(len(algorithms))
width = 0.25  # Độ rộng của mỗi cột

# Vẽ biểu đồ cột
plt.figure(figsize=(10, 6))
plt.bar(x - width, cpu1, width, label='%CPU1 - AVG', color='blue')
plt.bar(x, cpu2, width, label='%CPU2 - AVG', color='orange')
plt.bar(x + width, cpu3, width, label='%CPU3 - AVG', color='green')

# Gắn nhãn và tiêu đề
plt.xlabel('Algorithm')
plt.ylabel('% CPU')
plt.title('CPU Usage Comparison Between RR and CA')
plt.xticks(x, algorithms)  # Đặt nhãn trục hoành
plt.legend()

# Hiển thị giá trị trên đỉnh các cột
for i in range(len(algorithms)):
    plt.text(i - width, cpu1[i] + 2, str(cpu1[i]), ha='center', fontweight='bold')
    plt.text(i, cpu2[i] + 2, str(cpu2[i]), ha='center', fontweight='bold')
    plt.text(i + width, cpu3[i] + 2, str(cpu3[i]), ha='center', fontweight='bold')

# Lưu biểu đồ thành file ảnh
plt.savefig("cpu_usage_comparison.png", format="png", dpi=300)

# Hiển thị biểu đồ
plt.show()


# Dữ liệu
algorithms = ['RR', 'CA']
cpu1 = [70.1, 25]
cpu2 = [54.8, 30]
cpu3 = [50.4, 22]

# Thiết lập vị trí của các cột trên trục hoành
x = np.arange(len(algorithms))
width = 0.25  # Độ rộng của mỗi cột

# Vẽ biểu đồ cột
plt.figure(figsize=(10, 6))
plt.bar(x - width, cpu1, width, label='%RAM1 - AVG', color='blue')
plt.bar(x, cpu2, width, label='%RAM2 - AVG', color='orange')
plt.bar(x + width, cpu3, width, label='%RAM3 - AVG', color='green')

# Gắn nhãn và tiêu đề
plt.xlabel('Algorithm')
plt.ylabel('% RAM')
plt.title('RAM Usage Comparison Between RR and CA')
plt.xticks(x, algorithms)  # Đặt nhãn trục hoành
plt.legend()

# Hiển thị giá trị trên đỉnh các cột
for i in range(len(algorithms)):
    plt.text(i - width, cpu1[i] + 2, str(cpu1[i]), ha='center', fontweight='bold')
    plt.text(i, cpu2[i] + 2, str(cpu2[i]), ha='center', fontweight='bold')
    plt.text(i + width, cpu3[i] + 2, str(cpu3[i]), ha='center', fontweight='bold')

# Lưu biểu đồ thành file ảnh
plt.savefig("ram_usage_comparison.png", format="png", dpi=300)

# Hiển thị biểu đồ
plt.show()
