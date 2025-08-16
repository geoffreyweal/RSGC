"""
remove_atoms_from_molecule.py, Geoffrey Weal, 19/2/22

This script is designed to remove the given atoms from the molecule and the graph associated with the molecule.
"""
from copy     import deepcopy
from networkx import relabel_nodes
from SUMELF   import get_unit_vector

def remove_atoms_from_molecule(molecule, molecule_graph, atoms_to_delete_indices, atoms_to_turn_into_hydrogens, remove_non_H_leaf_atoms=True, return_new_branch_indices=True):
	"""
	This method will remove the given atoms from the molecule and the graph associated with the molecule.

	Parameters
	----------
	molecule : ase.Atoms
		This is the molecule you want to remove atoms from
	molecule_graph : networkx.Graph
		This is the graph of this molecule.
	atoms_to_delete_indices : list of int
		This is the list of indices for the atoms you want to remove from the molecule.
	atoms_to_turn_into_hydrogens : list of (int, int)
		This is the list of indices to be turned into hydrogen atoms (if they are not already hydrogen atoms).
	remove_non_H_leaf_atoms : bool.
		Remove atoms that are attached to ends of the saturate aliphatic chains that are non hydrogens. Default: True.
	return_new_branch_indices : bool.
		Return a list of the branch atom indices. Default: True.

	Returns
	-------
	molecule : ase.Atoms
		This is the molecule with atoms given in the final_atoms_to_delete_indices list removed
	molecule_graph : networkx.Graph
		This is the modified graph of this molecule.
	new_alpha_atoms_indices : list of int
		This is the list of alpha atoms in this molecules which has has some of its atoms removed.
	"""

	# First, get all the atom indices to remove. Include non-hydrogen atoms attached to leaf atoms (that are not alpha atoms) if remove_non_H_leaf_atoms == True
	if remove_non_H_leaf_atoms:
		final_atoms_to_delete_indices = sorted(set(deepcopy(atoms_to_delete_indices) + [outer_index for outer_index, inner_index in sorted(atoms_to_turn_into_hydrogens) if (not molecule[outer_index].symbol in ['H', 'D', 'T'])]))
	else:
		final_atoms_to_delete_indices = deepcopy(sorted(set(atoms_to_delete_indices)))

	# Second, get the original indices of atoms in the molecules before atoms were deleted.
	original_atom_indices = list(range(len(molecule)))

	# Third, remove all atoms involved in the aliphatic side chains.
	for index in sorted(final_atoms_to_delete_indices, reverse=True):
		del molecule[index]
		del original_atom_indices[index]

	# Fourth, modify the molecule_graph so that is properly reflect this now modified molecule with the aliphatic side chains removed.
	molecule_graph.remove_nodes_from(final_atoms_to_delete_indices)
	mapping = {original_index: new_index for new_index, original_index in enumerate(original_atom_indices)}
	molecule_graph = relabel_nodes(molecule_graph, mapping)

	# Fifth, check if leaf atoms are hydrogens. 
	#        * If they are not, turn them into hydrogen atoms with appropriate bond length to the alpha atom.
	if not remove_non_H_leaf_atoms:
		for outer_index, inner_index in sorted(atoms_to_turn_into_hydrogens, reverse=True):
			new_inner_index = mapping[inner_index]
			new_outer_index = mapping[outer_index]
			if not (molecule[new_outer_index].symbol in ['H', 'D', 'T']):
				position = readjust_for_hydrogen(molecule, new_outer_index, new_inner_index)
				molecule[new_outer_index].symbol = 'H' 
				molecule[new_outer_index].position = position

	# Sixth, get the indices of the atoms at the end of branches for this molecule.
	branch_atoms_indices = sorted(set([mapping[inner_index] for outer_index, inner_index in atoms_to_turn_into_hydrogens]))

	# Seventh, return the updated molecules and molecule_graph without sidegroups.
	if return_new_branch_indices:
		return molecule, molecule_graph, branch_atoms_indices
	else:
		return molecule, molecule_graph

atom_to_H_bond_length = 0.97 # Å
def readjust_for_hydrogen(molecule, beta_index, alpha_index):
	"""
	This method will place the beta atom in a position for the beta atom to be turned into a hydrogen atom.

	Parameters
	----------
	molecule : ase.Atoms
		This is the molecule you want to remove atoms from.
	beta_index : int
		This is the index of the beta atom that will be changed to a hydrogen atom.
	alpha_index : int
		This is the index of the alpha atom that is attached to the beta atom. 

	Returns
	-------
	position : numpy.array
		This is the position to place the beta atom in so that is has the right lengths for a H atom from the alpha atom.
	"""

	# First, get the positions of the alpha and beta atoms
	alpha_point = molecule[alpha_index].position
	beta_point  = molecule[beta_index].position

	# Second, get the unit vector for the direction from the alpha atom to the beta atom.
	unit_vector = get_unit_vector(beta_point - alpha_point)

	# Third, this is the new position to place the beta position in so it has the right length for an atom bonded to a hydrogen atom. 
	new_beta_point = atom_to_H_bond_length*unit_vector + alpha_point

	# Fourth, return the new position for the beta atom.
	return new_beta_point


