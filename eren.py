import numpy as np
import matplotlib.pyplot as plt


x = np.load("./pos_arr_x.npy")
y = np.load("./pos_arr_y.npy")

plt.plot(x, -y, "-gD")
plt.show()