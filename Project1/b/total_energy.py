import pandas as pd
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
for dt in [0.0001, 0.0005, 0.0010, 0.0050, 0.0100]:
    infile = "logs/log.dt_%.4f" % dt
    outfile = "data/energy.dt_%.4f" % dt
    if not os.path.exists(infile):
        os.system('lmp_serial < in.timestep -log ' + infile + ' -var dt %f' % dt)
    read_log(infile, outfile)
    df = pd.read_csv(outfile, delim_whitespace=True)
    df['TotEngNormal'] = df['TotEng']/df['TotEng'].iloc[0]*100
    plt.plot(df['Step'], df['TotEngNormal'], label="dt=%.4f" % dt)

plt.legend()
plt.xlabel('Timestep')
plt.ylabel('$E_n / E_0$', fontsize=15)
plt.tight_layout()
plt.savefig('plots/total_energy.png')
