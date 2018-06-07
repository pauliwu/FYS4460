import seaborn as sns
import sys
from pylab import *
from scipy.ndimage import measurements
from scipy.stats import linregress
from tqdm import tqdm

sns.set()
sys.path.insert(0, '/home/andreas/Code/Software/Diamond_Square')

from methods import *

max_rnd = 1.0
no_samples = 1000
pc = 0.433802206662

steps = np.array([k for k in range(4,12)])
max_indices = np.array([2**n for n in steps])
areas = np.zeros(len(steps))

for i, k in enumerate(steps):
    L = max_indices[k] + 1
    ds_steps = steps[k]
    max_index = max_indices[k]
    print("L=%d" % L)
    areaSum = 0.0
    percolations = 0.0
    for j in tqdm(range(no_samples)):
        seeded_map = f_seed_grid(L, max_rnd)
        final_height_map = f_dsmain(seeded_map, ds_steps, max_index, max_rnd)
        final_height_map += abs(final_height_map.min())
        final_height_map /= abs(final_height_map.max())
        z = final_height_map < pc
        lw, num = measurements.label(z)
        area = measurements.sum(z, lw, index=arange(lw.max() + 1))
        areaImg = area[lw]
        sliced = measurements.find_objects(areaImg == areaImg.max())
    
        sliceX = sliced[0][1]
        sliceY = sliced[0][0]
        maxsize = max(sliceX.stop - sliceX.start, sliceY.stop - sliceY.start)
    
        if(maxsize == L):
            areaSum += area.max()
            percolations += 1
    
    areas[i] = areaSum / percolations

plt.plot(np.log2(max_indices + 1), np.log2(areas))
plt.title("Mass of the percolation cluster")
plt.xlabel("log2 of system size L")
plt.ylabel("log2 of mass M")
plt.savefig("plots/mass_scaling.png")

D, lnc = linregress(ks, np.log2(areas))[:2]
print(D)
