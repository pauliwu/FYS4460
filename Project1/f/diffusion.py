import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from tqdm import tqdm
from scipy.stats import linregress

os.system('mkdir -p data')
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

temperatures = np.linspace(0.69, 0.72, 30)
equilibrium_temperatures = np.zeros(len(temperatures))
diffusion_constants = np.zeros(len(temperatures))
for i, temp in enumerate(tqdm(temperatures)):
    infile = "logs/log.temp_%.4f" % temp
    outfile = "data/msd.temp_%.4f" % temp
    if not os.path.exists(infile):
        os.system('mpirun -np 4 lmp_mpi < in.diffusion -log ' + infile + ' -var temp %f > /dev/null' % temp)
    read_log(infile, outfile)

    df = pd.read_csv(outfile, delim_whitespace=True)

    a, b = linregress(df['Step'], df['c_msd[4]'])[:2]
    plt.plot(df['Step'], df['c_msd[4]'])
    plt.plot(df['Step'], a*df['Step']+b)
    plt.xlabel('Timestep')
    plt.ylabel('MSD')
    plt.savefig('plots/diffusion_temp_%.4f.png' % temp)
    plt.clf()

    # find equilibrium timestep
    mean_temp = df['Temp'].mean()
    df['RelDiff'] = abs((df['Temp']-mean_temp)/(df['Temp'].iloc[0]-mean_temp))
    equilibrium = (df['RelDiff'] < 0.1).idxmax()


    diffusion_constants[i] = a/6
    equilibrium_temperatures[i] = df['Temp'][equilibrium:].mean()

plt.plot(equilibrium_temperatures, diffusion_constants)
plt.xlabel('Equilibrium temperature')
plt.ylabel('Diffusion constant')
plt.savefig('plots/diffusion_constant.png')
