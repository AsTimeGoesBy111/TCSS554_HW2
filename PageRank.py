import os
import numpy as np
import pandas as pd

# Set up parameters
file = open('graph.txt').read()
arr = file.split("\n")
size = 6
maxerr = 0.000001

# Generate the dictionary containing outlinks for each node
def getOutlinkDic(arr):
	dic = {}
	for l in arr:
		if not l:
			continue
		num = int(l.split(" ")[2])
		if (num == 0):
			continue
		j = l.split(" ")[0]
		if (j not in dic):
			dic[j] = 1
		else:
			dic[j] += 1
	return dic

# Generate the stochastic matrix
def getMatrix(beta):
	dic = getOutlinkDic(arr)
	matrix = [[0.0 for x in range(size)] for y in range(size)]
	for l in arr:
		if not l:
			continue
		num = int(l.split(" ")[2])
		j = l.split(" ")[0]
		i = l.split(" ")[1]
		val = (1 - beta) * (1 / size)
		if (num == 1):
			val = beta * (1 / dic[j])
		matrix[ord(i) - ord('A')][ord(j) - ord('A')] = val
    # Use the numpy matrix
	np_arr = np.array(matrix)
	np_matrix = np.asmatrix(np_arr)
	return np_matrix
	
# Get the original rank vector
def getRankVector():
	list1 = [1 / size] * size
	arr = np.array(list1)
	return arr.reshape(-1, 1)

# Implemente the page rank algorithm to generate converged vector
def pagerank(beta):
	np_matrix = getMatrix(1.00)
	vector = getRankVector()
	newVector = np.array([0.0] * size).reshape(-1, 1)
	count = 0
	sum1 = np.sum(vector)
	while (sum1 > maxerr):
		if (count != 0):
		   vector = newVector
		newVector = beta * np_matrix * vector + (1 - beta) * (1 / size)
		sum1 = np.sum(np.abs(newVector - vector))
		count += 1
	if beta == 1:
		print("When using Matrix M, the iterations taken to get the converge is: " + str(count))
	else:
		print("When using Matrix A, the iterations taken to get the converge is: " + str(count))
	return newVector

# When generate Matrix, use round(val, 4) for code line 40
print("The output of Matrix M is: ")
print(getMatrix(1.00))

print("After teleportation, the output of Matrix A is: ")
print(getMatrix(0.85))

print("The original rank vector(R) is: ")
print(getRankVector())

print("When using Matrix M, the Converged rank vector(R') is: ")
print(pagerank(1.00))

print("When using Matrix A, the Converged rank vector(R') is: ")
print(pagerank(0.85))
