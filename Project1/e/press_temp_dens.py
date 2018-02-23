import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from tqdm import tqdm
from mpl_toolkits.mplot3d import Axes3D
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

def pressure(tempdensity, a, b):
    T, rho = tempdensity
    press = (rho*T)/(1-rho*b) - a*rho*rho
    return press.ravel()

temperatures = np.linspace(1,3,30)
densities = np.linspace(0.001, 1.0, 30)

average_pressure = np.zeros((len(temperatures), len(densities)))
equilibrium_temperature = np.zeros(len(temperatures))

for i, temp in enumerate(tqdm(temperatures)):
    for j, rho in enumerate(tqdm(densities)):
        infile = "logs/log.temp_%.4f_rho_%.4f" % (temp, rho)
        outfile = "data/pressure.temp_%.4f_rho_%.4f" % (temp, rho)
        if not os.path.exists(infile):
            os.system('lammps < in.temperaturedensity -log ' + infile + ' -var temp %f' % temp 
                        + ' -var rho %f > /dev/null' % rho)
        read_log(infile, outfile)

        df = pd.read_csv(outfile, delim_whitespace=True)
    
        # find equilibrium timestep
        mean_temp = df['Temp'].mean()
        df['RelDiff'] = abs((df['Temp']-mean_temp)/(df['Temp'].iloc[0]-mean_temp))
        equilibrium = (df['RelDiff'] < 0.1).idxmax()
    
        average_pressure[i][j] = df['Press'][equilibrium:].mean()
    equilibrium_temperature[i] = df['Temp'][equilibrium:].mean()

xs, ys = np.meshgrid(equilibrium_temperature, densities)

fig = plt.figure()
ax = Axes3D(fig)
ax.plot_surface(xs, ys, average_pressure)
ax.set_zlabel('Pressure')
plt.xlabel('Temperatures')
plt.ylabel('Densities')
plt.savefig('plots/avg_pressure.png')

# perform curve fit
pressure_data = average_pressure.ravel()
initial_guess = (1.2, 0.1)
popt, pcov = curve_fit(pressure, (xs, ys), pressure_data, p0=initial_guess)
print(popt)

# reshape pressure to 2d and plot
pressure_fit = pressure((xs,ys), popt[0], popt[1]).reshape(len(xs),len(ys))
ax.plot_surface(xs, ys, average_pressure)
ax.plot_surface(xs, ys, pressure_fit)
plt.savefig('plots/curve_fit.png')
