#!/usr/bin/python
# -*- coding: utf-8 -*-
# filedup.py: finds duplicate files. based on calculating MD5 hashes, with special thanks to Andres
# Torres: https://www.pythoncentral.io/finding-duplicate-files-with-python/

import hashlib
import os
import sys

def hashfile(path, blocksize = 65536):
	afile = open(path, 'rb')
	hasher = hashlib.md5()
	buf = afile.read(blocksize)
	while len(buf) > 0:
		hasher.update(buf)
		buf = afile.read(blocksize)
	afile.close()
	return hasher.hexdigest()

def findDup(parentFolder):
	dupes = {} # dupes in format {hash:[names]}
	for dirName, subdirs, fileList in os.walk(parentFolder):
		print('Scanning %s...' % dirName)
		for filename in fileList:
			path = os.path.join(dirName, filename) # get the path to the file
			file_hash = hashfile(path) # calculate hash
			dupes.setdefault(file_hash,[]).append(path) # add or append the file path
	return dupes

# joins two dictionaries
def joinDicts(dict1, dict2):
	for key in dict2.keys():
		if key in dict1:
			dict1[key] = dict1[key] + dict2[key]
		else:
			dict1[key] = dict2[key]

def printResults(dict1):
	results = [x for x in dict1.values() if len(x) > 1]
	if len(results) > 0:
		print('Duplicates Found: ')
		print('The following files are identical. The name could differ, but the content is identical')
		print('----')
		for result in results:
			for subresult in result:
				print('\t\t%s' % subresult)
			print('---')
	else:
		print('No duplicates found.')
				
			
if __name__ == '__main__':
	if len(sys.argv) > 1:
		dupes = {}
		folders = sys.argv[1:]
		for i in folders: # iterate the folders given
			if os.path.exists(i):
				joinDicts(dupes,findDup(i)) # find the duplicated files and append them to the dupes
			else:
				print('%s is not a valid path, please verify' % i)
				sys.exit()
		printResults(dupes)
	else:
		print('Usage: python filedup.py folder or python filedup.py folder1 folder2 folder3')
