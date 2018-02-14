from pyquil.quil import Program
from pyquil.quilbase import RawInstr
import pyquil.api as api
from pyquil.gates import *
import numpy as np
from math import *
from gatedefs import *



qvm = api.QVMConnection()
p = Program()

angles = [225,225,226,227,231,239,270,215,202,195,191,187,184,209,197,191,188,184,208,197,191,186,208,197,189,208,194,205]

r = [0] * len(angles)
for i in range(len(angles)):
    r[i] = radians(angles[i])

gate_matrix = compute_matrix(angles)

p.defgate("ACCOMPANY_GATE", gate_matrix)
p.inst(I(2), X(1), X(0))

p.inst(RawInstr("""
DEFCIRCUIT ACTIVE-RESET q scratch_bit:
    MEASURE q scratch_bit
    JUMP-UNLESS @END-ACTIVE-SET scratch_bit
    X q
    LABEL @END-ACTIVE-SET

DEFCIRCUIT ACTIVE-SET q scratch_bit:
    MEASURE q scratch_bit
    JUMP-WHEN @END-ACTIVE-RESET scratch_bit
    X q
    LABEL @END-ACTIVE-RESET

ACCOMPANY_GATE 2 1 0

MEASURE 2 [2]
MEASURE 1 [1]
MEASURE 0 [0]

# Replicate the measurement results into qubits
JUMP-UNLESS @RESET-Q2 [2]
ACTIVE-SET 2 [63]
JUMP @END-Q2
LABEL @RESET-Q2
ACTIVE-RESET 2 [63]
LABEL @END-Q2 

JUMP-UNLESS @RESET-Q1 [1]
ACTIVE-SET 1 [63]
JUMP @END-Q1
LABEL @RESET-Q1
ACTIVE-RESET 1 [63]
LABEL @END-Q1 

JUMP-UNLESS @RESET-Q0 [0]
ACTIVE-SET 0 [63]
JUMP @END-Q0
LABEL @RESET-Q0
ACTIVE-RESET 0 [63]
LABEL @END-Q0 

ACCOMPANY_GATE 2 1 0

MEASURE 2 [5]
MEASURE 1 [4]
MEASURE 0 [3]
"""))

print(p)



num_runs = 1
res = qvm.run(p, [2, 1, 0, 5, 4, 3], num_runs)
print(res)


