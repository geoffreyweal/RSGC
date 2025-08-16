"""
general_methods.py, Geoffrey Weal, 9/6/22

This script contains general methods for using in removing aliphatic sidechains methods.
"""
# --------------------------------------------------------------------------------------------------

def is_list_in_another_list_of_lists_sorted(main_list, list_of_lists_to_compare):
	"""
	This method is designed to compare a sorted list with a list of sorted lists. 

	Sorting of lists is done during comparisons.

	Parameters
	----------
	main_list : list of ints
		This is the main list that we want to see is in list_of_lists_to_compare.
	list_of_lists_to_compare list of list of ints
		This is the list to see if main_list is in.

	Returns
	-------
	True if main_list is found in list_of_lists_to_compare if all lists are sorted. False if not.
	"""

	# First, sort the main_list
	sorted_main_list = sorted(main_list)

	# Second, go through all lists in list_of_lists_to_compare.
	for list_to_compare in list_of_lists_to_compare:
		# 2.1: if sorted_main_list is the same as list_to_compare when sorted, return True
		if sorted_main_list == sorted(list_to_compare):
			return True

	# Third, could not find sorted_main_list in the sorted lists of list_of_lists_to_compare, so return False
	return False

# --------------------------------------------------------------------------------------------------























