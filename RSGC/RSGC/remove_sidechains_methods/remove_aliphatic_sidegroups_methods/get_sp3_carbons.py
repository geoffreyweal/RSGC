"""
get_sp3_atoms.py, Geoffrey Weal, 19/2/22

This script is designed to modify the aliphatic sidegroups of your OPV molecule. 
"""

def get_sp3_carbons(molecule, molecule_graph):
	"""
	This method will determine which carbons are likely to be sp3.

	Parameters
	----------
	molecule : ase.Atoms
		This is the molecule.
	molecule_graph : networkx.Graph
		This is the graph of this molecule.

	Returns
	-------
	aliphatic_carbon_indices : list
		This is a list of the atoms that are likely sp3 carbons.
	"""
	aliphatic_carbon_indices = []
	for index in range(len(molecule)):
		if molecule[index].symbol == 'C' and is_sp3(molecule, molecule_graph, index):
			aliphatic_carbon_indices.append(index)
	return aliphatic_carbon_indices


def is_sp3(molecule, molecule_graph, index):
	"""
	This method will determine which carbons are likely to be sp3.

	Parameters
	----------
	molecule : ase.Atoms
		This is the molecule.
	molecule_graph : networkx.Graph
		This is the graph of this molecule.
	index : int
		This is the index of the atom you want to determine if it is sp3. 

	Returns
	-------
	True if the atom is sp3. False if the atom is not sp3
	"""

	# First, get the indices of the neighbours
	neighbour_indices = list(molecule_graph[index])

	# Second, depending on the number of neighbours
	if len(neighbour_indices) == 4:

		# If their are four neighbours around the atom, return True
		return True

	elif len(neighbour_indices) >= 2:

		# If their are two neighbours around the atom:
		# We assume here that an sp3 carbon is one where all the angles between neighbouring atoms are less than ~115.0 degrees in angle

		# Get the angles between the central atom and other neighbouring atoms.
		angles = []
		for i1 in range(len(neighbour_indices)):
			neighbour_index_1 = neighbour_indices[i1]
			for i2 in range(i1+1,len(neighbour_indices)):
				neighbour_index_2 = neighbour_indices[i2]
				angle = molecule.get_angle(neighbour_index_1, index, neighbour_index_2, mic=False)
				angles.append(angle)

		# If all angles are less than 115.0 degrees, we assume the atom is sp3
		if all([angle < 115.0 for angle in angles]):
			return True

	elif len(neighbour_indices) == 1: 

		# If the carbon is only attached to one other atom, it is assumed that the X-ray was not able to pick up the other three hydrogens.
		# Will check the bond length to see if it is the length of a single bond, or if it is short enough to indicate a double or triple bond.

		neighbour_index_1 = neighbour_indices[0]
		bond_length = molecule.get_distance(index,neighbour_index_1)
		if bond_length >= 1.3: #A
			return True

	# Third, if none of the above options could be found, the atom is not sp3.
	return False



