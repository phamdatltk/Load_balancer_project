import numpy as np 
import matplotlib.pyplot as plt

# Dữ liệu
X = np.array([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]]).T 
y = np.array([[12.68, 33.078, 51.60, 39.05, 27.76, 50.79, 51, 52, 53, 58, 60, 64, 63, 62, 68, 70, 72, 80, 86]]).T  

# Xây dựng Xbar 
one = np.ones((X.shape[0], 1))
Xbar = np.concatenate((one, X), axis=1)

# Tính toán trọng số của đường thẳng hồi quy 
A = np.dot(Xbar.T, Xbar)
b = np.dot(Xbar.T, y)
w = np.dot(np.linalg.pinv(A), b)
print('w = ', w)

# Hệ số góc của đường thẳng tuyến tính
slope = w[1][0]
print("Hệ số góc của đường tuyến tính:", slope)

# Chuẩn bị đường thẳng phù hợp 
w_0 = w[0][0]
w_1 = w[1][0]
x0 = np.linspace(0, 20, 2)  # Phạm vi mở rộng cho x0
y0 = w_0 + w_1 * x0

# Vẽ đường thẳng hồi quy 
plt.plot(X, y, 'ro')  # dữ liệu 
plt.plot(x0, y0, 'b-')  # đường thẳng phù hợp
plt.xlabel('Number of requests')
plt.ylabel('Response time (s)')
plt.title('Linear Regression Fit')
plt.show()
