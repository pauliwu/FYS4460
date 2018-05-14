from pylab import *
from scipy.ndimage import measurements
from scipy.stats import linregress
from tqdm import tqdm

no_samples = 1000
no_probabilities = 100
nu = 4/3
xs = 0.3

sizes = np.array([25, 50, 100, 200, 400, 800])
p_pis = np.zeros(len(sizes))
occupied_probability = linspace(0.4, 1.0, no_probabilities)

for l, L in enumerate(sizes):
    print("xs=%f L=%f" % (xs, L))
    percolation_probability = np.zeros(no_probabilities)
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
                percolation_probability[j] += 1

    percolation_probability /= no_samples
    p_pis[l] = occupied_probability[np.argmax(percolation_probability > xs)]

plt.plot(sizes**(-1/nu), p_pis)
plt.title("Fill probability of percolation, x=0.3, nu=4/3")
plt.xlabel("System size L^(-1/nu)")
plt.ylabel("Fill probability p of percolation")
plt.savefig("p_pi.png")

cx, pc = linregress(sizes**(-1/nu), p_pis)[:2]
print(pc)

p = 0.58
pc = 0.59275
percolation_probability = np.zeros(len(sizes))

for l, L in enumerate(sizes):
    print("L=%f" % L)
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
            percolation_probability[l] += 1


percolation_probability /= no_samples
plt.plot((np.abs(p - pc))*sizes**(1/nu), percolation_probability)
plt.title("Scaling function phi(u)")
plt.xlabel("(p - p_c)L^(1/nu)")
plt.ylabel("Percolation probability")
plt.savefig("phi.png")
