"""
remove_sidechains.py, Geoffrey Weal, 20/5/2022

This program will remove aliphatic sidechains from the main molecule.
"""
import os
import traceback
import numpy as np
from copy import deepcopy

from tqdm import tqdm

from ase import Atoms
from ase.io import read, write
from ase.visualize import view

from SUMELF import get_distance
from SUMELF import obtain_graph, process_crystal
from SUMELF import make_crystal
from SUMELF import remove_folder, make_folder

from RSGC.RSGC.remove_sidechains_methods.remove_aliphatic_sidegroups import remove_aliphatic_sidegroups
from SUMELF                                                          import add_graph_to_ASE_Atoms_object

def RSGC(filepath, save_crystal_folderpath='crystals_with_sidechains_removed', make_molecule_method='component_assembly_approach', leave_as_ethyls=False, save_molecules_individually=False, wrap=False, debug=False):
	"""
	This method is designed to to remove aliphatic sidechains from your molecules in the crystal file.

	Parameters
	----------
	filepath : str.
		This is the path to the crystal file.
	save_crystal_folderpath : str.
		This is the folder path to save the crystal with sidegroups removed into. 
	make_molecule_method : str.
		This is the name of the method you want to use to create the molecule. See https://github.com/geoffreyweal/ECCP for more information. Default: 'component_assembly_approach'. 
	leave_as_ethyls : bool.
		If False, all sidegroups will be left as methyl. If true, they will be given as ethyl (to their beta carbon). 
	save_molecules_individually : bool.
		This tag indicates if you also want to save the molecules in the crystal individual. Default: False. 
	wrap : bool.
		If true, wrap the molecule in the unit cell. If false, keep the molecule in its connected form.
	debug : bool.
		This tag indicates if the user wants debugging information and files to be provided by this program.
	"""

	# Preamble before beginning program
	no_of_char_in_divides = 70
	divide_string = '.'+'#'*no_of_char_in_divides+'.'
	print(divide_string)
	print(divide_string)
	print(divide_string)
	print('Looking at: '+str(filepath))
	print(divide_string)
	filepath_without_ext = '.'.join(filepath.split('.')[:-1])
	filename = os.path.basename(filepath)

	if filepath.endswith('.cif'):
		crystal = read(filepath) #,disorder_groups='remove_disorder')
	else:
		crystal = read(filepath)
	crystal.set_pbc(True)

	# Second, get the graph of the crystal.
	crystal, crystal_graph = obtain_graph(crystal,name='crystal')

	# Third, get the molecules and the graphs associated with each molecule in the crystal.
	molecules, molecule_graphs, SolventsList, symmetry_operations, cell = process_crystal(crystal,crystal_graph=crystal_graph,take_shortest_distance=True,return_list=False,logger=None)
	
	# Fourth, determine the solvents in the crystal
	solvent_components = list(make_SolventsList(crystal.info['SolventsList'])) if ('SolventsList' in crystal.info) else []

	# Fifth, check to make sure the molecules are all good.
	molecules, molecule_graphs, solvent_components = check_molecules(molecules, molecule_graphs, solvent_components)

	# Sixth, initialise the dictionary and lists to store updated information on.
	updated_molecules       = {}
	updated_molecule_graphs = {}

	# Seventh, remove the aliphatic sidegroup from molecules that are not solvents. Also get the list of molecules that are solvents. 
	print('Removing aliphatic sidechains from non-solvent molecules.')
	pbar = tqdm(sorted(molecules.keys()), unit='molecules')
	for molecule_name in pbar:

		# 7.1: Obtain the molecule and its associated graph.
		molecule       = molecules[molecule_name].copy()
		molecule_graph = deepcopy(molecule_graphs[molecule_name])

		# 7.2: Do not process molecule if it is a solvent. 
		#      * Keep in updated_molecules, but leave unchanged.
		if molecule_name in solvent_components:
			updated_molecules[molecule_name]       = molecule
			updated_molecule_graphs[molecule_name] = molecule_graph
			continue

		# 7.3: Remove the aliphatic sidechains from this molecule. 
		updated_molecule, updated_molecule_graph = remove_aliphatic_sidegroups(molecule, molecule_graph, filepath, leave_as_ethyls=leave_as_ethyls)

		# 7.4: Update the molecules and molecule_graphs with updated_molecule and updated_molecule_graph for molecule_name
		updated_molecules[molecule_name]       = updated_molecule
		updated_molecule_graphs[molecule_name] = updated_molecule_graph

	# Eighth, check to make sure the updated molecules are all good.
	updated_molecules, updated_molecule_graphs, solvent_components = check_molecules(updated_molecules, updated_molecule_graphs, solvent_components, original_molecules=molecules)

	# Ninth, create the crystal without aliphatic sidechains.
	new_crystal, new_crystal_graph = make_crystal(updated_molecules, symmetry_operations=symmetry_operations, cell=cell, wrap=False, solvent_components=solvent_components, remove_solvent=False, molecule_graphs=updated_molecule_graphs)

	# Tenth, check that no more atoms were added to the crystal, as only atoms should have been removed (and hydrogens added in their place)
	if len(new_crystal) > len(crystal):
		raise Exception('Error: The crystal contains more atoms after sidechains were removed than the original crystal. This should happen. Check your crystal file.')

	# Eleventh, wrap the atoms in the crystal so that all atoms are found inside the unit cell.
	if wrap:
		new_crystal.wrap()

	# Twelfth, add the node and edge properties of the crystal from the crystal_graph into the crystal ASE object itself. 
	add_graph_to_ASE_Atoms_object(new_crystal, new_crystal_graph)

	# Thirteenth, make the folder to place the editted crystal in if it doesnt currently exist.
	make_folder(save_crystal_folderpath)

	# Fourteenth, save the edited crystal file that excludes aliphatic sidechains from the crystal.
	crystal_name = filepath_without_ext.split('/')[-1]
	write(save_crystal_folderpath+'/'+crystal_name+'_with_sidechains_removed.xyz', new_crystal)

	# Fifteenth, if save_molecules_individually is set to True, save the individual molecules
	if save_molecules_individually:

		# 15.1: Add the node and edge information from the molecules graph back to the molecule
		for molecule_name in updated_molecules.keys():
			add_graph_to_ASE_Atoms_object(updated_molecules[molecule_name], updated_molecule_graphs[molecule_name])

		# 15.2: Create the folder to store molecule xyz data to.
		make_folder(save_crystal_folderpath+'_molecules'+'/'+crystal_name)

		# 15.3: Save each molecule from the crystal to disk
		for molecule_name, updated_molecule in updated_molecules.items():
			solvent_tag = 'S' if molecule_name in solvent_components else ''
			write(save_crystal_folderpath+'_molecules'+'/'+crystal_name+'/'+str(molecule_name)+str(solvent_tag)+'.xyz', updated_molecule)

	print(divide_string)

