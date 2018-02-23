import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from tqdm import tqdm

temperatures = np.linspace(0.1, 3.0, 10)

for i, temp in enumerate(tqdm(temperatures)):
    # run simulation
    os.system('lammps < in.radial -var temp %.4f > /dev/null' % temp)
    
    # compute radial distributions
    os.system('ovitos ovitos_radial.py %.4f' % temp)
    
    dfs = [pd.read_csv('data/radial.temp_%.4f_frame_%d' % (temp, frame), delim_whitespace=True, 
            names=['r', 'g(r)']) for frame in range(0,501,10)]
    df = pd.concat(dfs, axis=1)
    df['time averaged g(r)'] = df['g(r)'].sum(1)/len(df['g(r)'].columns)
    df['time averaged g(r)'].plot()
    plt.axis([0,200,0,3])
    plt.savefig('plots/radial_temp_%.4f.png' % temp)
    plt.clf()
