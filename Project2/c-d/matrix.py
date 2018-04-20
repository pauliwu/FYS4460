import numpy as np
from lammps import lammps

def create_matrix(lmpptr):
    lmp = lammps(ptr=lmpptr)

    boxlo, boxhi, xy, yz, xz, periodicity, box_change = lmp.extract_box()
    xmin, ymin, zmin = boxlo
    xmax, ymax, zmax = boxhi

    no_spheres = 20
    xpos = np.random.uniform(xmin, xmax, no_spheres)
    ypos = np.random.uniform(ymin, ymax, no_spheres)
    zpos = np.random.uniform(zmin, zmax, no_spheres)
    radius = np.random.uniform(2.0, 3.0, no_spheres)

    for i in range(no_spheres):
        x = xpos[i]
        y = ypos[i]
        z = zpos[i]
        r = radius[i]
        lmp.commands_list([
            'region cut sphere %f %f %f %f units box' %
                (x, y, z, r),
            'group spheres region cut',
            'region cut delete'])
