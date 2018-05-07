import numpy as np
from lammps import lammps

def create_matrix(lmpptr):
    lmp = lammps(ptr=lmpptr)

    boxlo, boxhi, xy, yz, xz, periodicity, box_change = lmp.extract_box()
    no_spheres = 20
    pos = np.random.uniform(boxlo, boxhi, [no_spheres, 3])
    radius = np.random.uniform(2.0, 3.0, no_spheres)

    regionnumber = 1
    regionlist = ""
    for i in range(no_spheres):
        dims = pos[i]
        r = radius[i]
        regionlist += "cut%d " % regionnumber
        create_sphere(lmpptr, dims, r, regionnumber)
        regionnumber += 1
        for j in range(len(dims)):
            if dims[j] + r > boxhi[j]:
                dims[j] -= boxhi[j] - boxlo[j]
                regionlist += "cut%d " % regionnumber
                create_sphere(lmpptr, dims, r, regionnumber)
                regionnumber += 1
            elif dims[j] - r < boxlo[j]:
                dims[j] += boxhi[j] - boxlo[j]
                regionlist += "cut%d " % regionnumber
                create_sphere(lmpptr, dims, r, regionnumber)
                regionnumber += 1
    lmp.command('region notspheres union %d ' % (regionnumber-1) + regionlist + " side out")

def create_sphere(lmpptr, dims, r, regionnumber):
    lmp = lammps(ptr=lmpptr)
    region = "cut%d" % regionnumber
    lmp.commands_list([
        'region %s sphere %f %f %f %f units box' %
            (region, dims[0], dims[1], dims[2], r),
        'group spheres region %s' % region])
