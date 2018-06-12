from methods import *
from pylab import *
from scipy.ndimage import measurements
from scipy.stats import linregress
from tqdm import tqdm
import seaborn as sns
import sys

sns.set()

def correlation_function(lw):
    nx, ny = lw.shape
    L = max([nx, ny])
    r = arange(1, 2*L+1)
    pr = zeros(2*L)
    npr = zeros(2*L)
    for i in range(nx):
        for j in range(ny):
            site1 = lw[i,j]
            for k in range(nx):
                for l in range(ny):
                    site2 = lw[k,l]
                    dx = i - k
                    dy = j - l
                    nr = int(hypot(dx,dy))
                    pr[nr] += (site1 == site2)*(site1 > 0)
                    npr[nr] += 1
    mask = nonzero(npr)
    pr[mask] /= npr[mask]
    return r, pr

ds_steps = 6
max_rnd = 1.0
max_index = 2**ds_steps
L = max_index + 1
no_samples = 10

p_rand = 0.58
r_avg, g_avg = zeros(2*L), zeros(2*L)
for j in tqdm(range(no_samples)):
    r = rand(L,L)

    z = r < p_rand
    lw, num = measurements.label(z)
    r, g = correlation_function(lw)
    r_avg += r
    g_avg += g
r_avg /= no_samples
g_avg /= no_samples

mask = nonzero(g_avg)
r_avg, g_avg = r_avg[mask], g_avg[mask]
b, a = linregress(log(r_avg), log(g_avg))[:2]
H_rand = b/2

plot(log(r_avg), log(g_avg))

p_corr = 0.48
r_avg, g_avg = zeros(2*L), zeros(2*L)
for j in tqdm(range(no_samples)):
    seeded_map = f_seed_grid(L, max_rnd)
    final_height_map = f_dsmain(seeded_map, ds_steps, max_index, max_rnd)
    final_height_map += abs(final_height_map.min())
    final_height_map /= abs(final_height_map.max())

    z = final_height_map < p_corr
    lw, num = measurements.label(z)
    r, g = correlation_function(lw)
    r_avg += r
    g_avg += g
r_avg /= no_samples
g_avg /= no_samples

mask = nonzero(g_avg)
r_avg, g_avg = r_avg[mask], g_avg[mask]
b, a = linregress(log(r_avg), log(g_avg))[:2]
H_corr = b/2

plot(log(r_avg), log(g_avg))

print(H_rand, H_corr)
show()
