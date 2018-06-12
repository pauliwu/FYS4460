from methods import *
from pylab import *
from scipy.ndimage import measurements
from tqdm import tqdm
import seaborn as sns
import sys

sns.set()

ds_steps = 9
max_rnd = 1.0
max_index = 2**ds_steps
L = max_index + 1
no_samples = 1000
no_probabilities = 100

occupied_probability = linspace(0.1, 1.0, no_probabilities)
percolation_probability = np.zeros(no_probabilities)
for i in tqdm(range(no_samples)):
    seeded_map = f_seed_grid(L, max_rnd)
    final_height_map = f_dsmain(seeded_map, ds_steps, max_index, max_rnd)
    final_height_map += abs(final_height_map.min())
    final_height_map /= abs(final_height_map.max())
    for j in range(no_probabilities):
        z = final_height_map < occupied_probability[j]
        lw, num = measurements.label(z)
        area = measurements.sum(z, lw, index=arange(lw.max() + 1))
        areaImg = area[lw]

        sliced = measurements.find_objects(areaImg == areaImg.max())
        sliceX = sliced[0][1]
        sliceY = sliced[0][0]
        maxsize = max(sliceX.stop - sliceX.start, sliceY.stop - sliceY.start)

        if(maxsize == L):
            percolation_probability[j] += 1

percolation_probability /= (no_samples)
plot(occupied_probability, percolation_probability)

percolation_probability = np.zeros(no_probabilities)
for i in tqdm(range(no_samples)):
    r = rand(L, L)
    for j in range(no_probabilities):
        z = r < occupied_probability[j]
        lw, num = measurements.label(z)
        area = measurements.sum(z, lw, index=arange(lw.max() + 1))
        areaImg = area[lw]
        sliced = measurements.find_objects(areaImg == areaImg.max())

        sliceX = sliced[0][1]
        sliceY = sliced[0][0]
        maxsize = max(sliceX.stop - sliceX.start, sliceY.stop - sliceY.start)

        if(maxsize == L):
            percolation_probability[j] += 1

percolation_probability /= (no_samples)
plot(occupied_probability, percolation_probability)

legend(['Diamond-Square', 'Rand'])
plt.savefig('plots/percolation_probability')
show()
