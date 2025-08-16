"""
add_hydrogens_to_carbon.py, Geoffrey Weal, 17/2/22

This script allows the user to easily add hydrogens to carbon atoms in your molecule model. 
"""
import numpy as np
from ase import Atom
from SUMELF import get_unit_vector, rotate_vector_around_axis, get_distance

def add_hydrogens_to_carbon(molecule, molecule_graph, carbon_index):
	"""
	This method will add hydrogens to your carbons to make them sp3.

	Parameters
	----------
	molecule : ase.Atoms
		This is the molecule you want to centre as close to the middle of the unit cell as possible.
	molecule_graph : networkx.Graph
		This is the graph of this molecule.
	carbon_index : int
		This is the index of the carbon in your molecule that you want to add hydrogens to.
	"""

	# First, determine how many neighbours your carbon atom is bonded to.
	neighbouring_indices = list(molecule_graph[carbon_index])
	no_of_neighbouring_atoms = len(neighbouring_indices)
	if not (1 <= no_of_neighbouring_atoms <= 4):
		print('Error in def add_hydrogens_to_carbon, in modify_aliphatic_sidegroups.py')
		print('The number of atoms neighbouring carbon (index: '+str(carbon_index)+') is '+str(no_of_neighbouring_atoms))
		print('This should be between 1 and 4')
		print('Check this out')
		import pdb; pdb.set_trace()
		exit('This program with finish without completing')

	# Second, hydrogen will be added to the end of the molecule, so any future additions of hydrogens 
	# to other carbons should not affect those carbons carbon_index
	
	# 2.1: Add the first hydrogen if it doesnt exist. 
	if no_of_neighbouring_atoms == 1:
		add_hydrogen_to_carbon_with_1_neighbour(molecule, molecule_graph, carbon_index, neighbouring_indices)
		neighbouring_indices = list(molecule_graph[carbon_index])
		no_of_neighbouring_atoms = len(neighbouring_indices)

	# 2.2: Add the second hydrogen if it doesnt exist.
	if no_of_neighbouring_atoms == 2:
		add_hydrogen_to_carbon_with_2_neighbour(molecule, molecule_graph, carbon_index, neighbouring_indices)
		neighbouring_indices = list(molecule_graph[carbon_index])
		no_of_neighbouring_atoms = len(neighbouring_indices)

	# 2.3: Add the third hydrogen if it doesnt exist.
	if no_of_neighbouring_atoms == 3:
		add_hydrogen_to_carbon_with_3_neighbour(molecule, molecule_graph, carbon_index, neighbouring_indices)
		neighbouring_indices = list(molecule_graph[carbon_index])
		no_of_neighbouring_atoms = len(neighbouring_indices)

# ----------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------

