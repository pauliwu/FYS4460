import numpy as np
from lammps import lammps

def create_matrix(lmpptr):
    lmp = lammps(ptr=lmpptr)

    boxlo, boxhi, xy, yz, xz, periodicity, box_change = lmp.extract_box()
    no_spheres = 20
    pos = np.random.uniform(boxlo, boxhi, [no_spheres, 3])
    radius = np.random.uniform(2.0, 3.0, no_spheres)

    for i in range(no_spheres):
        dims = pos[i]
        r = radius[i]
        create_sphere(lmpptr, dims, r)
        for i in range(len(dims)):
            if dims[i] + r > boxhi[i]:
                dims[i] -= boxhi[i] - boxlo[i]
                create_sphere(lmpptr, dims, r)
            elif dims[i] - r < boxlo[i]:
                dims[i] += boxhi[i] - boxlo[i]
                create_sphere(lmpptr, dims, r)

def create_sphere(lmpptr, dims, r):
    lmp = lammps(ptr=lmpptr)
    lmp.commands_list([
        'region cut sphere %f %f %f %f units box' %
            (dims[0], dims[1], dims[2], r),
        'group spheres region cut',
        'region cut delete'])
