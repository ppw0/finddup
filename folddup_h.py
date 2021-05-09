#!/usr/bin/python3
# -*- coding: utf-8 -*-
# folddup_h.py

from pathlib import Path
from tqdm import tqdm
import group
import hashlib
import os
        
def hashfile(file):
    sha = hashlib.sha1()
    try:
        with open(file, 'rb') as f:
            while True:
                try:
                    block = f.read(2**10) # 1MB blocks
                    if not block:
                        break
                    sha.update(block)
                except OSError: # locked file
                    return '-1'
        return sha.hexdigest()
    except PermissionError: # no permission to access or locked file
        return '-1'

if __name__ == '__main__':

    hashdict = {}
    for (_, path, dirnames, filenames) in tqdm(sorted(((dirpath.count(os.path.sep), dirpath, dirnames, filenames) for dirpath, dirnames, filenames in os.walk('.', topdown = False)), reverse = True)): # imitate a reverse breadth-first os.walk() traversal
        hashes = []
        for file in filenames:
            hashes.append(hashfile(os.path.join(path,file)))
        for dirpath in dirnames:
            hashes.append(hashdict[os.path.join(path,dirpath)])
        hashdict[path] = str(hash(''.join(hashes)))
    
    # invert k-v pairs to find collisions
    invdict = {}
    for dirpath, hash in hashdict.items():
        invdict.setdefault(hash,[]).append(dirpath)
    del hashdict

    # isolate duplicates
    dupes = [set(dirpaths) for dirpaths in invdict.values() if len(dirpaths) > 1]
    del invdict
    
    # isolate dupes whose parents are dupes
    results = []
    for d in dupes:
        if len(d) == 2:
            (d1,d2) = d
            if set([str(Path(d1).parent), str(Path(d2).parent)]) in dupes:
                continue
        results.append(d)
    del dupes
    
    group.print_complete(results)