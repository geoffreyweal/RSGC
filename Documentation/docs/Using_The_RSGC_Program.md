# How To Use The RSGC Program

The RSGC Program is designed to be versatile and be added to your existing python scripts if you want to couple the RSGC program with other methods and protocols. 

For a general use case, this is the python script you might want to set up to run the RSGC program on your existing crystals. 

???+ example "``Run_RSGC.py`` python script"

	```python title="Run_RSGC.py" linenums="1"
	--8<-- "docs/Files/Run_RSGC.py"
	```

Below we describe the ``Run_RSGC.py`` python script above so you can understand how it works.

## Part I: Get the names of the crystals you want to remove sidegroups from

In the first section, give the name of the folder that contains the crystals you want to remove sidegroups from in the ``crystal_database_dirname`` variable. **Change these variables to the names of your files and folders**. The names of the files and folders you need to give here are: 

* Also give the name of the folder containing the crystals that were repaired during the ``RSGC`` program in the ``repaired_crystal_database_dirname`` variable. 
* If you don't want to give a ``repaired_crystal_database_dirname`` variable, set it to ``None``. (i.e: ``repaired_crystal_database_dirname = None``).
* If there are any crystal you are having problems with and you want to exclude them in the meantime, put them in the ``exclude_identifiers`` list.

An example of the code for ``PART I`` is shown below:

```python title="Part I of Run_RSGC.py: Get the names of the crystals you want to remove sidegroups from" show_lines="9:22" linenums="9"
--8<-- "docs/Files/Run_RSGC.py"
```

## Part II: Determine settings

In the second section, determine the settings for running the RGSC program. **Change these to the settings you desire**. The variable settings you can set here are:

* ``leave_as_ethyls`` (*bool.*): This indicates if you want to change any saturated aliphatic sidechain into ethyl groups, in which case set this to ``True``. If you would want change these saturated aliphatic sidechain into methyl groups, set this to ``False``.
* ``save_molecules_individually`` (*bool.*): This indicates if you want to save the molecules from the crystals individually, as well as save the full crystal.

An example of the code for ``PART II`` is shown below:

```python title="Part II of Run_RSGC.py: Determine settings" show_lines="22:34" linenums="22"
--8<-- "docs/Files/Run_RSGC.py"
```

## Part III: Database checks

In the third section, check that the crystal databases exist. You can leave this as is, or modify it as you would like. An example of the code for ``PART III`` is shown below:

```python title="Part III of Run_RSGC.py: Database checks" show_lines="34:45" linenums="34"
--8<-- "docs/Files/Run_RSGC.py"
```

## Part IV: Gather the paths to the crystal files

In the fourth section, gather all the paths of the crystal files you want to remove. You can leave this as is, or modify it as you would like. An example of the code for ``PART IV`` is shown below:

```python title="Part IV of Run_RSGC.py: Gather the paths to the crystal files" show_lines="45:78" linenums="45"
--8<-- "docs/Files/Run_RSGC.py"
```

## Part V: Remove existing files from previous RSGC runs

In the fifth section, remove any existing files that were produced during previous RSGC runs. You can leave this as is, or modify it as you would like.  An example of the code for ``PART V`` is shown below:

```python title="Part V of Run_RSGC.py: Remove existing files from previous RSGC runs" show_lines="78:96" linenums="78"
--8<-- "docs/Files/Run_RSGC.py"
```

## Part VI: Run the RSGC program

In the sixth section, remove sidegroups from all your crystals of interest using the RSGC program. You can leave this as is, or modify it as you would like.  An example of the code for ``PART VI`` is shown below:

```python title="Part VI of Run_RSGC.py: Run the RSGC program" show_lines="96:132" linenums="96"
--8<-- "docs/Files/Run_RSGC.py"
```


## Output from the RSGC Program

The RSGC program will create a folder called ``crystals_with_sidechains_removed`` and save the xyz files of the crystals given in your ``Run_RSGC.py`` script that you want to remove the aliphatic sidechains of. 

* Another folder called ``crystals_with_sidechains_removed_molecules`` will also be created. This will contain the ``xyz`` files of the individual molecules from your crystal files. This folder is purely created to allow you to check the molecules that make up your crystal, and make it easier to double-check that only the alphatic sidechains that only contain sp<sup>3</sup> carbons and hydrogens have been removed. 

As well as the  ``crystals_with_sidechains_removed`` and ``crystals_with_sidechains_removed_molecules`` folders, the RSGC program will also create a file called ``RSGC_issues.txt`` that will record any warning messages produced while the RSGC program. 


## Example Output Files from the RSGC Program

[Click here](https://github.com/geoffreyweal/RSGC/tree/main/Examples) to find examples of crystals from the CCDC that have been repaired with the instructions from a ``Run_RSGC.py`` file. 

