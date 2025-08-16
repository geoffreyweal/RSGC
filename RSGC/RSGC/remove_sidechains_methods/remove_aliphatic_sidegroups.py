"""
general_methods.py, Geoffrey Weal, 19/2/22

This script is designed to modify the aliphatic sidegroups of your OPV molecule. 
"""
from copy import deepcopy

from RSGC.RSGC.remove_sidechains_methods.remove_aliphatic_sidegroups_methods.get_list_of_rings                        import get_list_of_rings
from RSGC.RSGC.remove_sidechains_methods.remove_aliphatic_sidegroups_methods.determine_flat_rings_in_molecule         import determine_flat_rings_in_molecule
from RSGC.RSGC.remove_sidechains_methods.remove_aliphatic_sidegroups_methods.get_sp3_carbons                          import get_sp3_carbons
from RSGC.RSGC.remove_sidechains_methods.remove_aliphatic_sidegroups_methods.determine_atoms_between_moieties_to_keep import determine_atoms_between_moieties_to_keep
from RSGC.RSGC.remove_sidechains_methods.remove_aliphatic_sidegroups_methods.get_alpha_beta_and_gamma_atoms           import get_alpha_beta_and_gamma_atoms
from RSGC.RSGC.remove_sidechains_methods.remove_aliphatic_sidegroups_methods.remove_atoms_from_molecule               import remove_atoms_from_molecule
from RSGC.RSGC.remove_sidechains_methods.remove_aliphatic_sidegroups_methods.add_hydrogens_to_alpha_carbons_method    import add_hydrogens_to_alpha_carbons_method

