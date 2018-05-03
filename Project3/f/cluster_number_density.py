from pylab import *
from scipy.ndimage import measurements
from tqdm import tqdm

no_samples = 1000
L = 500
p_below = np.array([0.45, 0.50, 0.54, 0.57, 0.58])
p_above = np.array([0.75, 0.70, 0.65, 0.62, 0.60])

print("\n p from below:")
for p in p_below:

    print("p = %f" % p)
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
    
    plt.plot(bin_centers, cluster_number_density, label="p=%f" % p)
    plt.xscale('log')
    plt.yscale('log')
    plt.xlim([10**(0), 10**5])
plt.legend()
plt.savefig("cnd_below.png")
plt.clf()

print("\n p from above:")
for p in p_above:

    print("p = %f" % p)
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
    
    plt.plot(bin_centers, cluster_number_density, label="p=%f" % p)
    plt.xscale('log')
    plt.yscale('log')
    plt.xlim([10**(0), 10**5])
plt.legend()
plt.savefig("cnd_above.png")
plt.clf()
