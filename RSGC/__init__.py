# The information about the Remove Sidechain Groups from Crystals (RSGC) Program

__name__    = 'RSGC (Remove Sidechain Groups from Crystals Program)'
__version__ = '0.5'
__author__  = 'Dr. Geoffrey Weal, Dr. Chayanit Wechwithayakhlung, Dr. Josh Sutton, Dr. Daniel Packwood, Dr. Paul Hume, Prof. Justin Hodgkiss'

import sys
from importlib.util import find_spec

if sys.version_info[0] == 2:
	toString = ''
	toString += '\n'
	toString += '================================================'+'\n'
	toString += 'This is the Remove Sidechain Groups from Crystals (RSGC) Program'+'\n'
	toString += 'Version: '+str(__version__)+'\n'
	toString += '\n'
	toString += 'The Remove Sidechain Groups from Crystals (RSGC) Program requires Python3. You are attempting to execute this program in Python2.'+'\n'
	toString += 'Make sure you are running the Remove Sidechain Groups from Crystals (RSGC) Program in Python3 and try again'+'\n'
	toString += 'This program will exit before beginning'+'\n'
	toString += '================================================'+'\n'
	raise ImportError(toString)
if sys.version_info[1] < 4:
	toString = ''
	toString += '\n'
	toString += '================================================'+'\n'
	toString += 'This is the Remove Sidechain Groups from Crystals (RSGC) Program'+'\n'
	toString += 'Version: '+str(__version__)+'\n'
	toString += '\n'
	toString += 'The Remove Sidechain Groups from Crystals (RSGC) Program requires Python 3.4 or greater.'+'\n'
	toString += 'You are using Python '+str('.'.join(sys.version_info))
	toString += '\n'
	toString += 'Use a version of Python 3 that is greater or equal to Python 3.4.\n'
	toString += 'This program will exit before beginning'+'\n'
	toString += '================================================'+'\n'
	raise ImportError(toString)

# ------------------------------------------------------------------------------------------------------------------------
# A check for ASE

ase_spec = find_spec("ase")
ase_found = (ase_spec is not None)
if not ase_found:
	toString = ''
	toString += '\n'
	toString += '================================================'+'\n'
	toString += 'This is the Remove Sidechain Groups from Crystals (RSGC) Program'+'\n'
	toString += 'Version: '+str(__version__)+'\n'
	toString += '\n'
	toString += 'The Remove Sidechain Groups from Crystals (RSGC) Program requires ASE.'+'\n'
	toString += '\n'
	toString += 'Install ASE through pip by following the instruction in https://github.com/GardenGroupUO/RSGC'+'\n'
	toString += 'These instructions will ask you to install ase by typing the following into your terminal\n'
	toString += 'pip3 install --user --upgrade ase\n'
	toString += '\n'
	toString += 'This program will exit before beginning'+'\n'
	toString += '================================================'+'\n'
	raise ImportError(toString)	

import ase
ase_version_minimum = '3.19.0'
from packaging import version
if version.parse(ase.__version__) < version.parse(ase_version_minimum):
	toString = ''
	toString += '\n'
	toString += '================================================'+'\n'
	toString += 'This is the Remove Sidechain Groups from Crystals (RSGC) Program'+'\n'
	toString += 'Version: '+str(__version__)+'\n'
	toString += '\n'
	toString += 'The Remove Sidechain Groups from Crystals (RSGC) Program requires ASE greater than or equal to '+str(ase_version_minimum)+'.'+'\n'
	toString += 'The current version of ASE you are using is '+str(ase.__version__)+'.'+'\n'
	toString += '\n'
	toString += 'Install ASE through pip by following the instruction in https://github.com/GardenGroupUO/RSGC'+'\n'
	toString += 'These instructions will ask you to install ase by typing the following into your terminal\n'
	toString += 'pip3 install --user --upgrade ase\n'
	toString += '\n'
	toString += 'This program will exit before beginning'+'\n'
	toString += '================================================'+'\n'
	raise ImportError(toString)

