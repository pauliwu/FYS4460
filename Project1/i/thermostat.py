import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from tqdm import tqdm

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

temperatures = np.linspace(0.1, 5.0, 10)
for i, temp in enumerate(tqdm(temperatures)):
    infile = "logs/log.temp_%.4f" % temp
    outfile = "data/thermo.temp_%.4f" % temp
    
    if not os.path.exists(infile):
        os.system('lammps < in.nosehoover -log ' + infile + ' -var temp %f > /dev/null' % temp)
    read_log(infile, outfile)

    df = pd.read_csv(outfile, delim_whitespace=True)
    plt.plot(df['Step'], df['Temp'])
    plt.xlabel('Timestep')
    plt.ylabel('Temperature')
    plt.savefig('plots/thermostat_temp_%.4f.png' % temp)
    plt.clf()
