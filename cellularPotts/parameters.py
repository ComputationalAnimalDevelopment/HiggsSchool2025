"""Parameter file"""

###############################

# installed modules
import numpy as np

###############################
###############################
# Simulation parameters

init_MCS  = 100 # Monte Carlo Steps of initialization routine
total_MCS = int(1e6) # int(1e7) # total number of Monte Carlo Steps

SAVE_DATA = False
MCS_to_save = 100  # How many of the data points should be saved

# Grid size
height = 80 # number of rows
width  = 80 # number of cols

initial_cell_number = [8, 8, 6]


# kT
"""
The cellular Potts model was originally inspired by the
Potts model of statistical mechanics, where the
Boltzmann constant times temperature (kT) is a
parameter that determines the energy scale of the
system. In the context of the cellular Potts model,
kT is used to control the motility or activity of the cells
and hence loses its physical meaning.
"""
kT = 15

# ADHESION
"""
The adhesion table stores pairwise adhesion values
between different cell types (tau).

Interaction mapping:
tau1:  0   1   2   3
tau2:
   0  0-0 0-1 0-2 0-3 
   1  1-0 1-1 1-2 1-3
   2  2-0 2-1 2-2 2-3
   3  3-0 3-1 3-2 3-3

It is a diagonally symmetric matrix.
Only the lower diagonal needs to be defined, 
the rest is auto-filled.

The adhesions are expressed as affinities, and in
the code their sign is flipped. This means that a
more positive value indicates stronger adhesion.
Stronger means more energetically favorable.
A negative value indicates repulsion, or energetically
not favorable.
"""

adhesion_table = np.array([
    [    0,   0,    0,   0], # adhesion medium - partner
    [ -0.5, 1.9,    0,   0], # adhesion cell type 1 - partner E
    [ -0.5, 0.5,  2.2,   0], # adhesion cell type 2 - partner T
    [ -0.5, 0.5,  0.4, 0.5]  # adhesion cell type 3 - partner X
])

adhesion_table *= 36 # scale all values

# Make the matrix diagonally symmetric (copy lower triangle to upper triangle)
i_lower = np.tril_indices_from(adhesion_table, -1)
adhesion_table[i_lower[::-1]] = adhesion_table[i_lower]


# Target volume (or area in 2D)
"""Target volume / area"""
target_volume = np.array([
    30, # target volume of cell type 1
    30, # target volume of cell type 2
    30  # target volume of cell type 3
])

# lambda is a Lagrange multiplier or penalty factor
lambda_volume = np.array([
    1, # cell type 1
    1, # cell type 2
    1  # cell type 3
])


# Surface area (or perimeter in 2D)
"""Target surface area / perimeter"""
target_surface = np.array([
    20, # target surface of cell type 1
    20, # target surface of cell type 2
    20  # target surface of cell type 3
])

# lambda is a Lagrange multiplier or penalty factor
lambda_surface = np.array([
    0.2,  # cell type 1
    0.2,  # cell type 2
    0.04  # cell type 3
])

###############################
###############################
# Graphics parameters

gui_scale = 5 # scale resolution

gui_update_frequency = 1000 # how often the GUI is updated in time steps

gui_cell_colours = {0: (250, 250, 250), # medium
                    1: (179, 71, 71),   # cell type 1
                    2: (74, 54, 176),   # cell type 2
                    3: (74, 158, 66),   # cell type 3
                    99: (180, 180, 180) # colour of cell boundary
}