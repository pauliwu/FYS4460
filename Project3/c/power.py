from pylab import *
from scipy.ndimage import measurements

no_samples = 100
no_probabilities = 100

sizes = np.array([100, 200, 300, 400, 500])
occupied_probability = linspace(0.58,0.62,no_probabilities)
spanning_density = np.zeros(no_probabilities)
for L in sizes:
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
    
    spanning_density /= (no_probabilities*L*L)
    critical_probability = 0.59275

    plot(log10(occupied_probability - critical_probability), log10(spanning_density), label="L=%d" % L)
legend()
savefig('plot.png')
