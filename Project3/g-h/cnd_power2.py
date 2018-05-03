from pylab import *
from scipy.ndimage import measurements
from tqdm import tqdm

no_samples = 1000
p = 0.59275
ks = np.array([i for i in range(4,10)])

for k in ks:

    print("L = 2**%d" % k)
    L = 2**k
    sizes = []
    for i in tqdm(range(no_samples)):
        r = rand(L,L)
        z = r < p
        lw, num = measurements.label(z)
        area = measurements.sum(z, lw, index=arange(lw.max() + 1))
        areaImg = area[lw]
        sliced = measurements.find_objects(areaImg == areaImg.max())

        sliceX = sliced[0][1]
        sliceY = sliced[0][0]
        maxsize = max(sliceX.stop - sliceX.start, sliceY.stop - sliceY.start)
        if(maxsize == L):
            area = area[where(area < area.max())]

        sizes.append(area)
    sizes = np.concatenate(sizes)

    bins = np.logspace(0, np.log2(sizes.max()), 100)
    hist, bin_edges = np.histogram(sizes, bins=bins)
    
    bin_centers = (bins[1:] + bins[:-1])*0.5
    cluster_number_density = hist/(no_samples*L*L*np.diff(bins))
    
    plt.plot(bin_centers, cluster_number_density, label="L=2**%d" % k)
    plt.xscale('log')
    plt.yscale('log')
    plt.xlim([10**0, 10**5])
plt.legend()
plt.savefig("cnd_power2.png")
plt.clf()
