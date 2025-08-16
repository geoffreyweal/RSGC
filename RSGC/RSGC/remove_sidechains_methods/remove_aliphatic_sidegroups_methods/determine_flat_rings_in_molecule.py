"""
determine_flat_rings_in_molecule.py, Geoffrey Weal, 9/6/22

This script is designed to determine which rings are flattish in the molecule. 
"""

tolerance_angle = 20.0 
def determine_flat_rings_in_molecule(rings_in_molecule, molecule):
	"""
	This method will determine which rings are flattish in the molecule. 

	This method is used to determine if a ring is probably conjugated.

	Parameters
	----------
	rings_in_molecule : list of lists of ints
		This is a list of ints in rings in the molecule.
	molecule : ase.Atoms
		This is the molecule you want to remove the aliphatic carbons to.

	Returns
	-------
	flat_rings_in_molecule : list of lists of ints
		This is a list of ints in rings that are flat. 
	"""

	# First, set up a variable for recording flat rings in the molecule.
	flat_rings_in_molecule = []

	# Second, check each ring to see if it is flat or not.
	for ring in rings_in_molecule:

		# 2.1: Do a simple check and see if the angles add up to the flat shape (within tolerance).

		# 2.1.1: What should the total internal angle be for a ring to be flat
		total_internal_angle_for_flat_moiety = (len(ring) - 2.0) * 180.0

		# 2.1.2: What is the total angle between atoms in the ring
		total_angle = 0.0
		for index1, index2, index3 in zip(ring, ring[1::]+ring[:1:], ring[2::]+ring[:2:]): 
			total_angle += molecule.get_angle(index1, index2, index3, mic=True)

		# 2.1.3: Is the ring within tolerance of being flat
		if (total_internal_angle_for_flat_moiety - tolerance_angle) <= total_angle <= (total_internal_angle_for_flat_moiety + tolerance_angle):
			flat_rings_in_molecule.append(ring)

	# Third, return the flat rings
	return flat_rings_in_molecule



