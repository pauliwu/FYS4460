import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

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

def pressure(rho, a, b, N=4000):
    T = 1
    return (rho*N*T)/(1-rho*b) - a*rho**2

avg_pressure = np.zeros((6,5))
for i, rho in enumerate([0.01, 0.02, 0.05, 0.10, 0.50, 1.00]):
    for j, temp in enumerate([1, 2, 3, 5, 10]):
        infile = "logs/log_rho_%.2f_temp_%d" % (rho, temp)
        outfile = "press/press_rho_%.2f_temp_%d.csv" % (rho, temp)
        files = os.listdir('logs')
        if('log_rho_%.2f_temp_%d' % (rho, temp) not in files):
            os.system('lammps < in.tempdensity -log ' + infile + ' -var rho %f -var temp %f' % (rho, temp))
            read_log(infile, outfile)

        df = pd.read_csv(outfile, delim_whitespace=True)
        avg_pressure[i][j] = df['Press'].mean()
plt.plot(avg_pressure[:,0])
plt.show()

xdata = np.array([0.01, 0.02, 0.05, 0.10, 0.50, 1.00])
ydata = avg_pressure[:,0]
plt.plot(xdata, ydata)

popt, pcov = curve_fit(pressure, xdata, ydata, p0=[2,2])
plt.plot(xdata, pressure(xdata, *popt))
plt.show()
