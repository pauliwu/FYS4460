import pandas as pd
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
outfile = 'data.temp'
if not os.path.exists(infile):
    os.system('lmp_serial < in.half')
read_log(infile, outfile)
df = pd.read_csv(outfile, delim_whitespace=True)
plt.plot(df['Step'], df['Temp'])
plt.show()
