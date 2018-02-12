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

for size in [1, 2, 3, 5, 10]:
    infile = "logs/log_size_%d" % size
    outfile = "temps/temp_size_%d.csv" % size

    os.system('lammps < in.temperature -log ' + infile + ' -var size %d' % size)
    read_log(infile, outfile)

    df = pd.read_csv(outfile, delim_whitespace=True)
    (df['Temp']/2.5).plot()
plt.show()
