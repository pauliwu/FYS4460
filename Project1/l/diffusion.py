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

temperatures = np.linspace(1.0, 2000.0, 2000)
diffusion_constants = np.zeros(len(temperatures))
for i, temp in enumerate(tqdm(temperatures)):
    infile = "logs/log.temp_%.4f" % temp
    outfile = "data/msd.temp_%.4f" % temp
    if not os.path.exists(infile):
        os.system('lammps -in in.silicon -log ' + infile + 
                    ' -var temp %f > /dev/null' % temp)
    read_log(infile, outfile)

    df = pd.read_csv(outfile, delim_whitespace=True)
    a, b = linregress(df['Step'], df['msd[4]'])[:2]
    if int(temp) % 100 == 0:
        plt.plot(df['Step'], df['msd[4]'])
        plt.plot(df['Step'], a*df['Step']+b)
        plt.xlabel('Timestep')
        plt.ylabel('MSD')
        plt.savefig('plots/diffusion_temp_%.4f.png' % temp)
        plt.clf()
 
    diffusion_constants[i] = a/6

plt.plot(temperatures, diffusion_constants)
plt.xlabel('Temperature')
plt.ylabel('Diffusion constant')
plt.savefig('plots/diffusion_constant.png')
