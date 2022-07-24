from __future__ import division
import re
from string import ascii_lowercase
import math
from math import sqrt

# Frequency of all letters, in the English language, in alphabetic order
english_freqs = [8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.966, 0.153, 0.772, 4.025, 2.406, 
				6.749, 7.507, 1.929, 0.095, 5.987, 6.327, 9.056, 2.758, 0.978, 2.360, 0.150, 1.974, 0.074]

def decrypt1(hex_file, key):
	# """
	# Decode hex file to ascii charachters and XOR with supposed key.
	# """
	with open(hex_file) as fp:
		hex_list = ["{0:2x}".format(ord(c)) for c in fp.read()]
	decoded = hex_list
	for i in range(0,len(hex_list)):
		decoded[i] = chr(int(hex_list[i], 16))# ^ key)
	print ''.join(decoded)
	#return hex_string

def euclidean_dis(data_set1, data_set2):
	# """
	# Calculates the euclidean distance between two datasets
	# """
	diffs_squared = []
	for i, data in enumerate(data_set1):
		diffs_squared.append(pow((data - data_set2[i]),2))
	return sqrt(sum(diffs_squared))


def FA(cipher):
	# """
	# Compares frequency of each letter in text with that of the english language and returns the euclidean distance
	# between both sets of frequencies
	# """
	cipher = ''.join(cipher.split()) # remove whitespace
	cipher = re.sub("[^a-zA-Z\s]+", "", cipher).lower()
	fa =[]
	length = len(cipher)
	for letter in ascii_lowercase:
		n = cipher.count(letter)
		fa.append((n/length)*100)
	return fa

def decrypt2(hex_file, key1, key2):
	# """
	# Decrypts the cipher text using two input keys to XOR with alternatively.
	# """
	key_ic = []
	with open(hex_file, 'r') as fp:
		hex_list = ["{0:2x}".format(ord(c)) for c in fp.read()]
	decoded = hex_list
	for i in range(0,len(hex_list), 2):
		decoded[i] = chr(int(hex_list[i], 16) ^ key1)
	for i in range(1,len(hex_list), 2):
		decoded[i] = chr(int(hex_list[i], 16) ^ key2)
	#print ''.join(decoded)
	return ''.join(decoded)

def find_second_key(hex_file):
	# """
	# Use euclidean distances for every key combination from 0-128 to find most likely possibility for second key.
	# euclidean distance is used to determine the most appropriate key
	# """
	edists = []
	for key in range(0,128):
		edists.append(euclidean_dis(FA(decrypt2(hex_file, 0x13, key)), english_freqs))
	print edists
	print "Min Euclidean Distance is:"
	print min(edists)
	print "Decrypt using:"
	keys = [i for i, x in enumerate(edists) if x == min(edists)]
	print keys
