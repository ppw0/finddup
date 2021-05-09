#!/usr/bin/python3
# -*- coding: utf-8 -*-
# folddup.py

import filecmp
import group
import itertools
import os

def folddup(f1,f2):
    try:
        dcmp = filecmp.dircmp(f1,f2)
        if any([len(dcmp.left_only),len(dcmp.right_only),len(dcmp.funny_files)]):
            return False
        (_, mismatch, errors) = filecmp.cmpfiles(f1,f2,dcmp.common_files,shallow=False)
        if any([len(mismatch),len(errors)]):
            return False
        for cf in dcmp.common_dirs:
            if not folddup(os.path.join(f1,cf),os.path.join(f2,cf)):
                return False
        return True
    except FileNotFoundError:
        return False
    except PermissionError:
        return False

print('''
Subfolders to find and compare:

(1) All of them
(2) Only those at the first level
(3) Only those at the lowest level

(Files with identical content but different filenames will be treated as different.)
''')
choice = int(input("Select: "))

if choice == 1:
    subf = [dirpath for dirpath, _, _ in os.walk('.')]
elif choice == 2:
    subf = [entry for entry in os.listdir('.') if os.path.isdir(os.path.join('.',entry))]
elif choice == 3:
    subf = [dirpath for dirpath, dirnames, _ in os.walk('.') if not dirnames]
else:
    exit(1)

# generate unordered folder pairs and put duplicate pairs in a list
results = [(f1,f2) for f1,f2 in itertools.combinations(subf,2) if folddup(f1,f2)]

group.print_complete(results)