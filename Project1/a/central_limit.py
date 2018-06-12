import os

os.system('mkdir -p plots')
os.system('lmp_serial < in.uniformvelocity')
os.system('ovitos ovitos_histogram.py')