# ------------------------------------------------------------------------------------------------------------------------

scipy_spec = find_spec("scipy")
scipy_found = (scipy_spec is not None)
if not scipy_found:
	toString = ''
	toString += '\n'
	toString += '================================================'+'\n'
	toString += 'This is the Remove Sidechain Groups from Crystals (RSGC) Program'+'\n'
	toString += 'Version: '+str(__version__)+'\n'
	toString += '\n'
	toString += 'The Remove Sidechain Groups from Crystals (RSGC) Program requires the "scipy" program.'+'\n'
	toString += '\n'
	toString += 'Install scipy by typing the following into your terminal\n'
	toString += '\n'
	toString += 'pip3 install --user --upgrade scipy\n'
	toString += '\n'
	toString += 'This program will exit before beginning'+'\n'
	toString += '================================================'+'\n'
	raise ImportError(toString)	

# ------------------------------------------------------------------------------------------------------------------------

networkx_spec = find_spec("networkx")
networkx_found = (networkx_spec is not None)
if not networkx_found:
	toString = ''
	toString += '\n'
	toString += '================================================'+'\n'
	toString += 'This is the Remove Sidechain Groups from Crystals (RSGC) Program'+'\n'
	toString += 'Version: '+str(__version__)+'\n'
	toString += '\n'
	toString += 'The Remove Sidechain Groups from Crystals (RSGC) Program requires the "networkx" program.'+'\n'
	toString += '\n'
	toString += 'Install networkx through pip by following the instruction in https://github.com/GardenGroupUO/RSGC'+'\n'
	toString += 'These instructions will ask you to install networkx by typing the following into your terminal\n'
	toString += '\n'
	toString += 'pip3 install --user --upgrade networkx\n'
	toString += '\n'
	toString += 'This program will exit before beginning'+'\n'
	toString += '================================================'+'\n'
	raise ImportError(toString)	

# ------------------------------------------------------------------------------------------------------------------------

pymatgen_spec = find_spec("pymatgen")
pymatgen_found = (pymatgen_spec is not None)
if not pymatgen_found:
	toString = ''
	toString += '\n'
	toString += '================================================'+'\n'
	toString += 'This is the Remove Sidechain Groups from Crystals (RSGC) Program'+'\n'
	toString += 'Version: '+str(__version__)+'\n'
	toString += '\n'
	toString += 'The Remove Sidechain Groups from Crystals (RSGC) Program requires the "pymatgen" program.'+'\n'
	toString += '\n'
	toString += 'Install pymatgen through pip by following the instruction in https://github.com/GardenGroupUO/RSGC'+'\n'
	toString += 'These instructions will ask you to install pymatgen by typing the following into your terminal\n'
	toString += '\n'
	toString += 'pip3 install --user --upgrade pymatgen\n'
	toString += '\n'
	toString += 'This program will exit before beginning'+'\n'
	toString += '================================================'+'\n'
	raise ImportError(toString)	

# ------------------------------------------------------------------------------------------------------------------------

packaging_spec = find_spec("packaging")
packaging_found = (packaging_spec is not None)
if not packaging_found:
	toString = ''
	toString += '\n'
	toString += '================================================'+'\n'
	toString += 'This is the Remove Sidechain Groups from Crystals (RSGC) Program'+'\n'
	toString += 'Version: '+str(__version__)+'\n'
	toString += '\n'
	toString += 'The Remove Sidechain Groups from Crystals (RSGC) Program requires the "packaging" program.'+'\n'
	toString += '\n'
	toString += 'Install packaging through pip by following the instruction in https://github.com/GardenGroupUO/RSGC'+'\n'
	toString += 'These instructions will ask you to install packaging by typing the following into your terminal\n'
	toString += '\n'
	toString += 'pip3 install --user --upgrade packaging\n'
	toString += '\n'
	toString += 'This program will exit before beginning'+'\n'
	toString += '================================================'+'\n'
	raise ImportError(toString)	

