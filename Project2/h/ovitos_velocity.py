from ovito import dataset
from ovito.io import import_file
from ovito.modifiers import ComputePropertyModifier
from ovito.modifiers import HistogramModifier
import numpy as np
import matplotlib.pyplot as plt

pipeline = import_file("dump.lammpstrj", multiple_frames=True)

b = 5.72
sigma = 3.405
bs = b/sigma
center = [10*bs, 10*bs]
bin_min, bin_max = [0.0*bs, 5.0*bs]
no_bins = 30
bins = np.sqrt(np.linspace(bin_min**2, bin_max**2, no_bins))

radialModifier = \
    ComputePropertyModifier(
            output_property="RadialDistance",
            expressions=["sqrt( (Position.X - %f)^2 + (Position.Y - %f)^2)" % (center[0], center[1])]
            )
pipeline.modifiers.append(radialModifier)

time_averaged_velocity = np.zeros(no_bins)
for frame in range(dataset.anim.first_frame+1, dataset.anim.last_frame+1):
    if(frame >= 500):
        data = pipeline.compute(frame-1)
        radii = data.particle_properties['RadialDistance']
        velocity_z = data.particle_properties['Velocity'][:,2]

        inds = np.digitize(radii, bins) - 1
        avg_velocity = np.zeros(no_bins)
        count = np.zeros(no_bins)

        for i in range(len(radii)):
            avg_velocity[inds[i]] += velocity_z[i]
            count[inds[i]] += 1
        mask = np.nonzero(avg_velocity)
        avg_velocity[mask] /= count[mask]
        
        time_averaged_velocity += avg_velocity

time_averaged_velocity /= 5500
np.savetxt("radial_velocity.csv", time_averaged_velocity)
