import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

datadir = "data/"
os.system("mkdir -p %s" % datadir)

b = 5.72
sigma = 3.405
bs = b/sigma
radius = 2*2.94
total_particles = 32000
viscosity = 0.73

no_spheres = [i for i in range(5,16)]
porosity = 1 - np.array(no_spheres)*(4/3)*np.pi*(radius/(20*bs))**3
outfiles = [datadir + "%d.lammpstrj" % i for i in no_spheres]
datafiles = [datadir + "%d.csv" % i for i in no_spheres]

avg_velocity = np.zeros(len(no_spheres))
number_of_particles = np.zeros(len(no_spheres))
for i, n  in enumerate(no_spheres):
    if not os.path.exists(outfiles[i]):
        os.system("lmp_serial < in.porosity -var no_spheres %d -var dump %s" % (n, outfiles[i]))
    if not os.path.exists(datafiles[i]):
        os.system("ovitos ovitos_velocity.py %s %s" % (outfiles[i], datafiles[i]))

    df = pd.read_csv(datafiles[i], header=None)
    avg_velocity[i] = df.values[0][0]
    number_of_particles[i] = df.values[1][0]

number_density = number_of_particles/total_particles

permeability = avg_velocity*viscosity/(number_density*0.1)
permeability_theoretical = radius**2/45 * porosity**3/(1-porosity)**2

plt.style.use('default')
plt.plot(porosity, permeability)
plt.plot(porosity, permeability_theoretical)
plt.legend(["Measured", "Carman-Kozeny"])
plt.title("Permeability as a function of porosity")
plt.xlabel("Porosity")
plt.ylabel("Permeability")
plt.savefig("permeability.png")
