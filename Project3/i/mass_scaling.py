from pylab import *
from scipy.ndimage import measurements
from scipy.stats import linregress
from tqdm import tqdm

no_samples = 1000
pc = 0.59275
ks = np.array([k for k in range(4, 12)])
areas = np.zeros(len(ks))

for i, k in enumerate(ks):
    L = 2**k
    print("L=2**%d" % k)
    areaSum = 0.0
    percolations = 0.0
    for j in tqdm(range(no_samples)):
        r = rand(L,L)
        z = r < pc
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

plt.plot(ks, np.log2(areas))
plt.title("Mass of the percolation cluster")
plt.xlabel("log2 of system size L")
plt.ylabel("log2 of mass M")
plt.savefig("mass_scaling.png")

D, lnc = linregress(ks, np.log2(areas))[:2]
print(D)
