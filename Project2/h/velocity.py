from ovito import dataset
from ovito.io import import_file
from ovito.modifiers import ComputePropertyModifier
from ovito.modifiers import HistogramModifier
import numpy as np
import matplotlib.pyplot as plt

pipeline = import_file("dump.lammpstrj", multiple_frames=True)

center = [16.8, 16.8]
bin_min, bin_max = [0.0, 5.0]
no_bins = 20
bins = np.linspace(bin_min, bin_max, no_bins)

radialModifier = \
    ComputePropertyModifier(
            output_property="RadialDistance",
            expressions=["sqrt( (Position.X - %f)^2 + (Position.Y - %f)^2)" % (center[0], center[1])]
            )
pipeline.modifiers.append(radialModifier)

time_averaged_velocity = np.zeros(no_bins)
for frame in range(dataset.anim.first_frame, dataset.anim.last_frame):
    if(frame >= 999):
        data = pipeline.compute(frame)
        radii = data.particle_properties['RadialDistance']
        velocity_z = data.particle_properties['Velocity'][:,2]

        inds = np.digitize(radii, bins, right=True) - 1
        avg_velocity = np.zeros(no_bins)
        count = np.zeros(no_bins)

        for i in range(len(radii)):
            avg_velocity[inds[i]] += velocity_z[i]
            count[inds[i]] += 1
        mask = np.nonzero(avg_velocity)
        avg_velocity[mask] /= count[mask]
        
        time_averaged_velocity += avg_velocity

plt.plot(bins, time_averaged_velocity)
plt.show()
