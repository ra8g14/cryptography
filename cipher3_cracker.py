from __future__ import division
import re
from fractions import gcd
from string import ascii_lowercase
import math
from itertools import cycle
import string
import csv

cipher3 = "NVL^OSZRHDFR@AHY^EPCFSHC][H^AEAB@^LZLQO^GVZXHR]Y^EZDLQMV]UO_AEAX@Z[RDR]ED^OEAR"

def decrypt2(key1, key2):
	# """
	# Decrypts the cipher text using two input keys to XOR with alternatively.
	# """
	decoded = list(cipher3)
	key_ic = []
	for i in range(0,len(cipher3), 2):
		decoded[i] = chr(ord(cipher3[i]) ^ key1)
	for i in range(1,len(cipher3), 2):
		decoded[i] = chr(ord(cipher3[i]) ^ key2)
	# print decoded
	return ''.join(decoded)

def decrypt1(key):
	# """
	# Decrypts the cipher text using two input keys to XOR with alternatively.
	# """
	decoded = list(cipher3)
	key_ic = []
	for i in range(0,len(cipher3)):
		decoded[i] = chr(ord(cipher3[i]) ^ key)
	# print decoded
	return ''.join(decoded)


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
	with open("output4.csv", 'wb') as csvfile:
		fwriter = csv.writer(csvfile)
		fwriter.writerow(fa)
	return fa

def IC(cipher):
	# """
	# works out the index of coincidence for a given input string
	# """
	ic =[]
	cipher = cipher.lower()
	length = len(cipher)
	for letter in ascii_lowercase:
		n = cipher.count(letter)
		ic.append((n*(n -1))/(length*(length-1)))
	return sum(ic)

def brute_force_key():
	# """
	# Cycles through all key combinations for one key and returns decrypts with the highest IC
	# """
	high_ics = []
	for i in range(0,128):
		decrypt = (decrypt1(i))
		if decrypt.isalpha():
			ic = IC(decrypt)
			if ic >= 0.065:
				high_ics.append([i])
				print ic
				print i

def brute_force_keys():
	# """
	# Cycles through all key combinations for two keys and returns the pairs with the highest IC
	# """
	high_ics = []
	for i in range(0,256):
		for j in range(0,256):
			decrypt = (decrypt2(i,j))
			if decrypt.isalpha():
				ic = IC(decrypt)
				if ic >= 0.065:
					high_ics.append([i,j])
					print ic
					print i
					print j
	with open("output3.csv", 'wb') as csvfile:
		fwriter = csv.writer(csvfile)
		for ic in high_ics:
			fwriter.writerow(ic)
