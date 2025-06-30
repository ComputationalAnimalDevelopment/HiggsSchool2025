'''
Parameters of the model
'''

import numpy as np
####
# Graphics parameters #
#######################

gui_X0 = 0
gui_Y0 = 0
gui_WINDOW_HEIGHT = 200
gui_WINDOW_WIDTH = gui_WINDOW_HEIGHT*5

gui_scale = 18 # scale factor for the graphics
gui_hexagon_size = 10 # size of hexagons in pixels

gui_update_frequency = 1 # step frequency of graphics update

#########################
# Simulation parameters #
#########################

grid = 10 # lattice size

# values of external VEGF to simulate, each value generates a data file
Vt_vec = np.array([0., 10., 50., 100., 150., 200., 220, 240, 260, 280, 300., 
                    500., 1000., 2000., 3000., 5000., 10000.]) 

extVEGF = Vt_vec[0]

T1, T2 = 1, 500   # time for initial relaxation and simulation afterwards
dt = 0.1           # timestep

##################
# Reaction rates #
##################

# Production rates
p_N = 1200   # production of Notch
p_D = 1000   # production of Delta
p_J = 800    # production of Jagged
p_R = 1000.  # production of VEGF receptor

# Degradation rates
d  = 1.0e-1   # general degradation rate
dI = 5.0e-1  # degradation rate of Notch intracellular domain (ICD)

# Binding rates
kc = 5.0e-4  # cis-binding rate
kt = 2.5e-5  # trans-binding rate


############################
# Hill function parameters #
############################

# Binding constants
# The binding constants correspond to the x-value
# where the functionr reaches its half-maximum y
Ki = 2.0e+2   # binding constant for Notch intracellular domain
Kv = 200/2.4  # binding constant for VEGF-VEGF-receptor complex

# Cooperativity exponents
# The higher the exponent, the steeper the function.
n = 2.0
m = 5.0

# Lambda factors
# Lambda corresponds to the value the function
# asymptotes to as x -> +infinity
ln  = 2.0e+0 # Notch induction by ICD
ldi = 0.0e+0 # Delta inhibition by ICD
ldr = 2.0e+0 # Delta induction by VEGF-VEGFR complex
lj  = 2.0e+0 # Jagged inhibition by ICD
lr  = 0.0e+0 # VEGFR induction by ICD


##################
# Initial values #
##################

# Min/max ranges for initial conditions
Ns = 305.990702465
Ds = 5379.23967769
Js = 2252.70384204
Is = 11.7416033051
Rs = 6643.7680484

Nr = 4085.34764119
Dr = 45.7669946329
Jr = 721.681376215
Ir = 624.162153987
Rr = 620.763683881