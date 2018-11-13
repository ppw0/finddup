#!/usr/bin/python
# -*- coding: utf-8 -*-
# folddup_m.py: finds and returns duplicate folders. multithreaded, with some optimizations.

from pathlib import Path
from tqdm import tqdm
import filecmp
import group
import itertools
import multiprocessing as mp
import os

# define folder duplicate function
def folddup(pair):
    #print ("comparing "+str(pair))
    while True:
        try:
            f1, f2 = pair
            fcmp = filecmp.dircmp(f1,f2)
            if any([len(fcmp.left_only),len(fcmp.right_only),len(fcmp.funny_files)]):
                return None
            (_, mismatch, errors) =  filecmp.cmpfiles(f1,f2,fcmp.common_files,shallow=False)
            if any([len(mismatch),len(errors)]):
                return None
            for cf in fcmp.common_dirs:
                if not folddup((os.path.join(f1,cf),os.path.join(f2,cf))):
                    return None
            return set(pair)
        except FileNotFoundError: # assumes folders were not removed during search
            #print ("access locked at "+str(pair)+",retrying")
            continue
        except PermissionError:
            #print ("no permission to access "+str(pair)+", skipping")
            return None
        break

# nonLineal: no folder can be a duplicate of any of its children or its parents
def nonLineal(pair):
    f1, f2 = pair
    parent = os.path.commonpath([f1,f2])
    if f1 == parent or f2 == parent:
        return False
    return True

# pair generator function                
def generatePairs(d):
    for l in d.values():
        if len(l) > 1:
            for pair in itertools.combinations(l,2):
                if nonLineal(pair):
                    yield pair

if __name__ == '__main__':

    # build a dict with key as file and subfolder number to group folders
    subf = {}
    for dirpath, dirnames, filenames in os.walk(os.getcwd()):
        subf.setdefault((len(dirnames),len(filenames)),[]).append(os.path.abspath(dirpath))
    
    size = int(sum(len(l)*(len(l)-1)/2 for l in subf.values() if len(l) > 1))
    
    # find duplicate folders
    dupes = []
    with mp.Pool(mp.cpu_count()) as p:
        for pair in tqdm(p.imap(folddup,generatePairs(subf)),total=size):
            if pair is not None:
                dupes_updated = False
                for d in dupes:
                    if len(d.intersection(pair)) > 0:
                        d.update(pair)
                        dupes_updated = True
                        break
                if dupes_updated is False:
                    dupes.append(pair)

    # trim results
    dupes = group.group(dupes)

    # resulting list contains no pairs with duplicate parents
    results = []
    for s in dupes:
        if len(s) > 2:
            results.append(s)
        else:
            (f1,f2) = s
            p = set([str(Path(f1).parent), str(Path(f2).parent)])
            if p not in dupes:
                results.append(s)
            
    group.print_groups(results)