def remove_aliphatic_sidegroups(original_molecule, original_molecule_graph, filepath, leave_as_ethyls=False):
	"""
	This method will remove all the aliphatic carbon sidechains from the OPV. 
	Only the alpha carbon will be kept from the aliphatic sidegroup. 

	Parameters
	----------
	molecule : ase.Atoms
		This is the molecule you want to remove the aliphatic carbons to.
	molecule_graph : networkx.Graph
		This is the graph of this molecule.
	filepath : str.
		This is the path to the crystal file of interest.
	leave_as_ethyls : bool.
		If False, all sidegroups will be left as methyl. If true, they will be given as ethyl (to their beta carbon). 

	Returns
	-------
	molecule : ase.Atoms
		This is the molecule with aliphatic carbons removed
	molecule_graph : networkx.Graph
		This is the modified graph of this molecule.
	"""

	# Preliminary Step: make a copy of molecule, molecule_graph
	molecule       = original_molecule.copy()
	molecule_graph = deepcopy(original_molecule_graph)

	# First, obtains all the rings that are 7 atoms or less in size in the molecule.
	rings_in_molecule = get_list_of_rings(molecule, molecule_graph, filepath)

	# Second, determine which rings are flat(ish). This will indicate if they are conjugated rings or not.
	flat_rings_in_molecule = determine_flat_rings_in_molecule(rings_in_molecule, molecule)

	# Third, get all atoms that are not hydrogens or carbons.
	non_hydrogen_and_carbon_atoms = [index for index in range(len(molecule)) if (molecule[index].symbol not in ['H', 'D', 'T', 'C'])]

	# Fourth, determine other non-sp3 moieties in the molecules.
	sp3_carbons = get_sp3_carbons(molecule, molecule_graph)
	non_sp3_carbons = [index for index in range(len(molecule)) if ((molecule[index].symbol == 'C') and (index not in sp3_carbons))]

	# Fifth, determine all the atoms in the molecule that should be kept.
	all_atom_of_moieties_to_keep = tuple(set([j for sub in rings_in_molecule for j in sub] + non_hydrogen_and_carbon_atoms + non_sp3_carbons))

	# Sixth, determine all the unique paths between the rings in your molecule
	atoms_in_any_ring, atoms_between_rings = determine_atoms_between_moieties_to_keep(molecule, molecule_graph, all_atom_of_moieties_to_keep)

	# Seventh, determine which atoms in the molecule are involved in branches
	atoms_in_rings_and_between_rings = tuple(sorted(set(atoms_in_any_ring + atoms_between_rings)))
	atoms_in_branches = tuple(sorted(set(range(len(molecule))) - set(atoms_in_rings_and_between_rings)))

	# Eighth, determine the alpha atoms. These are the atoms in atoms_in_branches are directly attached to a ring atom or a atom between rings.
	alpha_atoms, beta_atoms, gamma_atoms, beta_alpha_atoms, gamma_beta_atoms = get_alpha_beta_and_gamma_atoms(atoms_in_branches, atoms_in_rings_and_between_rings, molecule_graph)

	# Ninth, determine branch atoms to remove from the molecules
	if leave_as_ethyls:
		check_branches_have_atoms(atoms_in_branches, alpha_atoms + beta_atoms + gamma_atoms)
		atoms_to_remove = sorted(set(atoms_in_branches) - set(alpha_atoms) - set(beta_atoms) - set(gamma_atoms))
		atoms_to_turn_into_hydrogens = gamma_beta_atoms
	else:
		check_branches_have_atoms(atoms_in_branches, alpha_atoms + beta_atoms)
		atoms_to_remove = sorted(set(atoms_in_branches) - set(alpha_atoms) - set(beta_atoms))
		atoms_to_turn_into_hydrogens = beta_alpha_atoms

	# Tenth, remove the branch atoms from the molecule. Hydrogens will be added in-place of any side-chains that have been removed by this method
	molecule, molecule_graph, branch_atoms_indices = remove_atoms_from_molecule(molecule, molecule_graph, atoms_to_remove, atoms_to_turn_into_hydrogens, remove_non_H_leaf_atoms=False, return_new_branch_indices=True)

	# Eleventh, add any missing hydrogens to sp3 carbons. Not all sp3 carbons may have all the required number of hydrogens bound to them due to Xray crystallography issues with sp3 carbons. 
	# molecule, molecule_graph = add_hydrogens_to_alpha_carbons_method(molecule, molecule_graph, new_alpha_atoms_indices)

	# Eleventh, return the molecule without the side chains, and the molecule graph that is associated to this main component of the molecule
	return molecule, molecule_graph

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def check_branches_have_atoms(original_atoms_in_branches, atoms_to_check_are_in_the_branches):
	"""
	This method is designed to check if the atoms in atoms_to_check_are_in_the_branches are in atoms_in_branches

	Parameters
	----------
	original_atoms_in_branches : list
		This list contain all the atoms in the branch
	atoms_to_check_are_in_the_branches : list
		This list contains a set of indices that we expect to be in original_atoms_in_branches
	"""

	# First, make a copy of atoms_in_branches
	atoms_in_branches = sorted(set(deepcopy(original_atoms_in_branches)))

	# Second, initialise a list to contain all the indices in atoms_to_check_are_in_the_branches that were not found in original_atoms_in_branches.
	problematic_indices = []

	# Third, checck that the indices in atoms_to_check_are_in_the_branches are in atoms_in_branches.
	for atom_index in set(atoms_to_check_are_in_the_branches):

		# 3.1: If atom_index is not in atoms_in_branches, there is a problem, so record this index.
		if atom_index not in atoms_in_branches:

			# 3.2: atom_index was not found in atoms_in_branches, so record it in problematic_indices.
			problematic_indices.append(atom_index)

	# Fourth, if there are indices in problematic_indices, report them as an Exception:
	if len(problematic_indices) > 0:
		to_string  = 'Error: Some of the index expected in atoms_in_branches were not found.\n'
		to_string += f'Indices not found in atoms_in_branches: {problematic_indices}\n'
		to_string += f'atoms_in_branches: {atoms_in_branches}\n'
		to_string += 'Check this'
		raise Exception(to_string)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 



