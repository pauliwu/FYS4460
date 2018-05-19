import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

b = 5.72
sigma = 3.405
bs = b/sigma

bin_min, bin_max = [0.0*bs, 5.0*bs]
no_bins = 30
bins = np.sqrt(np.linspace(bin_min**2, bin_max**2, no_bins))

df = pd.read_csv('radial_velocity.csv', header=None)
plt.plot(bins, df)
plt.title("Flow profile in a cylinder")
plt.xlabel("Radial distance")
plt.ylabel("Velocity")

b, a = linregress(bins**2, df[0].values)[:2]
volume = np.pi*(5*bs)**2*(20*bs)
number = 3137
mu = -(number/volume)*0.1/(4*b)
print(mu)

continuum = (number/volume * 0.1/(4*mu))*(bin_max**2 - bins**2)
plt.plot(bins, continuum)
plt.legend(["Measured", "Continuum"])
plt.savefig("radial_velocity.png")
