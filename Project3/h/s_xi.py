from pylab import *
from scipy.ndimage import measurements
from scipy.stats import linregress
from tqdm import tqdm

no_samples = 1000
L = 512
p_c = 0.59275
p_below = np.linspace(0.45, 0.58, 14)
s_xis = np.zeros(len(p_below))

# n(s,p_c)
print("p = %f" % p_c)
sizes = []
for i in tqdm(range(no_samples)):
    r = rand(L,L)
    z = r < p_c
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

bins = np.logspace(0, 5, 20)
hist, bin_edges = np.histogram(sizes, bins=bins)

bin_centers = (bins[1:] + bins[:-1])*0.5
cluster_number_density_pc = hist/(no_samples*L*L*np.diff(bins))

# n(s,p)
for j, p in enumerate(p_below):

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

    hist, bin_edges = np.histogram(sizes, bins=bins)
    
    cluster_number_density = hist/(no_samples*L*L*np.diff(bins))
    F = cluster_number_density/cluster_number_density_pc

    s_xis[j] = bins[np.argmin(F > 0.5)]

    plt.plot(np.log10(bin_centers), np.log10(F), label="p=%f" % p)
plt.legend()
plt.title("Universal curve F(s/s_xi)")
plt.xlabel("log10 of size s")
plt.ylabel("log10 F(s/s_xi)")
plt.savefig("F.png")
plt.clf()

plt.plot(p_below, s_xis)
plt.title("Characteristic cluster size as a function of fill probability p")
plt.xlabel("fill probability p")
plt.ylabel("characterisitic cluster size s_xi")
plt.savefig("s_xi.png")
plt.clf()

lnc, sigma = linregress(np.log10(p_c - p_below), np.log10(s_xis))[:2]
print(sigma)
