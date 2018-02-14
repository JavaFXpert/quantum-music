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
p.inst(RawInstr("""
DEFCIRCUIT CLEAR q scratch_bit:
    MEASURE q scratch_bit
    JUMP-UNLESS @end scratch_bit
    X q
    LABEL @end
"""))

p.inst(I(2), X(1), X(0))

p.inst(RawInstr("""
CLEAR 0 [4]
"""))

p.inst(("ACCOMPANY_GATE", 2, 1, 0))
p.measure(0, 0).measure(1, 1).measure(2, 2)
print(p)

num_runs = 1
res = qvm.run(p, [2, 1, 0], num_runs)
print(res)


