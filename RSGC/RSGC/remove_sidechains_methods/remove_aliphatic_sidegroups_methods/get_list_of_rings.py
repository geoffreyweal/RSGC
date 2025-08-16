"""
get_list_of_rings.py, Geoffrey Weal, 9/6/22

This script is designed to get all the atoms in rings that are less than or equal to 7.
"""
import warnings

from copy import deepcopy

from RSGC.RSGC.Hydrogen_in_Ring_Exception import Hydrogen_in_Ring_Exception
from RSGC.RSGC.remove_sidechains_methods.remove_aliphatic_sidegroups_methods.general_methods import is_list_in_another_list_of_lists_sorted

def get_list_of_rings(molecule, molecule_graph, filepath):
	"""
	Get a list of all the atoms in rings that are less than or equal to 7.

	Parameters
	----------
	molecule : ase.Atoms
		This is the molecule.
	molecule_graph : networkx.Graph
		This is the graph of this molecule.

	Returns
	-------
	rings_in_molecule : list of list of ints
		This is the list of atoms that are inolved in rings
	"""

	# First, create the rings_in_molecule list to store rings
	rings_in_molecule = [] 

	# Second, look through the entire molecule for rings, beginning from each atom in the molecule.
	for atom_index in range(len(molecule)):
		traverse_rings_method(atom_index, molecule, molecule_graph, [], rings_in_molecule)

	# Third, warnthe user if their are hydrogens in the rings found in the given crystal. 
	hydrogen_in_ring_error_checking(rings_in_molecule, molecule, molecule_graph, filepath)
	
	# Fourth, return all the rings in the molecule. The order of the ring list is in order of the atoms to following to follow the ring around
	return rings_in_molecule

def traverse_rings_method(atom_index, molecule, molecule_graph, currently_travelled_path, rings_in_molecule):
	"""
	This is a recursive method for finding rings that are 7 atoms long or less. 

	Method being performed is a Depth-First Search (DFS) algorithm.

	Parameters
	----------
	atom_index : int
		This is the atom index to explore from.
	molecule : ase.Atoms
		This is the molecule.
	molecule_graph : networkx.Graph
		This is the graph of this molecule.
	currently_travelled_path : list
		This is the list of ints that has currently been followed
	rings_in_molecule : list
		This is the list of rings found in the molecule. Rings found with the recursive algorithm will be stored in this list.
	"""

	# First, add the atom_index to the currently_travelled_path list
	currently_travelled_path.append(atom_index)

	# Second, look at each nieghbour to atom_index and determine how to traverse next about the molecule, if you have found a ring, or if you have reached the max traversal length we want to travel.
	for next_atom_index in molecule_graph[atom_index]:

		if (next_atom_index == currently_travelled_path[0]) and (len(currently_travelled_path) > 2):
			# 2.1: We have found a ring.
			if not is_list_in_another_list_of_lists_sorted(currently_travelled_path, rings_in_molecule):
				# 2.1.1: If currently_travelled_path is not already in rings_in_molecule, add currently_travelled_path to the rings_in_molecule list
				rings_in_molecule.append(deepcopy(currently_travelled_path))

		elif next_atom_index in currently_travelled_path: 
			# 2.2: We have already looked at next_atom_index in this path, so we dont want to traverse the path from here anymore.
			pass

		elif len(currently_travelled_path) == 7:
			# 2.3: We have already traverse through 7 atoms in this path, so we dont want to traverse the path from here anymore.
			pass
			
		else:
			# 2.4: We want to continue to traverse through the molecule, continuing from next_atom_index. 
			traverse_rings_method(next_atom_index, molecule, molecule_graph, deepcopy(currently_travelled_path), rings_in_molecule)

def hydrogen_in_ring_error_checking(rings_in_molecule, molecule, molecule_graph, filepath):
	"""
	This method is designed to check if a ring contains a hydrogen, and if so warn the user in a txt file. 

	Parameters
	----------
	rings_in_molecule : list
		This is the list of rings found in the molecule. Rings found with the recursive algorithm will be stored in this list.
	molecule : ase.Atoms
		This is the molecule.
	molecule_graph : networkx.Graph
		This is the graph of this molecule.
	filepath : str.
		This is the path to the crystal file.
	"""
	for flat_ring in rings_in_molecule:
		hydrogen_found = False
		for atom_index in flat_ring:
			if molecule[atom_index].symbol in ['H', 'D']:
				if any((molecule[neighbour_index].symbol in ['O', 'N']) for neighbour_index in molecule_graph[atom_index]):
					with open('Rings_with_hydrogens_in_them.txt','a+') as fileTXT:
						fileTXT.write(str(filepath)+' (Ring may have hydrogen bonding in it.)\n')
				else:
					with open('Rings_with_hydrogens_in_them.txt','a+') as fileTXT:
						fileTXT.write(str(filepath)+'\n')
					raise Hydrogen_in_Ring_Exception('Hydrogen Found in Ring, this is weird, check out this crystal manually.')
				hydrogen_found = True
				break
		if hydrogen_found:
			break



