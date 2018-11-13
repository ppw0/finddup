#!/usr/bin/python
# -*- coding: utf-8 -*-
# filedup_r.py: removes all but one duplicate file in current folder.

import hashlib
import os

def md5hash(path, blocksize = 65536):
	afile = open(path,'rb')
	hasher = hashlib.md5()
	buf = afile.read(blocksize)
	while len(buf) > 0:
		hasher.update(buf)
		buf = afile.read(blocksize)
	afile.close()
	return hasher.hexdigest()

def filedup(folder):
	dupes = {} # dupes in format {hash:[names]}
	for filename in os.listdir(folder):
		hash = md5hash(filename) # calculate hash
		dupes.setdefault(hash,[]).append(filename) # add or append the filename
	return dupes	
			
if __name__ == '__main__':
    count = 0
    for r in filedup(os.getcwd()).values():
        while len(r) > 1:
            os.remove(r.pop())
            count += 1
    print("%d files removed" %(count))
