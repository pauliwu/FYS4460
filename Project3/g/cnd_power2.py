from pylab import *
from scipy.ndimage import measurements
from scipy.stats import linregress
from tqdm import tqdm

no_samples = 1000
pc = 0.59275
ks = np.array([i for i in range(4,10)])
taus = np.zeros(len(ks))

for j, k in enumerate(ks):

    print("L = 2**%d" % k)
    L = 2**k
    sizes = []
    for i in tqdm(range(no_samples)):
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
            area = area[where(area < area.max())]

        sizes.append(area)
    sizes = np.concatenate(sizes)

    bins = np.logspace(0, np.log2(sizes.max()), 100)
    hist, bin_edges = np.histogram(sizes, bins=bins)
    
    bin_centers = (bins[1:] + bins[:-1])*0.5
    cluster_number_density = hist/(no_samples*L*L*np.diff(bins))
    
    # remove zeros
    mask = np.nonzero(cluster_number_density)
    bin_centers = bin_centers[mask]
    cluster_number_density = cluster_number_density[mask]

    lnc, tau = linregress(np.log10(bin_centers), np.log10(cluster_number_density))[:2]
    taus[j] = tau

    plt.plot(np.log10(bin_centers), np.log10(cluster_number_density), label="L=2**%d" % k)
plt.legend()
plt.title("Cluster number density as a function of system size")
plt.xlabel("log10 of cluster size s")
plt.ylabel("log10 of cluster number density")
plt.savefig("cnd_power2.png")
plt.clf()

plt.plot(ks, taus)
plt.xlabel("log2 of system size L")
plt.ylabel("Exponent tau")
plt.title("Size scaling exponent tau as a function of system size")
plt.savefig("tau_power2.png")
plt.clf()
