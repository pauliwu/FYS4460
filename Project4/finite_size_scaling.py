from methods import *
from pylab import *
from scipy.ndimage import measurements
from scipy.stats import linregress
from tqdm import tqdm
import seaborn as sns
import sys

sns.set(font_scale=2)
rcParams['figure.figsize'] = [14, 16]

max_rnd = 1.0
no_samples = 1000
no_probabilities = 100

steps = np.array([n for n in range(4,10)])
max_indices = np.array([2**n for n in steps])
p_pi_below = np.zeros(len(steps))
p_pi_above = np.zeros(len(steps))
occupied_probability = linspace(0.1, 1.0, no_probabilities)
percolation_probability = np.zeros(no_probabilities)

for k, L in enumerate(steps):
    ds_steps = steps[k]
    max_index = max_indices[k]
    L = max_indices[k] + 1
    print("L = %d" % L)
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
    p_pi_below[k] = occupied_probability[np.argmax(percolation_probability > 0.1)]
    p_pi_above[k] = occupied_probability[np.argmax(percolation_probability > 0.8)]

plt.plot(2**steps+1, p_pi_below)
plt.xlabel("System size L")
plt.ylabel("Fill probability")
plt.title("Fill probability for Pi(p,L)=0.1")
plt.savefig("plots/p_pi_below.png")
plt.clf()

plt.plot(2**steps+1, p_pi_above)
plt.xlabel("System size L")
plt.ylabel("Fill probability")
plt.title("Fill probability for Pi(p,L)=0.8")
plt.savefig("plots/p_pi_above.png")
plt.clf()

nu, lnc = linregress(np.log(2**steps + 1), np.log(p_pi_above - p_pi_below))[:2]
print(-1/nu)
