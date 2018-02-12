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
dt = 0.003
for dt in [0.001, 0.005, 0.0100]:
    infile = "logs/log.dt_%.4f" % dt
    outfile = "energies/energy_dt_%.4f" % dt
    os.system('lammps < in.timestep -log ' + infile + ' -var dt %f' % dt)
    read_log(infile, outfile)
    df = pd.read_csv(outfile, delim_whitespace=True)
    df['TotEngNormal'] = df['TotEng']/df['TotEng'].iloc[0]*100
    df.plot(x='Step', y='TotEngNormal')
plt.show()
