import os

os.system('lammps < in.uniformvelocity')
os.system('ovitos ovitos_histogram.py')
