from pylab import *
from scipy.ndimage import measurements
from scipy.stats import linregress
from tqdm import tqdm

no_samples = 1000
no_probabilities = 100

sizes = np.array([100, 200, 300, 400, 500])
occupied_probability = linspace(0.60,0.62,no_probabilities)
spanning_density = np.zeros(no_probabilities)
betas = np.zeros(len(sizes))
for k, L in enumerate(sizes):
    print("L = %d" % L)
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
    critical_probability = 0.59275

    lnp = log(occupied_probability - critical_probability)
    lnP = log(spanning_density)

    b, a = linregress(lnp, lnP)[:2]
    betas[k] = b

    plot(lnp, lnP, \
        label="L=%d" % L)
legend()
xlabel("ln(p - p_c)")
ylabel("ln(P(p,L))")
title("log of spanning density cluster as a function of (p - p_c)")
savefig('power.png')
clf()

plot(sizes, betas)
xlabel("Size L")
ylabel("Beta")
title("Exponent beta as a function of size L")
savefig('beta.png')
clf()
