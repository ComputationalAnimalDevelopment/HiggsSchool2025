'''
Defines simulator class for the cellular automata simulation.
'''
#####################

# installed modules
import numpy as np
from numba import jit

# local modules
from parameters import *
from sim_functions import get_neighbour_average

#####################

@jit(nopython=True)
def HillF(S, s0, n, l):
	'''
	hill function
	'''
	return ( 1. + l*((S/s0)**n) )/( 1. + ((S/s0)**n) )

class Simulator:

	def __init__(self, g):

		self.g = g

		# Arrays for simulation results
		self.N = np.zeros((int(T2/dt)+1, g, g)) # Notch
		self.D = np.zeros((int(T2/dt)+1, g, g)) # Delta
		self.J = np.zeros((int(T2/dt)+1, g, g)) # Jagged
		self.I = np.zeros((int(T2/dt)+1, g, g)) # Notch intracellular domain
		self.R = np.zeros((int(T2/dt)+1, g, g)) # VEGF receptor


	def set_ic(self):
		'''
		Initialize 2D arrays for all variables with randomized initial conditions.
		The maximum ranges are defined in the parameter file.
		'''

		Nrnd, Drnd, Jrnd, Irnd, Rrnd = (np.zeros((self.g, self.g)) for _ in range(5)) 

		for q in range(self.g):
			for w in range(self.g):
				Nrnd[q][w] = np.random.uniform(low=0, high=max(Nr, Ns))
				Drnd[q][w] = np.random.uniform(low=0, high=max(Dr, Ds))
				Jrnd[q][w] = np.random.uniform(low=0, high=max(Jr, Js))
				Irnd[q][w] = np.random.uniform(low=0, high=max(Ir, Is))
				Rrnd[q][w] = np.random.uniform(low=0, high=max(Rr, Rs))

		return Nrnd, Drnd, Jrnd, Irnd, Rrnd
	

	def integrate(self, N, D, J, I, R, tm, dt, Vt_value):
		'''
		Integrate for time tm given initial conditions.
		Calls the updated_signal function to get the average values from neighbours in time t-1.
		Uses the explicit forward Euler method to calculate the new timepoint.
		'''

		Vext = Vt_value

		for _ in range(tm):

			# Get the average values from neighbours in time t-1
			# Default geometry is hexagonal lattice “even-r” horizontal layout with periodic boundaries.
			Next = get_neighbour_average(N)
			Dext = get_neighbour_average(D)
			Jext = get_neighbour_average(J)

			# Calculate new timepoint using explicit forward Euler method
			N = N + dt*( p_N*HillF(I,Ki,n,ln)                              - N*( kt*(Dext+Jext)   + kc*D + kc*J ) - d*N  )
			D = D + dt*( p_D*HillF(I,Ki,n,ldi)*HillF(kt*R*Vext/dI,Kv,n,ldr)- D*( kt*Next          + kc*N )        - d*D  )
			J = J + dt*( p_J*HillF(I,Ki,m,lj)                              - J*( kt*Next          + kc*N )        - d*J  )
			I = I + dt*(                                                         kt*N*(Dext+Jext)                 - dI*I )
			R = R + dt*( p_R*HillF(I,Ki,n,lr)                              - R*  kt*Vext                          - d*R  )

		return N, D, J, I, R
	

	def initialize(self):
		"""
		Initializes the simulation and does a short relaxation run with no external VEGF.
		"""
		Nrnd, Drnd, Jrnd, Irnd, Rrnd  = self.set_ic()

		self.N[0], self.D[0], self.J[0], self.I[0], self.R[0] = self.integrate(Nrnd, Drnd, Jrnd, Irnd, Rrnd, int(T1 / dt), dt, 0.)

	def do_simstep(self, cur_step):
		"""
		Does a single simulation step.
		"""

		N_prev = self.N[cur_step-1] 
		D_prev = self.D[cur_step-1]
		J_prev = self.J[cur_step-1]
		I_prev = self.I[cur_step-1]
		R_prev = self.R[cur_step-1]
		
		N, D, J, I, R = self.integrate(N_prev, D_prev, J_prev, I_prev, R_prev, int(dt/dt), dt, extVEGF)

		self.N[cur_step] = N
		self.D[cur_step] = D
		self.J[cur_step] = J
		self.I[cur_step] = I
		self.R[cur_step] = R

		# Save output
		np.savetxt(f'sim_data/delta_spatial_{int(extVEGF):05d}_{cur_step+1:02d}.txt', D)
		np.savetxt(f'sim_data/notch_spatial_{int(extVEGF):05d}_{cur_step+1:02d}.txt', N)