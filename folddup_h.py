#!/usr/bin/python
# -*- coding: utf-8 -*-
# folddup_h.py: find duplicate folders in current directory.

from pathlib import Path
from tqdm import tqdm
import group
import hashlib
import os
        
def hashfile(file):
    #print("hashing "+str(file)+"...")
    sha = hashlib.sha1()
    try:
        with open(file, 'rb') as f:
            while True:
                try:
                    block = f.read(2**10) # 1MB blocks
                    if not block:
                        break
                    sha.update(block)
                except OSError: # locked file?
                    return '-1'
        return sha.hexdigest()
    except PermissionError: # no permission to access or locked file
        return '-1'

def hashdir(path):
    #print("hashing "+str(path)+"...")
    hashes = []
    for _, dirnames, filenames in os.walk(path):
        for file in filenames:
            hashes.append(hashfile(os.path.join(path,file)))
        for dirpath in dirnames:
            fullpath = os.path.join(path,dirpath)
            if fullpath in hashdict:
                hashes.append(hashdict[fullpath])
            else:
                hashes.append(hashdir(fullpath))
        break
    return str(hash(''.join(hashes)))

if __name__ == '__main__':

    # build a dict with key as file and subfolder number to group folders
    subf = {}
    for dirpath, dirnames, filenames in tqdm(os.walk(os.getcwd())):
        subf.setdefault((len(dirnames),len(filenames)),[]).append(os.path.abspath(dirpath))
    
    # remove uniques | flatten list | add depth attribute | reverse sort the new list
    subf_ = []
    for key in subf.keys():
        sublist = subf[key]
        if len(sublist) > 1:
            for dirpath in sublist:
                subf_.append((dirpath.count(os.path.sep), dirpath))
    subf_.sort(reverse = True)
    del subf
    
    # run the hash function with a global dict
    global hashdict
    hashdict = {}
    for item in tqdm(subf_):
        (_,dirpath) = item
        if dirpath not in hashdict:
            hashdict[dirpath] = hashdir(dirpath)
    del subf_
    
    # invert key/value pairs
    hashdict_ = {}
    for dirpath, hash in hashdict.items():
        hashdict_.setdefault(hash,[]).append(dirpath)
    del hashdict
    
    # remove uniques
    dupes = [set(dirpaths) for dirpaths in hashdict_.values() if len(dirpaths) > 1]
    del hashdict_
    
    # remove pairs with duplicate parents
    results = []
    for s in dupes:
        if len(s) > 2:
            results.append(s)
        else:
            (f1,f2) = s
            p = set([str(Path(f1).parent), str(Path(f2).parent)])
            if p not in dupes:
                results.append(s)
    del dupes
    
    group.print_groups(results)