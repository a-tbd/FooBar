"""Google FooBar Doomsday Fuel Challenge
Find the probability of starting in state 0 and ending in every possible absorbing state
of an absorbing Markov Chain

Takes a square matrix of observations and returns a list of probabilities 
formatted as [numerator1, numerator2...denominator]

b = [[0,1,0,0,0,1], 
	 [4,0,0,3,2,0],
	 [0,0,0,0,0,0],
	 [0,0,0,0,0,0],
	 [0,0,0,0,0,0],
	 [0,0,0,0,0,0]]

answer(b) = [0, 3, 2, 9, 14]
"""

from fractions import Fraction
import fractions
import functools
import itertools
import math
import pdb

# convert matrix values to probabilities
def probability_matrix(m):
	init_n = len(m) 
	# initialize an empty array that will be our probability array
	prob_m = [[0. for col in range(init_n)] for row in range(init_n)]

	for r in range(init_n):
		for c in range(init_n):
			if sum(m[r]) != 0:
				prob_m[r][c] = Fraction(m[r][c], sum(m[r]))
			else:
				prob_m[r][c] = m[r][c]
	return prob_m

# get Q and R from the canonical matrix
def transient_matrix(m, m_prob):
	# indices for transient and abosrbing states
	sums=[sum(i) for i in m]
	zeroindices = [i for i, item in enumerate(sums) if item==0]
	notzeroindices = [i for i in set(range(len(m))) - set(zeroindices)]
	# m x m matrix of the transient states
	trans_m = [[0. for col in range(len(notzeroindices))] for row in range(len(notzeroindices))]

	for i in range(len(notzeroindices)):
		for j in range(len(notzeroindices)):
			trans_m[i][j] = m_prob[notzeroindices[i]][notzeroindices[j]]
	# m x n matrix of the transiet states x absorbing states
	trans_abs_m = [[0. for col in range(len(zeroindices))] for row in range(len(notzeroindices))]

	for i in range(len(notzeroindices)):
		for j in range(len(zeroindices)):
			trans_abs_m[i][j] = m_prob[notzeroindices[i]][zeroindices[j]]
	return trans_m, trans_abs_m

# Identity matrix minus Q
def identity_sub_trans(q):
	# create an identity matrix (diagonals = 1)
	identity = [[Fraction(0, 1) for col in range(len(q))] for row in range(len(q))]
	counter = 0
	for row in identity:
		row[counter] = Fraction(1, 1)
		counter += 1

	return[[a - b for a, b in itertools.izip(one, two)] 
			for one, two in itertools.izip(identity, q)]

# subroutines for inverse matrix
def get_minor(m, i, j):
	# return the smaller matrix without the first row and anything in column in index j
	minor = [m[a][0:j] + m[a][j+1:] for a in range(len(m))]
	return minor[0:i] + minor[i+1:]

def get_determinant(m):
	if len(m) == 2:
		return m[0][0]*m[1][1] - m[0][1]*m[1][0]
	determinant = 0
	for col in range(len(m)):
		determinant += (Fraction(-1, 1)**col)*m[0][col]*get_determinant(get_minor(m, 0, col))
	return determinant

def matrix_of_minors(m):
	minors = [[Fraction(0, 1) for col in range(len(m))] for row in range(len(m))]

	for i in range(len(minors)):
		for j in range(len(minors)):
			minors[i][j] = get_determinant(get_minor(m, i, j))
	return minors

def matrix_of_cofactors(m):
	cofactors = [[Fraction(0, 1) for col in range(len(m))] for row in range(len(m))]
	count = 0
	for i in range(len(m)):
		for j in range(len(m)):
			if count % 2 == 0:
				cofactors[i][j] = m[i][j]
			else:
				cofactors[i][j] = -1*m[i][j]
			count +=1 
	return cofactors

# inverse matrix
def get_inverse(m):
	determinant = get_determinant(m)

	if len(m) == 2:
		return [[m[1][1] * Fraction(1, determinant), m[0][1]*Fraction(-1,determinant)], 
				[m[1][0]*Fraction(-1,determinant), m[0][0]*Fraction(1, determinant)]]
	else:
		try:
			# step 1: get the matrix of minors
			minors = matrix_of_minors(m)
			# step 2: turn that into a matrix of cofactors
			cofacs = matrix_of_cofactors(minors)
			# step 3: adjugate
			ad = list(itertools.izip(*cofacs))
			# step 4: multiply by 1/determinant
			inverse = [[Fraction(1, determinant)*ad[i][j] for j in range(len(ad[0]))] for i in range(len(ad))]
		except ZeroDivisionError:
			print "Inverse matrix doesn't exist"
		return inverse