C_to_H_bond_length = 0.97 # Å
H_C_H_bond_angle = np.radians(109.5)
def add_hydrogen_to_carbon_with_1_neighbour(molecule, molecule_graph, carbon_index, neighbouring_indices):
	"""
	This method will add a hydrogen to a carbon tha currently only has one neighbour.

	Parameters
	----------
	molecule : ase.Atoms
		This is the molecule you want to centre as close to the middle of the unit cell as possible.
	molecule_graph : networkx.Graph
		This is the graph of this molecule.
	carbon_index : int
		This is the index of the carbon in your molecule that you want to add hydrogens to.
	neighbouring_indices : list
		This is a list containing all the indices of the neighbours bound to this carbon atom.

	Attributes
	----------
	C_to_H_bond_length : float
		This is the C to H bond distance for binding new hydrogens to carbon atoms.
	H_C_H_bond_angle : float
		This is the diangle between H-C-H if a sp3 carbon currently has only 1 or two bonds about it.
	"""

	# First, get the index of the neighbouring atom. This will be a carbon atom in a benzene ring.
	n_atom_index = neighbouring_indices[0]

	# Second, get another carbon that is in the benzene ring. Have chosen for this carbon to be closest to the centre of mass.
	centre_of_mass = molecule.get_center_of_mass()
	nn_index = None
	smallest_distance_from_CM = float('inf')
	for nn_index_temp in molecule_graph[n_atom_index]:
		if molecule[nn_index_temp].symbol in ['C','N','O','S']:
			distance_from_CM = get_distance(molecule[nn_index_temp].position,centre_of_mass)
			if distance_from_CM < smallest_distance_from_CM:
				smallest_distance_from_CM = distance_from_CM
				nn_index = nn_index_temp
	if nn_index is None:
		print('Error in def add_hydrogen_to_carbon_with_1_neighbour, in modify_aliphatic_sidegroups.py')
		print('Could not find a neighbouring atom to the neighbouring carbon atom that was not a C, N, O, or S atom')
		print('Neighbouring Carbon index: '+str(n_atom_index))
		print("Neighbouring Carbon's neighbours indices: '+str(molecule_graph[n_atom_index])")
		print('The molecule will now appear in the ASE GUI')
		from ase.visualize import view
		view(molecule)
		print('Check this out')
		import pdb; pdb.set_trace()
		exit('This program with finish without completing')

	# Third, make the carbon to add a hydrogen to the origin.
	centre_point = molecule[carbon_index].position

	# Fourth, get the normal vector of the plane that the benzene ring lies in.
	unit_vector_1 = get_unit_vector(molecule[n_atom_index].position - centre_point)
	unit_vector_2 = get_unit_vector(molecule[nn_index].position     - centre_point)
	normal_unit_vector = get_unit_vector(np.cross(unit_vector_1,unit_vector_2))
	
	# Fifth, rotate unit_vector_1 in the plane with normal normal_unit_vector by an angle of H_C_H_bond_angle
	rotated_unit_vector_1 = rotate_vector_around_axis(unit_vector_1, H_C_H_bond_angle, normal_unit_vector)
	hydrogen_position_1   = centre_point + C_to_H_bond_length*rotated_unit_vector_1
	rotated_unit_vector_2 = rotate_vector_around_axis(unit_vector_1, -H_C_H_bond_angle, normal_unit_vector)
	hydrogen_position_2   = centre_point + C_to_H_bond_length*rotated_unit_vector_2
	
	# Sixth, select the rotation that will add a hydrogen to a point closest to the molecules centre of mass.
	hydrogen_position = hydrogen_position_1 if (get_distance(hydrogen_position_1,centre_point) < get_distance(hydrogen_position_2,centre_point)) else hydrogen_position_2

	# Seventh, add the hydrogen to the molecule.
	add_hydrogen_to_molecule(molecule, molecule_graph, hydrogen_position, carbon_index)

# ----------------------------------------------------------------------------------------------------------------------------------

def add_hydrogen_to_carbon_with_2_neighbour(molecule, molecule_graph, carbon_index, neighbouring_indices):
	"""
	This method will add a hydrogen to a carbon tha currently only has two neighbour.

	Parameters
	----------
	molecule : ase.Atoms
		This is the molecule you want to centre as close to the middle of the unit cell as possible.
	molecule_graph : networkx.Graph
		This is the graph of this molecule.
	carbon_index : int
		This is the index of the carbon in your molecule that you want to add hydrogens to.
	neighbouring_indices : list
		This is a list containing all the indices of the neighbours bound to this carbon atom.

	Attributes
	----------
	C_to_H_bond_length : float
		This is the C to H bond distance for binding new hydrogens to carbon atoms.
	"""
	
	# First, get the index of the neighbouring atoms. We will set the C to index1 and the H to index2.
	neighbouring_atom_index1, neighbouring_atom_index2 = neighbouring_indices if molecule[neighbouring_indices[0]].symbol == 'C' else neighbouring_indices[::-1]

	# Second, make the carbon to add a hydrogen to the origin.
	centre_point = molecule[carbon_index].position

	# Third, get the unit vectors that point from your carbon atom to each of its neighbours. 
	position_1 = molecule[neighbouring_atom_index1].position
	position_2 = molecule[neighbouring_atom_index2].position
	unit_vector_1 = get_unit_vector(position_1 - centre_point)
	unit_vector_2 = get_unit_vector(position_2 - centre_point)

	# Fourth, we will rotate the non-benzene related bond vector about line_to_rotate_about by 120 degrees. 
	# This will give us the new position for the bond to add our next hydrogen to.
	line_to_rotate_about = -unit_vector_1
	rotated_unit_vector_2 = rotate_vector_around_axis(unit_vector_2, np.radians(120), line_to_rotate_about)

	# Fifth, add the hydrogen to the molecule
	hydrogen_position = centre_point + C_to_H_bond_length*rotated_unit_vector_2
	add_hydrogen_to_molecule(molecule, molecule_graph, hydrogen_position, carbon_index)

