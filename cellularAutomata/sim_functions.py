import numpy as np
from numba import jit

@jit(nopython=True) # compiles the function to optimized machine code
def get_neighbour_average(x):
	"""
	Parameters:
    -----------
    x : numpy.ndarray
        A 2D array representing the input matrix to be transformed.

    Returns:
    --------
    numpy.ndarray
        A 2D array representing the transformed matrix where each element is the average of its neighbors.

    Notes:
    ------
	In the hexagonal grid, sites are offset in alternating rows.
	Note the periodic boundaries.

	Row 3 (Odd): (3,3)---(3,0)---(3,1)---(3,2)---(3,3)---(3,0)
					 \    / \    /   \    / \    /   \   /
	Row 0 (Even):    (0,0)---(0,1)---(0,2)---(0,3)---(0,0)
            	     /    \ /    \   /    \ /    \   /   \ 
	Row 1 (Odd): (1,3)---(1,0)---(1,1)---(1,2)---(1,3)---(1,0)
					 \    / \    /   \    / \    /   \   /
	Row 2 (Even):    (2,0)---(2,1)---(2,2)---(2,3)---(2,0)
            	     /    \ /    \   /    \ /    \   /   \ 
	Row 3 (Odd): (3,3)---(3,0)---(3,1)---(3,2)---(3,3)---(3,0)
					 \    / \    /   \    / \    /   \   /
	Row 0 (Even):    (0,0)---(0,1)---(0,2)---(0,3)---(0,0)

	Hence when looping over neighbours, we need to treat even and odd rows differently.
	"""

	n = x[0].size
	M = np.zeros((n + 2, n + 2))  # slightly larger dummy matrix to include boundary conditions

	# matrix body
	M[1:n + 1, 1:n + 1] = x

	# PERIODIC BOUNDARY CONDITION
	M[1:n + 1, 0]     = M[1:n + 1, n]  # first column equals second to last column
	M[1:n + 1, n + 1] = M[1:n + 1, 1]  # last column equals second column
	M[0, 1:n + 1]     = M[n, 1:n + 1]  # first row equals second to last row
	M[n + 1, 1:n + 1] = M[1, 1:n + 1]  # last row equals second row

	# corners for hexagonal lattice
	M[0, 0]         = M[n, n]
	M[0, n + 1]     = M[n, 1]
	M[n + 1, n + 1] = M[1, 1]
	M[n + 1, 0]     = M[1, n]
	
	I = np.zeros((n, n)) # central part of M (excluding the boundary)

	# iterates over each element of I, updating it based on M
	for i in range(1, n + 1):
		for j in range(1, n + 1):

			# Set the value on I[i-1][j-1] which corresponds to M[i][j].
			# To do that, sum values of the neighboring elements of M[i][j].
			I[i - 1][j - 1] = M[i + 1][j] + M[i - 1][j] + M[i][j + 1] + M[i][j - 1]

			# even row
			if (i - 1) % 2 == 0: 
				I[i - 1][j - 1] += M[i + 1][j + 1] + M[i - 1][j + 1]

			# odd row
			else:
				I[i - 1][j - 1] += M[i + 1][j - 1] + M[i - 1][j - 1]

	return (1./6)*I # divide by the number of neighbors