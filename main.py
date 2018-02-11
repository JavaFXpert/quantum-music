from pyquil.quil import Program
import pyquil.api as api
from pyquil.gates import *
import numpy as np
from math import *
from gatedefs import *



qvm = api.QVMConnection()
p = Program()
p.inst(X(0), Y(1), Z(0))

angles = [180, 90, 127, 144, 148, 167, 171, 180, 126, 90, 131, 141, 172, 180, 180, 174, 123, 152, 180, 180, 136, 145, 90, 90, 138, 180, 123, 125]
#angles = [0] * 28

r = [0] * len(angles)
for i in range(len(angles)):
    r[i] = radians(angles[i])

gate_matrix = compute_matrix(angles)

p = Program().defgate("HARMONY_GATE", gate_matrix)

p.inst(I(2), I(1), X(0)).inst(("HARMONY_GATE", 2, 1, 0)).measure(0, 0).measure(1, 1).measure(2, 2)
print(p)

num_runs = 5
res = qvm.run(p, [2, 1, 0], num_runs)
print(res)


