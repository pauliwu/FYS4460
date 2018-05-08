from ovito import dataset
from ovito.io import import_file
from ovito.modifiers import ComputePropertyModifier
from ovito.modifiers import HistogramModifier
import numpy as np
import matplotlib.pyplot as plt

pipeline = import_file("dump.lammpstrj", multiple_frames=True)

center = [16.8, 16.8]
bin_min, bin_max = [0.0, 5.0]
no_bins = 50
bin_size = abs(bin_max - bin_min)/no_bins

radialModifier = \
    ComputePropertyModifier(
            output_property="RadialDistance",
            expressions=["sqrt( (Position.X - %f)^2 + (Position.Y - %f)^2)" % (center[0], center[1])]
            )
pipeline.modifiers.append(radialModifier)

radialBinModifier = \
    ComputePropertyModifier(
            output_property="RadialBin",
            expressions=["rint(RadialDistance/%f)" % bin_size]
            )
pipeline.modifiers.append(radialBinModifier)

for frame in range(dataset.anim.first_frame, dataset.anim.last_frame):
    time_averaged_velocity = np.zeros(no_bins)
    if(frame >= 200):
        data = pipeline.compute(frame)
        radial_bins = data.particle_properties['RadialBin']
        velocity_z = data.particle_properties['Velocity'][:,2]

        avg_velocity = np.zeros(no_bins)
        count = np.zeros(no_bins)
        for i in range(len(radial_bins)):
            bin_i = int(radial_bins[i])
            avg_velocity[bin_i] += velocity_z[i]
            count[bin_i] += 1
        mask = np.nonzero(count)
        avg_velocity[mask] /= count[mask]

        time_averaged_velocity += avg_velocity

time_averaged_velocity /= 49
plt.plot(np.linspace(0.0, 5.0, no_bins), time_averaged_velocity)
plt.show()
