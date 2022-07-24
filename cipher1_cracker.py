from __future__ import division
import re
from fractions import gcd
from string import ascii_lowercase
import math
from itertools import cycle
import string
import csv

alphabet = "abcdefghijklmnopqrstuvwxyz"

# Frequency of all letters, in the English language, in alphabetic order
english_freqs = [8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.966, 0.153, 0.772, 4.025, 2.406, 
				6.749, 7.507, 1.929, 0.095, 5.987, 6.327, 9.056, 2.758, 0.978, 2.360, 0.150, 1.974, 0.074]

probable_keys = ["DJV", "DJK", "DJZ", "DJR", "DYV", "DYK", "DYZ", "DYR", "HJV", "HJK", "HJZ", "HJR", "HYR", "HYV", "HYZ", "HYR"]

def strip_to_lc_alphabet(cipher_text_file):
	# """
	# Reads the cipher text from a text file (name given in input parameter), 
	# removes the whitespace and outputs the cipher text in lowercase format.
	# """
	with open(cipher_text_file, "r") as f:
		for line in f:
			cipher_text = re.sub("[^a-zA-Z]+", "", line).lower()
	return cipher_text

def remove_punctuation(string):
	# """
	# Remove the punctuation from a string - for finding spaces when decrypting
	# """
	return re.sub("[^a-zA-Z\s]+", "", string).lower()

def IC(cipher):
	# """
	# Use the index of coincidence work out what kind of cipher this is.
	# """
	ic =[]
	length = len(cipher)
	for letter in ascii_lowercase:
		n = cipher.count(letter)
		ic.append((n*(n -1))/(length*(length-1)))
	return sum(ic)


def kasisky_test(cipher):
	# """
	# Performs the kasisky test on the cipher text to find a probable key length.
	# - find distances between repeated substrings of length at least 3.
	# - start with three and increse length until no more repetitions found.
	# - find distance between pairs.
	# - return as dictionary with sequence and distances as key value pairs.
	# """
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
	# """
	# Determines the probable key length from the distances between repeated substrings
	# - calculates the greatest common denominator (GCD) of all the distances
	# """
	dists = [val for dists in substrDistances.values() for val in dists]
	print dists
	print reduce(lambda x,y:gcd(x,y),dists)


def friedman(cipher, guess):
	# """
	# Statistically reaffirm the key length using IC (Friedman test)
	# """
	ic = []
	matrix = [cipher[i::guess] for i in range(guess)]
	for row in matrix:
		print row
		ic.append(IC(row))
	print ic
	return matrix

def vigenere_decrypt(cipher, key):
	# """
	# Decrypt a cipher text using a given key.
	# """
	with open(cipher,'r') as f:
		cipher_text = f.read()
	spaces = []
	# get index of all spaces in orginal cipher text
	for i, c in enumerate(remove_punctuation(cipher_text)):
		if c==' ':
			spaces.append(i)
	cipher_no_spaces = ''.join(remove_punctuation(cipher_text).split())
	pairs = zip(cipher_no_spaces, cycle(key.lower()))
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

def f_analysis(subtexts):
	# """
	# Performs frequency analysis on every letter in each subtext
	# """
	freqs = []
	subtext_freqs = []
	top_freqs  = []
	for i, text in enumerate(subtexts):
		fa =[]
		length = len(text)
		for letter in ascii_lowercase:
			n = text.count(letter)
			fa.append((n/length)*100)
		freqs.append(fa)
		subtext_freqs.append(zip(alphabet,fa))
		top_freqs.append([x for x in subtext_freqs[i] if x[1] >= 10.0])
	print top_freqs
	print freqs
	with open("output.csv", 'wb') as csvfile:
		fwriter = csv.writer(csvfile)
		for subtext_freq in subtext_freqs:
			for f in subtext_freq:
				fwriter.writerow(f)
	return subtext_freqs

def test_probable_keys(keys):
	# """
	# Decrypts and calculates the IC for all of the probable keys.
	# """
	ic = []
	for key in keys:
		ic.append(IC(vigenere_decrypt("cipher1.txt", key)))
	combo = zip(keys, ic)
	with open("output.csv", 'wb') as csvfile:
		fwriter = csv.writer(csvfile)
		for val in combo:
			fwriter.writerow(val)
	return combo







