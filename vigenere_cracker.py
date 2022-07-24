from __future__ import division
import re
from fractions import gcd
from string import ascii_lowercase
import math
from itertools import cycle
import string

alphabet = "abcdefghijklmnopqrstuvwxyz"

def strip_to_lc_alphabet(cipher_text_file):
	"""
	Reads the cipher text from a text file (name given in input parameter), 
	removes the whitespace and outputs the cipher text.
	"""
	with open(cipher_text_file, "r") as f:
		for line in f:
			cipher_text = re.sub("[^a-zA-Z]+", "", line).lower()
	return cipher_text

def remove_punctuation(string):
	"""
	Remove the punctuation from a string - for 
	"""
	return re.sub("[^a-zA-Z\s]+", "", string).lower()

def IC(cipher):
	"""
	Use the index of coincidence work out what kind of cipher this is.
	"""
	ic =[]
	length = len(cipher)
	for letter in ascii_lowercase:
		n = cipher.count(letter)
		ic.append((n*(n -1))/(length*(length-1)))
	return sum(ic)


def kasisky_test(cipher):
	"""
	Performs the kasisky test on the cipher text to find a probable key length.
	- find distances between repeated substrings of length at least 3.
	- start with three and increse length until no more repetitions found.
	- find distance between pairs.
	- return as dictionary with sequence and distances as key value pairs.
	"""
	substrDistances = {}
	substrlen = 3
	repfound = True
	while(repfound == True):
		# iterate from 0 to end of message minus subs string length
		repfound = False
		for i in range(0, len(cipher)-substrlen):
			# substring to search for in message
			substr = cipher[i:i+substrlen]
			# search for substr in remainder of message
			for j in range(i+substrlen, len(cipher)-substrlen):
				# repeated substr found
				if cipher[j:j+substrlen] == substr:
					repfound = True
					if substr not in substrDistances:
						substrDistances[substr] = []
					substrDistances[substr].append(j-i)
		substrlen = substrlen + 1
	return substrDistances

def extract_prob_key_length(substrDistances):
	"""
	Determines the probable key length from the distances between repeated substrings
	- calculates the greatest common denominator (GCD) of all the distances
	"""
	dists = [val for dists in substrDistances.values() for val in dists]
	print dists
	print reduce(lambda x,y:gcd(x,y),dists)


def friedman(cipher, guess):
	"""
	Statistically reaffirm the key length using IC (Friedman test)
	"""
	ic = []
	matrix = [cipher[i::guess] for i in range(guess)]
	for row in matrix:
		ic.append(IC(row))
	return sum(ic)/len(ic)

def vigenere_decrypt(cipher, key):
	"""
	Decrypt a cipher text using a given key.
	"""
	with open(cipher,'r') as f:
		cipher_text = f.read()
	spaces = []
	# get index of all spaces in orginal cipher text
	for i, c in enumerate(remove_punctuation(cipher_text)):
		if c==' ':
			spaces.append(i)
	cipher_no_spaces = strip_to_lc_alphabet(cipher)
	pairs = zip(cipher_no_spaces, cycle(key))
	result = ''
	for pair in pairs:
		# difference in indexes between key char and cipher text char
		diff = alphabet.index(pair[0]) - alphabet.index(pair[1])
		# modulo 26 of the difference position in the alphabet
		result += alphabet[diff%26]
	# add spaces to plain text
	for space in spaces:
		result = result[:space] + " " + result[space:]
	return result

def RMH(cipher, key_length):
	"""
	Use frequency analysis to make educated guesses for the key. - Random mutation hill cimber? 
	compare frequency of letters from different keys. Or use IC as a fiteness metric?
	"""


