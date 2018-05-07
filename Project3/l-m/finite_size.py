from pylab import *
from scipy.ndimage import measurements
from tqdm import tqdm

no_samples = 100
no_probabilities = 100
sizes = np.array([25, 50, 100, 200, 400, 800])
p_pi_below = np.zeros(len(sizes))
p_pi_above = np.zeros(len(sizes))
occupied_probability = linspace(0.4,1.0,no_probabilities)

percolation_probability = np.zeros(no_probabilities)
for k, L in enumerate(sizes):
    print("L = %d" % L)
    for i in tqdm(range(no_samples)):
        r = rand(L,L)
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
    
    percolation_probability /= no_samples
    p_pi_below[k] = occupied_probability[np.argmax(percolation_probability > 0.3)]
    p_pi_above[k] = occupied_probability[np.argmax(percolation_probability > 0.8)]

plt.plot(p_pi_below)
plt.show()

plt.plot(p_pi_above)
plt.show()

plt.plot(np.log2(p_pi_above - p_pi_below), np.log2(sizes))
plt.show()

lnc, nu = linregress(np.log(p_pi_above - p_pi_below), np.log(sizes))[:2]
print(nu)
