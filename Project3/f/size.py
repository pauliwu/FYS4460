from pylab import *
from scipy.ndimage import measurements

no_samples = 1000
L = 200
p_below = np.array([0.45, 0.50, 0.54, 0.57, 0.58])
p_above = np.array([0.75, 0.70, 0.65, 0.62, 0.60])

sizes = []
p = 0.58
for i in range(no_samples):
    r = rand(L,L)
    z = r < p
    lw, num = measurements.label(z)
    area = measurements.sum(z, lw, index=arange(lw.max() + 1))
    sizes.append(area)
sizes = np.concatenate(sizes)

bins = np.linspace(0, sizes.max(), 200)
hist, bin_edges = np.histogram(sizes, bins=bins)

plt.plot(bin_edges[1:], hist)
plt.show()

plt.plot(np.log(bin_edges[1:]), np.log(hist))
plt.show()

for p in p_below:

    sizes = []
    for i in range(no_samples):
        r = rand(L,L)
        z = r < p
        lw, num = measurements.label(z)
        area = measurements.sum(z, lw, index=arange(lw.max() + 1))
        sizes.append(area)
    sizes = np.concatenate(sizes)

    bins = np.logspace(0, np.log2(sizes.max()), 50)
    hist, bin_edges = np.histogram(sizes, bins=bins)
    
    bin_centers = (bins[1:] + bins[:-1])*0.5
    nsp = hist/(no_samples*L*L*np.diff(bins))
    
    plt.plot(bin_centers, nsp, label="p=%f" % p)
    plt.xscale('log')
    plt.yscale('log')
    plt.xlim([10**(0), 10**5])
plt.legend()
plt.show()

for p in p_above:

    sizes = []
    for i in range(no_samples):
        r = rand(L,L)
        z = r < p
        lw, num = measurements.label(z)
        area = measurements.sum(z, lw, index=arange(lw.max() + 1))
        sizes.append(area)
    sizes = np.concatenate(sizes)

    bins = np.logspace(0, np.log2(sizes.max()), 50)
    hist, bin_edges = np.histogram(sizes, bins=bins)
    
    bin_centers = (bins[1:] + bins[:-1])*0.5
    nsp = hist/(no_samples*L*L*np.diff(bins))
    
    plt.plot(bin_centers, nsp, label="p=%f" % p)
    plt.xscale('log')
    plt.yscale('log')
    plt.xlim([10**(0), 10**5])
plt.legend()
plt.show()
