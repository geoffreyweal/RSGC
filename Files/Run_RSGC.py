"""
Run_RSGC.py, Geoffrey Weal, 12/4/24

This script will allow you to run the Remove SideGroups from Crystals (RSGC) program upon the crystals of interest. 
"""
import os, shutil
from RSGC import RSGC, Hydrogen_in_Ring_Exception

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# PART I: Get the names of the folders holding the crystals you want to remove sidegroups from

# First, give the name of the folder that contains the crystal database you want to remove sidegroups from here. 
crystal_database_dirname = 'crystal_database'

# Second, give the name of the folder that contains repaired crystals obtained from the ReCrystals program.
repaired_crystal_database_dirname = None # f'repaired_{crystal_database_dirname}'

# Third, give the identifiers of the crystals you do not want to remove sidegroups from but may be in the databases here
exclude_identifiers  = ['ECIGUV']
exclude_identifiers += ['XEZCOX', 'XEZDAK']

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Part II: Determine settings for running the RSGC program.

# Fourth, Determine if you want any saturated aliphatic groups to be replaced with
#         * Ethyl group (set this to True), or
#         * Methyl group (set this to False). 
leave_as_ethyls = True

# Fifth, determine if you also want to save the molecules from the crystals individually, 
#        as well as save the full crystal.
save_molecules_individually = True

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Part III: Check that the folders of the databases exist.

# Sixth, check that the crystal database you gave exists. 
if not os.path.exists(crystal_database_dirname):
    raise Exception(f'Error: {crystal_database_dirname} does not exist in {os.getcwd()}')

# Seventh, check that the crystal database holding reparred crystals you gave exists.
if (repaired_crystal_database_dirname is not None) and (not os.path.exists(repaired_crystal_database_dirname)):
    raise Exception(f'Error: {crystal_database_dirname} does not exist in {os.getcwd()}')

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Part VI: Get the paths to the crystals you want to remove sidegroups from.

# Eighth, get the names of the files contained in the crystal database folder.
crystal_database_filenames = sorted(os.listdir(crystal_database_dirname))

# Ninth, get the names of the files contained in the repaired crystal database folder.
repaired_crystal_database_filenames = sorted(os.listdir(repaired_crystal_database_dirname)) if (repaired_crystal_database_dirname is not None) else []

# Tenth, initalise the list to hold all the paths to the crystals to remove sidegroups from.
filepath_names = []

# Eleventh, obtain all the paths to the crystals to remove sidegroups from.
for crystal_database_filename in crystal_database_filenames:

    # 11.1: Make sure that the file ends with ".xyz""
    if not crystal_database_filename.endswith('.xyz'):
        continue

    # 11.2: Get the name of the identifier for this crystal. 
    crystal_identifier = crystal_database_filename.replace('.xyz','')

    # 11.3: If the crystal is in the exclude_identifiers list, don't process it.
    if crystal_identifier in exclude_identifiers:
        continue

    # 11.4: Check if the crystal is in the repaired crystal database folder. 
    #        * If it is, take the crystal from the repaired folder rather than the original folder. 
    crystal_folder_name = repaired_crystal_database_dirname if (crystal_database_filename in repaired_crystal_database_filenames) else crystal_database_dirname

    # 11.5: Add the path to the crystal file to the filepath_names list.
    filepath_names.append(crystal_folder_name+'/'+crystal_database_filename)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# PART V: Reset RSGC files from previous RSGC runs

# Twelfth, reset the RSGC files.  

# 12.1: Remove the folder that we will place crystals in that we will remove sidegroups from.
crystal_database_with_removed_sidegroups_folder_name = f'{crystal_database_dirname}_with_removed_sidegroups'
if os.path.exists(crystal_database_with_removed_sidegroups_folder_name):
    shutil.rmtree(crystal_database_with_removed_sidegroups_folder_name)

# 12.2: Remove the file indicating what issues were found when running the RSGC program. 
if os.path.exists('RSGC_issues.txt'):
    os.remove('RSGC_issues.txt')

# 12.3: Remove the file containing which rings contain hydrogens in them when running the RSGC program. 
if os.path.exists('Rings_with_hydrogens_in_them.txt'):
    os.remove('Rings_with_hydrogens_in_them.txt')

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# PART VI: Run the RSGC program on the crystals you want to remove sidegroups from

# Thirteenth, run the RSGC program on the crystals you want to remove sidegroups from

# 13.1: Obtain the total number of crystal you want to process with the RSGC program. 
total_no_of_crystals = str(len(filepath_names))

# 13.2: Set a counter to record successful RSGC executions.
successful = 0

# 13.3: For each crystal in the filepath_names list. 
for counter, filepath in enumerate(filepath_names, start=0):

    # 13.4: Print to screen how many crystals have been processed by the RSGC program. 
    print('Running crystal: '+str(counter)+' out of '+total_no_of_crystals)

    # 13.5: Run the RSGC program. 
    try:

        # 13.5.1: Run the RSGC program. 
        RSGC(filepath, leave_as_ethyls=leave_as_ethyls, save_molecules_individually=save_molecules_individually)

        # 13.5.2: Record the successful result. 
        successful += 1

    except Hydrogen_in_Ring_Exception as exception_message:

        # 13.5.3: If there was an issue with the RSGC program, write the issue in the 'RSGC_issues.txt' file
        with open('RSGC_issues.txt','a+') as issuesTXT:
            issuesTXT.write(filepath+': '+str(exception_message)+'\n')

# 13.6: Report the number of successful executions.
print('========================')
print('Number of successfuls: '+str(successful))

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -