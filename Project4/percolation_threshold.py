from methods import *
from pylab import *
from scipy.ndimage import measurements
from scipy.stats import linregress
from tqdm import tqdm
import seaborn as sns
import sys

sns.set(font_scale=2)
rcParams['figure.figsize'] = [16, 14]

max_rnd = 1.0
no_samples = 1000
no_probabilities = 100
nu = 9.32041189553
xs = 0.1

steps = np.array([n for n in range(4,10)])
max_indices = np.array([2**n for n in steps])
p_pis = np.zeros(len(steps))
occupied_probability = linspace(0.1, 1.0, no_probabilities)

for l, L in enumerate(steps):
    ds_steps = steps[l]
    max_index = max_indices[l]
    L = max_indices[l] + 1
    percolation_probability = np.zeros(no_probabilities)
    print("xs=%f L=%f" % (xs, L))
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

    percolation_probability /= no_samples
    p_pis[l] = occupied_probability[np.argmax(percolation_probability > xs)]

plt.plot((2**steps + 1)**(-1/nu), p_pis)
plt.xlabel("System size L^(-1/nu)")
plt.ylabel("Fill probability p of percolation")
plt.title("Fill probability for Pi(p,L)=%.1f" % xs)
plt.savefig("plots/p_pi.png")

cx, pc = linregress((2**steps + 1)**(-1/nu), p_pis)[:2]
print(pc)

# pc = 0.455479500389
