"""
determine_atoms_between_moieties_to_keep.py, Geoffrey Weal, 9/6/22

This script is designed to determine the atoms that are found between the atoms of moieties you want to keep, as well as the atoms that lead down paths without moieties you want to keep.
"""
from copy import deepcopy

from RSGC.RSGC.remove_sidechains_methods.remove_aliphatic_sidegroups_methods.general_methods import is_list_in_another_list_of_lists_sorted

def determine_atoms_between_moieties_to_keep(molecule, molecule_graph, all_atom_of_moieties_to_keep):
	"""
	This method is designed to determine the atoms that are found between the atoms of moieties you want to keep, as well as the atoms that lead down paths without moieties you want to keep.

	Parameters
	----------
	molecule : ase.Atoms
		This is the molecule.
	molecule_graph : networkx.Graph
		This is the graph of this molecule.
	all_atom_of_moieties_to_keep : list of ints
		These are the atoms of the moieties you want to keep.

	Returns
	-------
	atoms_between_moieties : list of ints
		This is a list that contains the atom indices found in branches that connect moieties to moieties.
	atoms_in_branch_paths : list of ints
		This is a list that contains all the atom indices found in branches that DO NOT connect moieties to moieties.
	"""

	# First, set up the lists to record paths found during all the depth-first searches.
	paths_from_moiety_to_moiety = []
	paths_from_moiety_to_ends_of_branch = []

	# Second, search for all the paths between moieties and from moieties to the ends of branches.
	for atom_index in all_atom_of_moieties_to_keep:
		# Perform the depth-first search for paths. 
		traverse_between_moieties_method(atom_index, molecule, molecule_graph, [], all_atom_of_moieties_to_keep, paths_from_moiety_to_moiety, paths_from_moiety_to_ends_of_branch)

	# Third, remove any moiety to moiety paths that are alternative routes from the same startpoint to the same endpoint but are longer.
	shortest_unique_paths_from_moiety_to_moiety = obtain_shortest_unique_paths_from_moiety_to_moiety(paths_from_moiety_to_moiety)

	# Fourth, obtain all the atoms that are involved in paths from moieties to the same or other different moieties.
	atoms_between_moieties = tuple(sorted(set([j for sub in shortest_unique_paths_from_moiety_to_moiety for j in sub]) - set(all_atom_of_moieties_to_keep)))

	# Fifth, do some checks.
	if not (len(all_atom_of_moieties_to_keep) == len(set(all_atom_of_moieties_to_keep))):
		raise Exception('Error in def determine_atoms_between_moieties, determine_atoms_between_moieties.py. Check out')
	if not (len(atoms_between_moieties) == len(set(atoms_between_moieties))):
		raise Exception('Error in def determine_atoms_between_moieties, determine_atoms_between_moieties.py. Check out')
	if not (len(set(all_atom_of_moieties_to_keep) & set(atoms_between_moieties)) == 0):
		raise Exception('Error in def determine_atoms_between_moieties, determine_atoms_between_moieties.py. Check out')

	# Sixth, return the atoms in the moieties, and atoms in the shortest unique paths between moieties.
	return all_atom_of_moieties_to_keep, atoms_between_moieties

# ===============================================================================================================================