# ------------------------------------------------------------------------------------------------------------------------

tqdm_spec = find_spec("tqdm")
tqdm_found = (tqdm_spec is not None)
if not tqdm_found:
	toString = ''
	toString += '\n'
	toString += '================================================'+'\n'
	toString += 'This is the Remove Sidechain Groups from Crystals (RSGC) Program'+'\n'
	toString += 'Version: '+str(__version__)+'\n'
	toString += '\n'
	toString += 'The Remove Sidechain Groups from Crystals (RSGC) Program requires the "tqdm" program.'+'\n'
	toString += '\n'
	toString += 'Install tqdm through pip by following the instruction in https://github.com/GardenGroupUO/RSGC'+'\n'
	toString += 'These instructions will ask you to install tqdm by typing the following into your terminal\n'
	toString += '\n'
	toString += 'pip3 install --user --upgrade tqdm\n'
	toString += '\n'
	toString += 'This program will exit before beginning'+'\n'
	toString += '================================================'+'\n'

# ------------------------------------------------------------------------------------------------------------------------

tqdm_spec = find_spec("xlsxwriter")
tqdm_found = (tqdm_spec is not None)
if not tqdm_found:
	toString = ''
	toString += '\n'
	toString += '================================================'+'\n'
	toString += 'This is the Remove Sidechain Groups from Crystals (RSGC) Program'+'\n'
	toString += 'Version: '+str(__version__)+'\n'
	toString += '\n'
	toString += 'The Remove Sidechain Groups from Crystals (RSGC) Program requires the "xlsxwriter" program.'+'\n'
	toString += '\n'
	toString += 'Install xlsxwriter through pip by following the instruction in https://github.com/GardenGroupUO/RSGC'+'\n'
	toString += 'These instructions will ask you to install xlsxwriter by typing the following into your terminal\n'
	toString += '\n'
	toString += 'pip3 install --user --upgrade xlsxwriter\n'
	toString += '\n'
	toString += 'This program will exit before beginning'+'\n'
	toString += '================================================'+'\n'

# ------------------------------------------------------------------------------------------------------------------------

mprof_spec = find_spec("memory_profiler")
mprof_found = (tqdm_spec is not None)
if not mprof_found:
	toString = ''
	toString += '\n'
	toString += '================================================'+'\n'
	toString += 'This is the Remove Sidechain Groups from Crystals (RSGC) Program'+'\n'
	toString += 'Version: '+str(__version__)+'\n'
	toString += '\n'
	toString += 'The Remove Sidechain Groups from Crystals (RSGC) Program requires the "memory_profiler" program.'+'\n'
	toString += '\n'
	toString += 'Install memory_profiler through pip by following the instruction in https://github.com/GardenGroupUO/RSGC'+'\n'
	toString += 'These instructions will ask you to install memory_profiler by typing the following into your terminal\n'
	toString += '\n'
	toString += 'pip3 install --user --upgrade memory_profiler\n'
	toString += '\n'
	toString += 'This program will exit before beginning'+'\n'
	toString += '================================================'+'\n'

# ------------------------------------------------------------------------------------------------------------------------

__author_email__ = 'geoffrey.weal@vuw.ac.nz'
__license__ = 'GNU AFFERO GENERAL PUBLIC LICENSE'
__url__ = 'https://github.com/geoffreyweal/RSGC'
__doc__ = 'See https://github.com/geoffreyweal/RSGC for the documentation on this program'

# ================================================================================================
from RSGC.RSGC.RSGC import RSGC
from RSGC.RSGC.Hydrogen_in_Ring_Exception import Hydrogen_in_Ring_Exception
# ================================================================================================

__all__ = [RSGC, Hydrogen_in_Ring_Exception]

# ------------------------------------------------------------------------------------------------------------------------




