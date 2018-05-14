# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 11:19:57 2013

@author: svenni
"""

# modified

from pylab import *
from scipy.ndimage import measurements
from scipy.stats import linregress
from walk import walk
from tqdm import tqdm

def masswalk(L, p):
    ncount = 0
    perc = []
    while (len(perc) == 0):
        ncount = ncount + 1
        if(ncount > 1000):
            print("Couldn't make percolation cluster...")
            mass = 0
            break
        
        z = rand(L, L) < pc
        lw, num = measurements.label(z)
        perc_x = intersect1d(lw[0,:],lw[-1,:])
        perc = perc_x[where(perc_x > 0)]
    
    if len(perc) > 0:
        labelList = arange(num + 1)
        area = measurements.sum(z, lw, index=labelList)
        areaImg = area[lw]
        maxArea = area.max()
        zz = (lw == perc[0])
        
        l,r = walk(zz)    
        zzz = l*r # Find points where both l and r are non-zero
        zadd = zz + zzz
        mass = count_nonzero(zzz)
    
        return mass

no_samples = 1000
pc = 0.59275
sizes = np.array([2**k for k in range(2,10)])
masses = np.zeros(len(sizes))

for j, L in enumerate(sizes):
    print("L = 2**%d" % int(log2(L)))
    for i in tqdm(range(no_samples)):
        masses[j] += masswalk(L, pc)

masses /= no_samples

plot(sizes, masses)
plt.title("Mass of the singly connected bonds")
plt.xlabel("System size L")
plt.ylabel("Mass")
plt.savefig("mass_sc.png")
plt.clf()

D, lnc = linregress(log(sizes), log(masses))[:2]
print(D)

L = 2**9
ps = np.linspace(0.45, 0.58, 14)
p_sc = np.zeros(len(ps))
for j, p in enumerate(ps):
    print("p = %f" % p)
    mass = 0
    for i in tqdm(range(no_samples)):
        mass += masswalk(L, p)
    mass /= no_samples

    p_sc[j] = mass/(L*L)

plot(np.abs(ps - pc), p_sc)
plt.title("Singly connected cluster density")
plt.xlabel("Size L")
plt.ylabel("Cluster density")
plt.savefig("p_sc.png")
plt.clf()
