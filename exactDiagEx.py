"""
Sample code for using applyHam.py and genLocalHams.py 

This code performs the exact diagonalization of a finite one-dimensional 
quantum lattice where sites interact locally. 

The quantum XX model and the Ising model can be solved analytically (e.g., see
calculation below) and used to verify the numerical results.

"""

import numpy as np
from scipy.sparse.linalg import LinearOperator, eigsh
from timeit import default_timer as timer
from genLocalHams import genLocalHams
from applyHam import applyHam

# Simulation parameters
model = 'rand-homog-c' # see genLocalHams.py for options
Nsites = 16 # number of lattice sites
usePBC = True # use periodic or open boundaries
d = 2 # local dimension
n = 2 # interaction length
numval = 1 # number of eigenstates to compute

# Calculate exact analytical solution (only for ground state with PBCs)
if model == 'XX-G' and usePBC and numval == 1:
  energy_exact = -4 / np.sin(np.pi / Nsites)  
elif model == 'Ising-G' and usePBC and numval == 1:
  energy_exact = -2 / np.sin(np.pi / (2 * Nsites))

# Generate Hamiltonian as list of local terms    
hloc = genLocalHams(model, Nsites, usePBC, d, n)

# Cast the Hamiltonian 'H' as a linear operator
# This defines the matrix (Hamiltonian) by its action on a vector rather than 
# by its explicit matrix entries. This makes solving for eigenvalues much
# more efficient and practical for large matrices
def applyLocalHamClosed(psiIn):
    return applyHam(psiIn, hloc, Nsites, usePBC, d, n)

H = LinearOperator((d**Nsites, d**Nsites), matvec=applyLocalHamClosed)

# Perform the exact diagonalization
start_time = timer()
E, psi = eigsh(H, k=numval, which='SA')
diag_time = timer() - start_time

# Check against exact energy if applicable
if (model == 'XX-G' or model == 'Ising-G') and usePBC and numval == 1:
    energy_error = E[0] - energy_exact  # should equal to zero
    print('N: %d, time: %.2f s, energy: %.4e, exact energy: %.4e, error: %1.0e'
           % (Nsites, diag_time, E[0], energy_exact, energy_error))

else:
    print('N: %d, time: %.2f s, energy %.4e' % (Nsites, diag_time, E[numval-1]))

