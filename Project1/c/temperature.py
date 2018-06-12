import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

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

sizes = np.arange(1,16)
average_temperatures = np.zeros(len(sizes))
for i, size in enumerate(sizes):
    infile = "logs/log.size_%d" % size
    outfile = "data/temp.size_%d" % size
    if not os.path.exists(infile):
        os.system('lmp_serial < in.temperature -log ' + infile + ' -var size %d' % size)
    read_log(infile, outfile)

    df = pd.read_csv(outfile, delim_whitespace=True)
    
    plt.plot(df['Step'], df['Temp'])
    plt.xlabel('Timestep')
    plt.ylabel('Temperature')
    plt.savefig('plots/temperature_size_%d.png' % size)
    plt.clf()

    # find equilibrium timestep
    mean_temp = df['Temp'].mean()
    df['RelDiff'] = abs((df['Temp']-mean_temp)/(df['Temp'].iloc[0]-mean_temp))
    equilibrium = (df['RelDiff'] < 0.1).idxmax()
    
    average_temperatures[i] = df['Temp'][equilibrium:].mean()

initial_temp = 2.5
rel_average_temp = 100*abs((average_temperatures-initial_temp)/initial_temp)
plt.plot(sizes, rel_average_temp)
plt.xlabel('System size (L)')
plt.ylabel('Average temperature relative to initial (%)')
plt.savefig('plots/rel_avg_temp.png')
