import numpy as np
from ovito.data import *

def modify(frame, input, output):
	N = input.number_of_particles
	forces = input.particle_properties['Force'].array
	positions = input.particle_properties['Position'].array
	dot_prod = 0
	for i in range(N):
		for j in range(i, N):
			dot_prod += forces[i].dot(positions[i])
	print(dot_prod)