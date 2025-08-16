"""
add_hydrogens_to_sp3_carbons_method.py, Geoffrey Weal, 7/8/22

This script will add hydrogens to a list of carbon atoms given so they are sp3 (i.e. have four atoms surrounding them).
"""
from copy import deepcopy

from RSGC.RSGC.remove_sidechains_methods.remove_aliphatic_sidegroups_methods.get_sp3_carbons         import get_sp3_carbons
from RSGC.RSGC.remove_sidechains_methods.remove_aliphatic_sidegroups_methods.add_hydrogens_to_carbon import add_hydrogens_to_carbon

def add_hydrogens_to_sp3_carbons_method(molecule, molecule_graph):
	"""
	This method will add hydrogens to a list of carbon atoms given so they are sp3 (i.e. have four atoms surrounding them).

	Parameters
	----------
	molecule : ase.Atoms
		This is the molecule you to add hydrogens to.
	molecule_graph : networkx.Graph
		This is the graph associated with molecule.

	Returns
	-------
	molecule_copy : ase.Atoms
		This is the molecule with added hydrogens.
	molecule_graph_copy : networkx.Graph
		This is the graph associated with molecule_copy		
	"""

	# First, obtain all the indices of the aliphatic carbons in the molecule (that are sp3). 
	aliphatic_carbon_indices = get_sp3_carbons(molecule, molecule_graph)
	import pdb; pdb.set_trace()

	# Second, make a copy of the molecule and it's associated graph.
	molecule_copy = molecule.copy()
	molecule_graph_copy = deepcopy(molecule_graph)

	# Third, add hydrogens to each carbon that is sp3 so that it contains the correct number of bonds for sp3 carbons (4 neighbours). 
	for carbon_index in aliphatic_carbon_indices:
		add_hydrogens_to_carbon(molecule_copy, molecule_graph_copy, carbon_index)

	# Fourth, return molecule_copy and molecule_graph_copy
	return molecule_copy, molecule_graph_copy
