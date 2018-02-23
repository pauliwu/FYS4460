import os
import pandas as pd
import matplotlib.pyplot as plt

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

os.system('lammps < in.silicon')
read_log('log.lammps', 'test')
df = pd.read_csv('test', delim_whitespace=True)
df['msd[4]'].plot()
plt.show()

"""
for temp in [1, 2, 3, 5, 10]:
    infile = "logs/log.temp_%d" % temp
    outfile = "diffs/diff_temp_%d.csv" % temp
    
    if("log.temp_%d" % temp not in os.listdir('logs')):
        os.system('lammps < in.diffusion -log ' + infile + ' -var temp %f' % temp)
        read_log(infile, outfile)

    df = pd.read_csv(outfile, delim_whitespace=True)
    df['msd[4]'].plot()
plt.show()
"""
