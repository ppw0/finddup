#!/usr/bin/python3
# -*- coding: utf-8 -*-
# folddup_m.py

from pathlib import Path
from tqdm import tqdm
import filecmp
import group
import itertools
import multiprocessing as mp
import os

def folddup(pair):
    while True:
        try:
            f1,f2 = pair
            dcmp = filecmp.dircmp(f1,f2)
            if any([len(dcmp.left_only),len(dcmp.right_only),len(dcmp.funny_files)]):
                return None
            (_, mismatch, errors) = filecmp.cmpfiles(f1,f2,dcmp.common_files,shallow=False)
            if any([len(mismatch),len(errors)]):
                return None
            for cf in dcmp.common_dirs:
                if not folddup((os.path.join(f1,cf),os.path.join(f2,cf))):
                    return None
            return set(pair)
        except FileNotFoundError:
            # assume folders were not removed during search
            print("access locked at "+str(pair)+", retrying")
            continue
        except PermissionError:
            print("no permission to access "+str(pair)+", skipping")
            return None
        break
            
def generatePairs(d):
    for l in d.values():
        # remove singletons
        if len(l) > 1:
            for f1,f2 in itertools.combinations(l,2):
                # remove the folders that have lineal relatives, since no
                # folder can be a duplicate of any of its children or parents
                parent = os.path.commonpath([f1,f2])
                if (f1 != parent and f2 != parent):
                    yield f1,f2

if __name__ == '__main__':
    # partition the directory structure into groups of folders with the same
    # number of subfolders and files contained on the first level
    subf = {}
    for dirpath, dirnames, filenames in os.walk(os.getcwd()):
        subf.setdefault((len(dirnames),len(filenames)),[]).append(os.path.abspath(dirpath))
    
    size = int(sum(len(l)*(len(l)-1)/2 for l in subf.values() if len(l) > 1))

    dupes = []
    with mp.Pool(mp.cpu_count()) as p:
        for pair in tqdm(p.imap(folddup,generatePairs(subf)),total=size):
            # place an incoming pair into its corresponding group if they
            # share any elements to avoid creating a massive list of pairs
            if pair is not None:
                updated = False
                for d in dupes:
                    if len(d.intersection(pair)) > 0:
                        d.update(pair)
                        updated = True
                        break
                if updated is False:
                    dupes.append(pair)  
    
    # remove dupes whose parents are dupes
    results = []
    for d in dupes:
        if len(d) == 2:
            (d1,d2) = d
            if set([str(Path(d1).parent), str(Path(d2).parent)]) in dupes:
                continue
        results.append(d)
    del dupes
     
    group.print_complete(results)
