import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy.stats import linregress

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

infile = 'log.lammps'
outfile = 'data.diff'
if not os.path.exists(infile):
    os.system('lmp_serial < in.diffusion')
read_log(infile, outfile)
df = pd.read_csv(outfile, delim_whitespace=True)

a, b = linregress(df['Step'], df['c_msd[4]'])[:2]
plt.plot(df['Step'], df['c_msd[4]'])
plt.plot(df['Step'], a*df['Step']+b)
plt.show()
diffusion = a/6
print("Diffusion constant: %f" % diffusion)
