#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import division
import os
import re
import sys
import timeit
import argparse
from multiprocessing import Pool


CWD = os.getcwd()  #current working directory 

def get_filenames():
	"""
	Returns complete list of filenames
    """

	filenames = []

	for filename in os.listdir(CWD):
		if filename.endswith(".txt"):
			filenames.append(filename)
	
	return filenames 


def get_data(filename):
	"""
	Pre-processes data in filename by stripping lines and commas out of words
	:param a given file
    """

	words = []

	with open(filename,'r') as f: 
		for line in f:
			word = line.strip('\n').strip('\r').strip('.').strip(',').split(' ')
			words.append(word)

	return words 


def sumFileSize():
	"""
	Prints sum of filesize of files to be mapreduced
    	"""

	filesize = 0

	for filename in os.listdir(CWD):
		if filename.endswith(".txt"):
			statinfo = os.path.getsize(filename)
			filesize += statinfo
	
	filesize_in_gb = filesize / 1073741824
	print("Size of files:", filesize_in_gb, "GB")


def map_function(filename):
	"""
	Takes a list of sentences,splits, and sums up words per sentence
    :param filename: a single filename
   	"""

	sentences = get_data(filename)

	wordCount = {}

	for  sentence in sentences:
		for word in sentence:
			try:
				wordCount[word] += 1 
			except KeyError:
				wordCount[word] = 1

	print("Done Analyzing %s" % (filename))
	
	return wordCount

def reduce_function(dict_list):
	"""
	This function reduces a dictionary with mapped keys/values by summing values
    :param words: List of words
    """
	d = {}

	for entry in dict_list:
		print("merging dictionary...")
		for k, v in entry.items():
			try:
				d[k] += v
			except KeyError:
				d[k] = v
	
	return d 

def show_items(mapreduce):
	"""
	Sorts values by descending order and prints them
    	:param mapreduce: Mapreduce dictionary
   	"""

	sorted_items = sorted(mapreduce.items(), key=lambda x: x[1])
	
	for i in sorted_items:
		print("'%s' - %i" % i)

if __name__ == '__main__':
	sumFileSize()

	print("Processing textfiles...")

	#Single-thread
	
	files = get_filenames()

	for filename in files: 
		mapr = map_function(filename)
	
	mr = reduce_function(mapr)
	
	show_items(mr)

	#Multiprocessing

	# files = get_filenames()
	# pool= Pool(processes=5) 
	# result_set = pool.map(map_function, files, chunksize=30) #processing an iterated list of files

	# show_items(reduce_function(result_set))

	
