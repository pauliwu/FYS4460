from ovito import dataset
from ovito.io import import_file
from ovito.modifiers import CoordinationNumberModifier
import numpy
import sys

temp = float(sys.argv[1])

# Load a particle dataset, apply modifier, and evaluate data pipeline.
node = import_file("dumps/dump.temp_%.4f" % temp)
for frame in range(dataset.anim.first_frame, dataset.anim.last_frame+1, 10):
    dataset.anim.current_frame = frame
    
    modifier = CoordinationNumberModifier(cutoff = 15.0, number_of_bins = 200)
    node.modifiers.append(modifier)
    node.compute()
    
    # Export the computed RDF data to a text file.
    numpy.savetxt("data/radial.temp_%.4f_frame_%d" % (temp, frame), modifier.rdf)