# -----------------------------------------------------------------------------------------------------------------------------

def check_molecules(molecules, molecule_graphs, solvent_components, original_molecules=None):
	"""
	This method is designed to check the molecules are all good.

	Parameters
	----------
	molecules : dict. of ase.Atoms
		This is the dict. of molecules in the crystal
	molecule_graphs : dict. of networkx.Graph 
		This is the dict that contains the graph of each molecule in the molecules dictionary. 
	solvent_components : list of int.
		This list contains the indices of all the solvents in the molecules list. 
	original_molecules : dict. of ase.Atoms or None
		These are the dict. of molecules that was obtained from the original molecules before removing aliphatic sidechains. If set to None, molecules are molecules from the unmodified crystal. Default: None.
	"""

	# First, record all the molecules that have problems with them.
	problematic_molecule_names = []

	# Second, for each molecule in the molecules dictionary.
	for mol_name, molecule in molecules.items():

		# Third, if their are no atoms in the molecule, record it as a problem.
		if len(molecule) == 0:
			problematic_molecule_names.append(mol_name)

	# Fourth, sort the problematic_molecule_names list
	problematic_molecule_names.sort()

	# Fifth, report the issue to the user if there are problematic molecules, and ask the user if they want to continue otherwise. 
	if len(problematic_molecule_names) > 0:

		# 5.1: Print error message.
		traceback_stack = traceback.extract_stack()
		print('Error: These is an issue at:')
		for trace in traceback_stack:
			print(f'  {trace.filename}, line {trace.lineno} in {trace.name}')#: {trace.line}')
		print('Molecules '+str([prob_mol_name for prob_mol_name in problematic_molecule_names])+' in the crystal have no atoms in it?')
		print("Look at the GUI's to see the problem")
		print('One or more GUIs show all the problematic molecules before and after the RSGC has been applied to it')
		print('The other GUI shows all the OK molecules')

		# 5.2: For each problematic molecule
		for problematic_molecule_name in problematic_molecule_names:

			# 5.2.1: Create a list that contains the problematic molecule.
			problem_molecule = [molecules[problematic_molecule_name]]

			# 5.2.2: If original_molecules is not none, add the original molecule to the list to compare molecule with.
			if original_molecules is not None:
				problem_molecule.append(original_molecules[problematic_molecule_name])

			# 5.2.3: Open the GUI to allow the user to see the problematic molecule (and its original version if given).
			view(problem_molecule)

		# 5.3: Show all the ok molecules
		view([molecules[prob_mol_name] for prob_mol_name in molecules.keys() if (prob_mol_name not in problematic_molecule_names)])

		# 5.4: Check with the user if they want to continue anyway.
		while True:
			to_continue = input('Would you like to continue without these problematic molecules in the crystal? (y/N): ')
			to_continue = to_continue.lower()
			if to_continue in ['y', 'yes']:
				break
			elif to_continue in ['n', 'no']:
				exit('Program will exit without completing.')
			print('Please type either yes (y) or no (n).')

		# 5.5: Mark the problematic molecules as None objects. 
		for prob_mol_name in problematic_molecule_names:
			molecules[prob_mol_name] = None
			molecule_graphs[prob_mol_name] = None

		# 5.6: Update molecules, molecule_graphs, and solvent_components to remove molecules with no atoms
		molecules, molecule_graphs, solvent_components = remove_None_placeholders(molecules, molecule_graphs, solvent_components)

	# Sixth, return the molecules and molecule_graphs objects
	return molecules, molecule_graphs, solvent_components

