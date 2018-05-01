from pylab import *
from scipy.ndimage import measurements
from tqdm import tqdm

L = 100
no_samples = 1000
no_probabilities = 100

occupied_probability = linspace(0.4,1.0,no_probabilities)
spanning_density = np.zeros(no_probabilities)
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
            spanning_density[j] += area.max()

spanning_density /= (no_probabilities*L*L)
plot(occupied_probability, spanning_density)
xlabel("Fill probability p")
ylabel("Spanning cluster density P(p,L)")
title("Spanning cluster density for L=%d" % L)
savefig("spanning_cluster_density.png")