def get_final_prob(n, r):
	zip_r = itertools.izip(*r)
	B = [[sum(abs(ele_a)*abs(ele_b) for ele_a, ele_b in zip(row_a, col_b)) 
             for col_b in zip_r] for row_a in n]
	return B

def get_gcd(l):
	if len(l) == 2:
		return fractions.gcd(l[0], l[1])
	elif len(l) > 2:
		return fractions.gcd(l[0], get_gcd(l[1:]))
	else:
		return l[0]

def final_answer_format(m):
	state_0 = m[0]
	numers = [i.numerator for i in state_0]
	denoms = [i.denominator for i in state_0]

	denominator = 1
	for i in range(len(numers)):
		for j in range(len(numers)):
			if j != i:
				numers[i] *= denoms[j]
		denominator *= denoms[i]

	gcd = get_gcd(numers)

	ans = [int(i / gcd) for i in numers]
	ans.append(int(denominator / abs(gcd)))
	return ans

def answer(m):
	if len(m) == 1:
		return [1,1]
	prob_m = probability_matrix(m)
	Q, R = transient_matrix(m, prob_m)
	N = identity_sub_trans(Q)
	N_inv = get_inverse(N)
	B = get_final_prob(N_inv, R)
	return final_answer_format(B)


########################
###### TEST CASES ######
########################

# additional test cases: https://pastebin.com/HAiEwnD2

def test0:
	m = [[0]]
	return m
#a: [1,1]

def test1():
	m = [[1, 2, 3, 0, 0, 0], 
		 [4, 5, 6, 0, 0, 0], 
		 [7, 8, 9, 1, 0, 0], 
		 [0, 0, 0, 0, 1, 2], 
		 [0, 0, 0, 0, 0, 0], 
		 [0, 0, 0, 0, 0, 0]]
	return m
#a = [1, 2, 3]

def test3():
	m = [[0, 2, 1, 0, 0], 
		 [0, 0, 0, 3, 4], 
		 [0, 0, 0, 0, 0], 
		 [0, 0, 0, 0, 0], 
		 [0, 0, 0, 0, 0]]
	return m
#[7, 6, 8, 21]

def test4():
	m = [[0, 1, 0, 0, 0, 1], 
		 [4, 0, 0, 3, 2, 0], 
		 [0, 0, 0, 0, 0, 0], 
		 [0, 0, 0, 0, 0, 0], 
		 [0, 0, 0, 0, 0, 0], 
		 [0, 0, 0, 0, 0, 0]]
	return m
#a: [0, 3, 2, 9, 14]

def test5():
	m = [[0, 86, 61, 189, 0, 18, 12, 33, 66, 39], 
		 [0, 0, 2, 0, 0, 1, 0, 0, 0, 0], 
		 [15, 187, 0, 0, 18, 23, 0, 0, 0, 0], 
		 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
		 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
		 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
		 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
		 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
		 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
		 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
	return m
#a = [6, 44, 4, 11, 22, 13, 100]

def test6():
	m =  [[0, 0, 0, 0, 3, 5, 0, 0, 0, 2], 
		 [0, 0, 4, 0, 0, 0, 1, 0, 0, 0], 
		 [0, 0, 0, 4, 4, 0, 0, 0, 1, 1], 
		 [13, 0, 0, 0, 0, 0, 2, 0, 0, 0], 
		 [0, 1, 8, 7, 0, 0, 0, 1, 3, 0], 
		 [1, 7, 0, 0, 0, 0, 0, 2, 0, 0], 
		 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
		 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
		 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
		 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
	return m
#a = [1, 1, 1, 2, 5]


def test7():
	m = [[0,1,0,0,0,1], 
	 	[4,0,0,3,2,0],
	 	[0,0,0,0,0,0],
	 	[0,0,0,0,0,0],
	 	[0,0,0,0,0,0],
	 	[0,0,0,0,0,0]]
	return m
#a: [0, 3, 2, 9, 14]

print answer(test7())

