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

read_log('log.lammps', 'thermo.csv')
df = pd.read_csv('thermo.csv', delim_whitespace=True)
N = df['Atoms'].iloc[0]

df['TotEng'].divide(df['TotEng'].max()).plot()
plt.show()

df['KinEng'].plot()
df['PotEng'].plot()
plt.show()

temp = df['KinEng'].values * (2/3)  # k_B = ???
df['Temp'].plot()
plt.plot(temp)
plt.show()

