from pylab import *
from scipy.ndimage import measurements
from tqdm import tqdm

no_samples = 100
no_probabilities = 100
sizes = np.array([25, 50, 100, 200, 400, 800])
p_xs = np.linspace(0.3, 0.8, 11)
p_pis = np.zeros((len(sizes), len(p_xs)))

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
    for l, xs in enumerate(p_xs):
        p_pis[k][l] = occupied_probability[np.argmax(percolation_probability > xs)]

    plt.plot(p_pis[k])
plt.show()
