"""
add_hydrogens_to_alpha_carbons_method.py, Geoffrey Weal, 19/2/22

This script is designed to add hydrogens to your alpha carbon atoms
"""
from copy import deepcopy
from RSGC.RSGC.remove_sidechains_methods.remove_aliphatic_sidegroups_methods.add_hydrogens_to_carbon import add_hydrogens_to_carbon

def add_hydrogens_to_alpha_carbons_method(molecule, molecule_graph, alpha_indices):
	"""
	This script is designed to add hydrogens to your alpha carbon atoms.

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
	
	# First, make a copy of the molecule and it's associated graph.
	molecule_copy = molecule.copy()
	molecule_graph_copy = deepcopy(molecule_graph)

	# Second, add hydrogens to each carbon that is sp3 so that it contains the correct number of bonds for sp3 carbons (4 neighbours). 
	for index in alpha_indices:
		if molecule[index].symbol == 'C':
			add_hydrogens_to_carbon(molecule_copy, molecule_graph_copy, index)

	# Third, return molecule_copy and molecule_graph_copy
	return molecule_copy, molecule_graph_copy

