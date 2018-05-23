from ovito import dataset
from ovito.io import import_file
from ovito.modifiers import ComputePropertyModifier
from ovito.modifiers import HistogramModifier
import numpy as np
import matplotlib.pyplot as plt
import sys

pipeline = import_file(sys.argv[1], multiple_frames=True)

average_velocity = 0
for frame in range(dataset.anim.first_frame+1, dataset.anim.last_frame+1):
    if(frame >= 500):
        data = pipeline.compute(frame-1)
        velocity_z = data.particle_properties['Velocity'][:,2]
        average_velocity += np.average(velocity_z)

average_velocity /= 1500
number_of_particles = pipeline.source.number_of_particles
np.savetxt(sys.argv[2], np.array([average_velocity, number_of_particles]))
