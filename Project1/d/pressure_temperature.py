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

temperatures = np.arange(1,16)
average_pressure = np.zeros(len(temperatures))
average_temperature = np.zeros(len(temperatures))
for i, temp in enumerate(temperatures):
    infile = "logs/log.temp_%.4f" % temp
    outfile = "data/pressure.temp_%.4f" % temp
    if not os.path.exists(infile):
        os.system('lammps < in.pressure -log ' + infile + ' -var temp %d' % temp)
    read_log(infile, outfile)

    df = pd.read_csv(outfile, delim_whitespace=True)
    
    plt.plot(df['Step'], df['Press'])
    plt.xlabel('Timestep')
    plt.ylabel('Pressure')
    plt.savefig('plots/pressure_temp_%.4f.png' % temp)
    plt.clf()

    # find equilibrium timestep
    mean_temp = df['Temp'].mean()
    df['RelDiff'] = abs((df['Temp']-mean_temp)/(df['Temp'].iloc[0]-mean_temp))
    equilibrium = (df['RelDiff'] < 0.1).idxmax()
    
    average_pressure[i] = df['Press'][equilibrium:].mean()
    average_temperature[i] = df['Temp'][equilibrium:].mean()

plt.plot(average_temperature, average_pressure)
plt.xlabel('Temperatures')
plt.ylabel('Average pressure')
plt.savefig('plots/avg_pressure.png')
