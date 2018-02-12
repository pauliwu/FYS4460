import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

def gaussian(x, mu=0, std=1):
    factor = 1/(np.sqrt(2*np.pi*std*std))
    exponent = -(x-mu)*(x-mu)/(2*std*std)
    return factor*np.exp(exponent)

files = sorted(os.listdir('histograms'))

dfs = [pd.read_csv('histograms/' + histfile, delim_whitespace=True, names=['Velocity.X', 'Count'],
                    skiprows=[0]) for histfile in files]

diffs_square = np.zeros(len(dfs))
for i in range(len(dfs)):
    a = dfs[i]['Velocity.X'].iloc[0]
    b = dfs[i]['Velocity.X'].iloc[-1]
    N = dfs[i]['Velocity.X'].count()
    dx = (b-a)/N
    x = np.linspace(a, b, N)

    dfs[i]['Product'] = dfs[i]['Velocity.X']*dfs[i]['Count']
    dfs[i]['Normalized'] = dfs[i]['Count']/(dfs[i]['Count'].sum()*dx)
    mu = dfs[i]['Product'].mean()
    std = dfs[i]['Product'].std()

    dfs[i].plot(x='Velocity.X', y='Normalized')
    plt.plot(x, gaussian(x))
    plt.show()

    diffs_square[i] = np.mean((dfs[i]['Normalized'].values - gaussian(x))**2)

plt.plot(diffs_square)
plt.show()
