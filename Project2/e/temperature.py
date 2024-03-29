import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

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
outfile = 'temp.csv'
if not os.path.exists(infile):
    os.system('lmp_serial < in.half')
read_log(infile, outfile)
df = pd.read_csv(outfile, delim_whitespace=True)

plt.plot(df['Step'], df['Temp'])
plt.title("Temperature of nanoporous system")
plt.xlabel("Timestep")
plt.ylabel("Temperature (LJ-units)")
plt.savefig("temperature.png")
