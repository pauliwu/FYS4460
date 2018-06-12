import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from tqdm import tqdm

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

temperatures = np.linspace(0.1, 5.0, 10)
thermostats = ['in.berendsen', 'in.nosehoover']
for name in thermostats:
    for i, temp in enumerate(tqdm(temperatures)):
        infile = "logs/log.temp_%.4f_%s" % (temp, name[3:])
        outfile = "data/thermo.temp_%.4f_%s" % (temp, name[3:])
        
        if not os.path.exists(infile):
            os.system('mpirun -np 4 lmp_mpi < %s -log ' % name + infile + ' -var temp %f > /dev/null' % temp)
        read_log(infile, outfile)
    
        df = pd.read_csv(outfile, delim_whitespace=True)
        plt.plot(df['Step'], df['Temp'])
        plt.xlabel('Timestep')
        plt.ylabel('Temperature')
        plt.savefig('plots/%s_temp_%.4f.png' % (name[3:], temp))
        plt.clf()