# ----------------------------------------------------------------------------------------------------------------------------------

def add_hydrogen_to_carbon_with_3_neighbour(molecule, molecule_graph, carbon_index, neighbouring_indices):
	"""
	This method will add a hydrogen to a carbon tha currently only has three neighbour.

	Parameters
	----------
	molecule : ase.Atoms
		This is the molecule you want to centre as close to the middle of the unit cell as possible.
	molecule_graph : networkx.Graph
		This is the graph of this molecule.
	carbon_index : int
		This is the index of the carbon in your molecule that you want to add hydrogens to.
	neighbouring_indices : list
		This is a list containing all the indices of the neighbours bound to this carbon atom.

	Attributes
	----------
	C_to_H_bond_length : float
		This is the C to H bond distance for binding new hydrogens to carbon atoms.
	"""

	# First, get the index of the neighbouring atoms. 
	neighbouring_atom_index1, neighbouring_atom_index2, neighbouring_atom_index3 = neighbouring_indices

	# Second, make the carbon to add a hydrogen to the origin.
	centre_point = molecule[carbon_index].position

	# Third, get each of the unit vectors from the carbon atom to each of it's neighbours
	unit_vector_1 = get_unit_vector(molecule[neighbouring_atom_index1].position - centre_point)
	unit_vector_2 = get_unit_vector(molecule[neighbouring_atom_index2].position - centre_point)
	unit_vector_3 = get_unit_vector(molecule[neighbouring_atom_index3].position - centre_point)

	# Fourth, get the unit vector to plane the next hydrogen as the negative of the sum of each unit vector.
	bond_unit_vector = -get_unit_vector(unit_vector_1 + unit_vector_2 + unit_vector_3)

	# Fifth, add the hydrogen to the molecule
	hydrogen_position = centre_point + C_to_H_bond_length*bond_unit_vector
	add_hydrogen_to_molecule(molecule, molecule_graph, hydrogen_position, carbon_index)

# ----------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------

def add_hydrogen_to_molecule(molecule, molecule_graph, position, carbon_index):
	"""
	This method will add a hydrogen to your molecule

	Parameters
	----------
	molecule : ase.Atoms
		This is the molecule you want to centre as close to the middle of the unit cell as possible.
	molecule_graph : networkx.Graph
		This is the graph of this molecule.
	position : np.array
		This is the position that you want to place your hydrogen at in.
	carbon_index : int
		This is the index of the carbon in your molecule that you want to add hydrogens to.
	"""
	# First, make the hydrogen atom.
	hydrogen_atom = Atom(symbol='H',position=position)

	# Second, add the hydrogen atom to your molecule.
	molecule.append(hydrogen_atom)

	# Third, add the hydrogen atom to the molecule's graph.
	hydrogen_index = len(molecule)-1
	molecule_graph.add_node(hydrogen_index, E=molecule[hydrogen_index].symbol) # molecule[hydrogen_index].symbol should be a H
	molecule_graph.add_edge(carbon_index,hydrogen_index)

# ----------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------




