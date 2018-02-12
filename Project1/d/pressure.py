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

for temp in [1, 2, 3, 5, 10]:
    infile = "logs/log_temp_%d" % temp
    outfile = "press/press_temp_%d.csv" % temp

    os.system('lammps < in.pressure -log ' + infile + ' -var temp %d' % temp)
    read_log(infile, outfile)

    df = pd.read_csv(outfile, delim_whitespace=True)
    df['Press'].plot()
plt.show()
