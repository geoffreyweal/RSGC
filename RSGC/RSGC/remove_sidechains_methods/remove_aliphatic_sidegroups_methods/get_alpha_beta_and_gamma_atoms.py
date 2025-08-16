"""
get_alpha_beta_and_gamma_atoms.py, Geoffrey Weal, 9/6/22

This script is designed to obtain the alpha, beta, and gamma atoms that are attached to atoms in rings or between rings.
"""
def get_alpha_beta_and_gamma_atoms(atoms_in_branches, atoms_in_rings_and_between_rings, molecule_graph):
	"""
	This script is designed to obtain the alpha, beta, and gamma atoms that are attached to atoms in rings or between rings.

	Parameters
	----------
	atoms_in_branches : tuple of ints
		These are the atoms that are in branches in the molecule.
	atoms_in_rings_and_between_rings : tuple of ints
		These are the atoms that are rings or between rings in the molecule.
	molecule_graph : networkx.Graph
		This is the graph of this molecule.

	Returns
	-------
	alpha_atoms : list of ints
		These are all the alpha atoms in the molecule (relative to the atoms in rings or atoms between rings).
	beta_atoms : list of ints
		These are all the beta atoms in the molecule (relative to the atoms in rings or atoms between rings).
	beta_alpha_atoms : list of ints
		These are all the beta atoms in the molecule and the alpha atoms they are bound to (relative to the atoms in rings or atoms between rings).
	"""

	# First, determine the alpha atoms. These are the atoms in atoms_in_branches are directly attached to a ring atom or a atom between rings.
	alpha_atoms = []
	for index_in_branch in atoms_in_branches:
		for neighbouring_index in molecule_graph[index_in_branch]:
			if neighbouring_index in atoms_in_rings_and_between_rings:
				alpha_atoms.append(index_in_branch)
	alpha_atoms = sorted(set(alpha_atoms))

	# Second, determine the beta atoms. These are atoms that are bound to the alpha atoms that are not in the atoms_in_rings_and_between_rings list.
	beta_atoms = []
	beta_alpha_atoms = []
	for alpha_index in alpha_atoms:
		for neighbouring_index in molecule_graph[alpha_index]: 
			if neighbouring_index in atoms_in_rings_and_between_rings:
				continue
			beta_atoms.append(neighbouring_index)
			beta_alpha_atoms.append((neighbouring_index, alpha_index))
	beta_atoms = sorted(set(beta_atoms))

	# Third, determine the gamma atoms. These are atoms that are bound to the gamma atoms that are not in the atoms_in_rings_and_between_rings list.
	gamma_atoms = []
	gamma_beta_atoms = []
	for beta_index in beta_atoms:
		for neighbouring_index in molecule_graph[beta_index]: 
			if neighbouring_index in atoms_in_rings_and_between_rings:
				continue
			if neighbouring_index in alpha_atoms:
				continue
			gamma_atoms.append(neighbouring_index)
			gamma_beta_atoms.append((neighbouring_index, beta_index))
	gamma_atoms = sorted(set(gamma_atoms))

	# Third, return the lists of alpha, beta, and gamma atoms.
	return alpha_atoms, beta_atoms, gamma_atoms, beta_alpha_atoms, gamma_beta_atoms