from pylab import *
from scipy.ndimage import measurements
from scipy.stats import linregress
from tqdm import tqdm

no_samples = 1000
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

plt.plot(sizes, p_pi_below)
plt.xlabel("System size L")
plt.ylabel("Fill probability")
plt.title("Fill probability for Pi(p,L)=0.3")
plt.savefig("p_pi_below.png")
plt.clf()

plt.plot(sizes, p_pi_above)
plt.xlabel("System size L")
plt.ylabel("Fill probability")
plt.title("Fill probability for Pi(p,L)=0.8")
plt.savefig("p_pi_above.png")
plt.clf()

nu, lnc = linregress(np.log(sizes), np.log(p_pi_above - p_pi_below))[:2]
print(-1/nu)
