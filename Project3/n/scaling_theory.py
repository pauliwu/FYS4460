from pylab import *
from scipy.ndimage import measurements
from tqdm import tqdm

no_samples = 1000
no_probabilities = 100
nu = 4/3

p_xs = np.linspace(0.3, 0.8, 11)
sizes = np.array([25, 50, 100, 200, 400, 800])
p_pis = np.zeros((len(p_xs), len(sizes)))
occupied_probability = linspace(0.4, 1.0, no_probabilities)

for k, xs in enumerate(p_xs):
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
        p_pis[k][l] = occupied_probability[np.argmax(percolation_probability > xs)]
    
    plt.plot(sizes**(-1/nu), p_pis[k], label="x=%f" % xs)
plt.legend()
plt.title("Fill probability of percolation, nu=4/3")
plt.xlabel("System size L**(-1/nu)")
plt.ylabel("Fill probability p of percolation")
plt.savefig("p_pi.png")
