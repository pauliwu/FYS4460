import numpy as np
import matplotlib.pyplot as plt

z = np.random.uniform(0.0, 1.0, 1000000)**(-3+1)
bins = np.logspace(0, np.log10(z.max()), 200)
cumulative = np.zeros(len(bins))

for i in range(len(bins)):
    cumulative[i] = np.sum(z < bins[i])
cumulative /= len(z)

plt.plot(bins, cumulative)
plt.xscale('log')
plt.show()
