#!/usr/bin/python
# -*- coding: utf-8 -*-
# folddup.py: finds duplicate folders in current directory.

import os

# define folder duplicate function
import filecmp
def folderdup(f1,f2):
	try:
		fcmp = filecmp.dircmp(f1,f2)
		if any([len(fcmp.left_only),len(fcmp.right_only),len(fcmp.funny_files)]:
			return False
		(_, mismatch, errors) =  filecmp.cmpfiles(f1,f2,fcmp.common_files,shallow=False)
		if any([len(mismatch),len(errors)]):
			return False
		for cf in fcmp.common_dirs:
			if not (folderdup((os.path.join(f1,cf),os.path.join(f2,cf)))):
				return False
		return True
	except PermissionError:
		return False

# get list of folders and generate unordered folder pairs

# first-level depth version
import itertools
import glob
pairs = itertools.combinations([p[:-1] for p in glob.glob('*/')],2)

# least efficient (all-to-all) version

# recursive list of all subdirectories
#subfolders = [dirpath for dirpath, _, _ in os.walk('.')]

# recursive list of all subdirectories (slightly faster)
#for entry in os.listdir('.'):
#    if os.path.isdir(os.path.join('.',entry)):
#        subfolders.append(entry)

#pairs = [pair for pair in itertools.combinations(subfolders,2)]

# leaves only all-to-all comparison
#subfolders = [dirpath for dirpath, dirnames, _ in os.walk('.') if not dirnames]
#pairs = [pair for pair in itertools.combinations(subfolders,2)]

# put duplicate pairs in a list
dupes = [[f1,f2] for f1,f2 in pairs if folderdup(f1,f2)]

import group
group.print_groups(dupes)
