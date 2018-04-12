import numpy as np
from mpi4py import MPI
from lammps import lammps

lmp = lammps()
lines = open('in.matrix','r').readlines()
linenumber = 0
for line in lines:
    if 'velocity' in line:
        break
    lmp.command(line)
    linenumber += 1
lines = lines[linenumber:]

pos = np.random.uniform(0.0,40.0,size=(20,3))
rad = np.random.uniform(2.0,3.0,size=20)
for i in range(20):
    lmp.commands_list([
        'region cut sphere %f %f %f %f units box' % 
            (pos[i][0],pos[i][1],pos[i][2],rad[i]),
        'group spheres region cut',
        'region cut delete'])

for line in lines:
    lmp.command(line)