def traverse_between_moieties_method(atom_index, molecule, molecule_graph, path_through_molecule, all_atom_of_moieties_to_keep, paths_from_moiety_to_moiety, paths_from_moiety_to_ends_of_branch):
	"""
	This is a recursive method for finding paths between moieties given in the moieties_in_molecule list (see determine_atoms_between_moieties method above).

	Method being performed is a Depth-First Search (DFS) algorithm.

	Parameters
	----------
	atom_index : int
		This is the atom index to explore from.
	molecule : ase.Atoms
		This is the molecule.
	molecule_graph : networkx.Graph
		This is the graph of this molecule.
	path_through_molecule : list
		This is the current path that has been travelled during this resursive algorithm
	all_atom_of_moieties_to_keep : tuple
		These are the atoms in 
	paths_from_moiety_to_moiety : list
		These are the paths found from moiety to moiety. Paths from moiety to moieties found with the recursive algorithm will be stored in this list.
	paths_from_moiety_to_ends_of_branch : list
		These are the paths found from moiety to the end of branches with no moieties. Paths from moiety to branch ends found with the recursive algorithm will be stored in this list.
	"""

	# First, add the current atom_index to the current path travelled, recorded in path_through_molecule
	path_through_molecule.append(atom_index)

	# Second, determine if we have found the end of a branch with no moiety
	for next_atom_index in molecule_graph[atom_index]:
		if next_atom_index not in path_through_molecule:
			# If here, there is a path that we can continue to travel on, so we are not at the end of a branch and can continue on our travel.
			break
	else:
		# If we are here, we can not travel forward on any new path. Therefore, we have reached the end of a branch without finding a moiety.
		if not is_list_in_another_list_of_lists_sorted(path_through_molecule, paths_from_moiety_to_ends_of_branch):
			# Only record new branches that have not been recorded yet to paths_from_moiety_to_ends_of_branch.
			paths_from_moiety_to_ends_of_branch.append(deepcopy(path_through_molecule))	
		return

	# Third, look at the neighbouring atoms and determine if you have found a moiety atom, the end of a branch, or you need to continue traversing down the path. 
	for next_atom_index in molecule_graph[atom_index]:

		if next_atom_index in all_atom_of_moieties_to_keep:
			# 3.1: We have found a moiety at the end of this path.
			completed_path = deepcopy(path_through_molecule) + [next_atom_index]
			if (completed_path[0] == completed_path[-1]) and (len(completed_path) <= 3):
				# This if statements check that the path has not moved one step forward and then one step backwards 
				pass
			elif not is_list_in_another_list_of_lists_sorted(completed_path, paths_from_moiety_to_moiety):
				# Only record new paths from one moiety to another moiety that has not been recorded yet. 
				paths_from_moiety_to_moiety.append(completed_path)

		elif next_atom_index in path_through_molecule: 
			# 3.2: We have already looked at next_atom_index in this path, so we dont want to traverse the path from here anymore.
			pass

		else:
			# 3.3: We want to continue to traverse through the molecule, continuing from next_atom_index. 
			traverse_between_moieties_method(next_atom_index, molecule, molecule_graph, deepcopy(path_through_molecule), all_atom_of_moieties_to_keep, paths_from_moiety_to_moiety, paths_from_moiety_to_ends_of_branch)

# ===============================================================================================================================

def obtain_shortest_unique_paths_from_moiety_to_moiety(original_paths_from_moiety_to_moiety):
	"""
	This method will determine which paths in the original_paths_from_moiety_to_moiety are the shortest unique paths. 

	Parameters
	----------
	original_paths_from_moiety_to_moiety : list of ints
		These are all the path that have been found from one moiety to the same moiety or a different moiety. 

	Returns
	-------
	shortest_unique_paths_from_moiety_to_moiety : list of ints
		These are all the unique paths in the original_paths_from_moiety_to_moiety that are shortest.
	"""

	# First, sort the paths_from_moiety_to_moiety list from shortest to longest path.
	paths_from_moiety_to_moiety = sorted(original_paths_from_moiety_to_moiety, key=lambda x: len(x))

	# Second, obtain the shortest unique paths from one moiety to the same moiety or a different moiety. 
	shortest_unique_paths_from_moiety_to_moiety = []
	for path in paths_from_moiety_to_moiety:
		for shortest_unique_path in shortest_unique_paths_from_moiety_to_moiety:
			# 2.1.1: Determine if path has a similar start and end as shortest_unique_path
			start_of_path = compare_lists(path, shortest_unique_path, compare='start')
			end_of_path   = compare_lists(path, shortest_unique_path, compare='end')
			if (len(start_of_path) > 0) and (len(end_of_path) > 0):
				# If path has a similar start and end to shortest_unique_path, 
				# then path is not the shortest unique path
				break
		else:
			# 2.2.1: If here, could not find a shortest unique path that starts with path[0] and ends with path[-1]. 
			# Add path to shortest_unique_paths_from_moiety_to_moiety
			shortest_unique_paths_from_moiety_to_moiety.append(path)

	# Third, return all the unique paths in the original_paths_from_moiety_to_moiety that are shortest.
	return shortest_unique_paths_from_moiety_to_moiety

def compare_lists(original_first_list, original_second_list, compare='start'):
	"""
	This method is designed to compare two lists together to see how much of the start and end of the list is the same.

	Parameters
	----------
	original_first_list : list of ints
		This is the first list to compare
	original_second_list : list of ints
		This is the second list to compare
	compare : str
		If compare='start', compare the starts of the two lists. If compare='end', compare the ends of the two lists.

	Returns
	-------
	same_entries_of_list : list of ints
		This is the start or the ends of the two lists that are the same.
	"""

	# First, determine if you want to compare the lists from the starts or ends.
	if compare == 'start':
		first_list  = original_first_list
		second_list = original_second_list
	elif compare == 'end':
		first_list  = original_first_list[::-1]
		second_list = original_second_list[::-1]

	# Second, determine how much of the start or end of the two lists are the same.
	same_entries_of_list = []
	for first_entry, second_entry in zip(first_list, second_list):
		if first_entry == second_entry:
			same_entries_of_list.append(first_entry)
		else:
			break

	# Third, if you are comparing the ends, reverse the same_entries_of_list list.
	if compare == 'end':
		same_entries_of_list = same_entries_of_list[::-1]

	# Fourth, return the same_entries_of_list list.
	return same_entries_of_list

# ===============================================================================================================================