def remove_None_placeholders(molecules, molecule_graphs, solvent_components):
	"""
	This method is designed to remove any None objects from the molecules, molecule_graphs, and solvent_components dictionaries and lists.

	Parameters
	----------
	molecules : dict. of ase.Atoms
		This is the dict. of molecules in the crystal
	molecule_graphs : dict. of networkx.Graph 
		This is the dict that contains the graph of each molecule in the molecules dictionary. 
	solvent_components : list of int.
		This list contains the indices of all the solvents in the molecules list. 

	Returns
	-------
	molecules : dict. of ase.Atoms
		This is the dict. of molecules in the crystal
	molecule_graphs : dict. of networkx.Graph 
		This is the dict that contains the graph of each molecule in the molecules dictionary. 
	solvent_components : list of int.
		This list contains the indices of all the solvents in the molecules list. 
	"""

	# First, check if there are any None objects in the molecules list.
	None_object_names = []
	for mol_name in sorted(molecules.keys(), reverse=False):
		if molecules[mol_name] is None:
			None_object_names.append(mol_name)

	# Second, if there are values in None_object_names, there are None objects to remove, so do that
	if len(None_object_names) > 0:

		# 2.1: Remove all None objects from molecules and molecule_graphs, and their respective indices from solvent_components
		for None_object_name in None_object_names:
			del molecules[None_object_name]
			del molecule_graphs[None_object_name]
			if None_object_name in solvent_components:
				solvent_components.remove(None_object_name)

		# 2.2: Place all remaining molecules and molecule_graphs objects together, as well as a boolean to indicate if it is a solvent.
		all_data = []
		for mol_name in sorted(molecules.keys(), reverse=False):
			molecule       = molecules[mol_name]
			molecule_graph = molecule_graphs[mol_name]
			is_solvent = mol_name in solvent_components
			all_data.append([mol_name, molecule, molecule_graph, is_solvent])

		# 2.3: Sort all_data by the mol_name.
		all_data.sort(key=lambda x:x[0], reverse=False)

		# 2.4: Decrement molecules by the approproriate amount
		for index, (old_mol_name, molecule, molecule_graph, is_solvent) in enumerate(all_data):

			# 2.4.1: Write the new name for this molecule.
			new_mol_name = index + 1

			# 2.4.2: Change the old_mol_name to new_mol_name for this datum set. 
			all_data[index][0] = new_mol_name

		# 2.4: Check that none of the molecules in all_data have the same name.
		if not len(all_data) == len(set([mol_name for mol_name, _, _, _ in all_data])):
			raise Exception('Error: Some molecules have the same indices after None objects have been removed from the all_data list. This is a programming error.')

		# 2.5: Construct new molecules and molecule_graphs dictionaries, as well as a new solvent_components list.
		molecules = {}; molecule_graphs = {}; solvent_components = []
		for mol_name, molecule, molecule_graph, is_solvent in all_data:
			molecules[mol_name]       = molecule
			molecule_graphs[mol_name] = molecule_graph
			if is_solvent:
				solvent_components.append(mol_name)

	# Third, return molecules, molecule_graphs, and solvent_components.
	return molecules, molecule_graphs, solvent_components

def make_SolventsList(SolventsList):
	"""
	This method is designed to require that SolventsList is a list, even if their is only one value in the list.

	Parameters
	----------
	SolventsList : list of ints, np.int64
		This is the SolventsList to convert to a list.

	Returns
	-------
	SolventsList : list of ints
		This is the SolventsList as a list.
	"""
	if isinstance(SolventsList,np.int64):
		return [int(SolventsList)]
	return SolventsList

# -----------------------------------------------------------------------------------------------------------------------------

