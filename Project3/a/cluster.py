from pylab import *
from scipy.ndimage import measurements

L = 100
no_samples = 100
no_probabilities = 100

occupied_probability = linspace(0.4,1.0,no_probabilities)
spanning_density = np.zeros(no_probabilities)
percolation_probability = np.zeros(no_probabilities)
for i in range(no_samples):
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
            percolation_probability[j] += 1

spanning_density /= (no_probabilities*L*L)
percolation_probability /= no_probabilities

figure(1)
plot(occupied_probability, percolation_probability)
figure(2)
plot(occupied_probability, spanning_density)
show()
