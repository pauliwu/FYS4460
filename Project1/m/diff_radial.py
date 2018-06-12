import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from tqdm import tqdm
from scipy.stats import linregress

os.system('mkdir -p data')
os.system('mkdir -p dumps')
os.system('mkdir -p logs')
os.system('mkdir -p plots')

def read_log(log, thermo):
     with open(log, 'r') as infile:
        with open(thermo, 'w') as outfile:
            header = 'Step'
            bottom = 'Loop'
            line = infile.readline()
            while(header not in line):
                line = infile.readline()

            while(bottom not in line):
                outfile.write(line)
                line = infile.readline()

temperatures = np.linspace(150.0, 350.0, 100)
diffusion_constants = np.zeros(len(temperatures))
for i, temp in enumerate(tqdm(temperatures)):
    logfile = 'logs/log.temp_%.4f' % temp
    dumpfile = 'dumps/dump.temp_%.4f' % temp
    datafile = 'data/msd.temp_%.4f' % temp

    # run simulation
    if not os.path.exists(logfile):
        os.system('mpirun -np 4 lammps -in spce-water-system.in -log %s \
                    -var temp %.4f -var dump %s > /dev/null' 
                    % (logfile, temp, dumpfile))

    # compute radial distributions
    os.system('ovitos ovitos_radial.py %.4f' % temp)
    dfs = [pd.read_csv('data/radial.temp_%.4f_frame_%d' % (temp, frame), 
            delim_whitespace=True, 
            names=['r', 'g(r)']) for frame in range(0,501,10)]
    df = pd.concat(dfs, axis=1)
    df['time averaged g(r)'] = df['g(r)'].sum(1)/len(df['g(r)'].columns)
    
    if i%10 == 0:
        no_bins = len(df['time averaged g(r)'])
        plt.plot(np.linspace(0,15,no_bins), df['time averaged g(r)'])
        plt.axis([0,15,0,8])
        plt.xlabel('distance r')
        plt.ylabel('g(r)')
        plt.savefig('plots/radial_temp_%.4f.png' % temp)
        plt.clf()

    # compute diffusion constant
    read_log(logfile, datafile)
    df = pd.read_csv(datafile, delim_whitespace=True)
    a, b, r, p, std = linregress(df['Step'][10:], df['msd[4]'][10:])
    if i%10 == 0:
        plt.plot(df['Step'], df['msd[4]'])
        plt.plot(df['Step'], a*df['Step']+b)
        plt.xlabel('Time')
        plt.ylabel('MSD')
        plt.savefig('plots/msd_temp_%.4f.png' % temp)
        plt.clf()
    
    diffusion_constants[i] = a/6

plt.plot(temperatures, diffusion_constants)
plt.xlabel('Temperature')
plt.ylabel('Diffusion constant')
plt.savefig('plots/diffusion_constant.png')
