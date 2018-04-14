import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate

z = np.random.uniform(0.0, 1.0, 1000000)**(-3+1)
z_sort = np.sort(z)

plt.figure(1)
plt.plot(z)
plt.figure(2)
plt.plot(z_sort)
plt.show()
