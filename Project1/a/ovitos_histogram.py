from ovito import dataset
from ovito.io import import_file
from ovito.modifiers import HistogramModifier
import numpy as np
import matplotlib.pyplot as plt

pipeline = import_file("dump.lammpstrj", multiple_frames=True)

myHistogramModifier = HistogramModifier(
    property="Velocity.x",
    bin_count=200,
    fix_xrange=True,
    xrange_start=-10,
    xrange_end=10)
pipeline.modifiers.append(myHistogramModifier)

# get histogram in last frame
pipeline.compute(dataset.anim.last_frame)
histogram_final = myHistogramModifier.histogram[:,1]
normalization_factor = (histogram_final*histogram_final).sum()

# calculate normalized inner product
inner_prod = np.zeros(dataset.anim.last_frame)
for frame in range(dataset.anim.first_frame, dataset.anim.last_frame):
    pipeline.compute(frame)
    histogram = myHistogramModifier.histogram[:,1]
    inner_prod[frame] = (histogram*histogram_final).sum()
    if(frame % 200 == 0):
        plt.plot(np.linspace(-10, 10, len(histogram)), histogram/histogram.sum(), label="t=%d" % (frame*10))
plt.legend()
plt.xlabel('Velocity.X')
plt.ylabel('PDF')
plt.savefig('plots/histogram.png')
plt.clf()

inner_prod /= normalization_factor
plt.plot([i*10 for i in range(dataset.anim.last_frame)], inner_prod)
plt.xlabel('Timestep')
plt.ylabel('Normalized inner product')
plt.savefig('plots/inner_product.png')
plt.clf()
