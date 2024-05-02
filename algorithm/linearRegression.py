from __future__ import division, print_function, unicode_literals
import numpy as np 
import matplotlib.pyplot as plt

# Dữ liệu
X = np.array([[3, 4, 5, 6, 7]]).T  # Ram (e-1 Gb)
y = np.array([[20, 34.395, 55.939, 58.940, 30.812]]).T  # Responsetime (e-2s)

# Building Xbar 
one = np.ones((X.shape[0], 1))
Xbar = np.concatenate((one, X), axis=1)

# Calculating weights of the fitting line 
A = np.dot(Xbar.T, Xbar)
b = np.dot(Xbar.T, y)
w = np.dot(np.linalg.pinv(A), b)
print('w = ', w)

# Preparing the fitting line 
w_0 = w[0][0]
w_1 = w[1][0]
x0 = np.linspace(2.5, 7.5, 2)
y0 = w_0 + w_1 * x0

# Drawing the fitting line 
plt.plot(X.T, y.T, 'ro')  # data 
plt.plot(x0, y0)  # the fitting line
plt.xlabel('Ram (Gb)')
plt.ylabel('Responsetime (s)')
plt.show()

# Hệ số góc của đường tuyến tính
slope = w[1][0]
print("Hệ số góc của đường tuyến tính:", slope)
