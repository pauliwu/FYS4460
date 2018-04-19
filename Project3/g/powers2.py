from pylab import *
from scipy.ndimage import measurements

no_samples = 1000
ks = np.array([k for k in range(4,10)])
pc = 0.59275

for k in ks:
    L = 2**k
    sizes = []
    for i in range(no_samples):
        r = rand(L,L)
        z = r < pc
        lw, num = measurements.label(z)
        area = measurements.sum(z, lw, index=arange(lw.max() + 1))
        sizes.append(area)
    sizes = np.concatenate(sizes)
    
    bins = np.logspace(0, np.log2(sizes.max()), 50)
    hist, bin_edges = np.histogram(sizes, bins=bins)
    
    bin_centers = (bins[1:] + bins[:-1])*0.5
    nsp = hist/(no_samples*L*L*np.diff(bins))
    
    plt.plot(bin_centers, nsp, label="L=2**%d" % k)
    plt.xscale('log')
    plt.yscale('log')
    plt.xlim([10**(0), 10**5])
plt.legend()
plt.show()
