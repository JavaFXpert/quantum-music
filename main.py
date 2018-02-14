from pyquil.quil import Program
from pyquil.quilbase import RawInstr
import pyquil.api as api
from pyquil.gates import *
import numpy as np
from math import *
from gatedefs import *



qvm = api.QVMConnection()
p = Program()

melodic_angles_deg = [225,225,226,227,231,239,270,215,202,195,191,187,184,209,197,191,188,184,208,197,191,186,208,197,189,208,194,205]
harmonic_angles_deg = [216,218,215,217,231,234,270,108,259,107,258,91,234,207,206,197,197,195,200,196,193,191,200,200,195,201,198,205]

melodic_gate_matrix = compute_matrix(melodic_angles_deg)
harmonic_gate_matrix = compute_matrix(harmonic_angles_deg)

p.defgate("MELODIC_GATE", melodic_gate_matrix)
p.defgate("HARMONIC_GATE", harmonic_gate_matrix)

# Initial pitch (0-7 signifying C4, D4, E4, F4, G4, A4, B4, C5)
initial_pitch_index = 0

# Note: code in service will convert initial_pitch_index to the initial gates
p.inst(I(2), I(1), I(0))

# Place initial pitch into Lead Note #1
p.inst(FALSE(0), FALSE(0), FALSE(0))

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

# ---- Produce pitch for Lead Note #2 and replicate measurement results into qubits ----
MELODIC_GATE 2 1 0

MEASURE 2 [5]
MEASURE 1 [4]
MEASURE 0 [3]

JUMP-UNLESS @RESET-Q5 [5]
ACTIVE-SET 5 [63]
JUMP @END-Q5
LABEL @RESET-Q5
ACTIVE-RESET 5 [63]
LABEL @END-Q5 

JUMP-UNLESS @RESET-Q4 [4]
ACTIVE-SET 4 [63]
JUMP @END-Q4
LABEL @RESET-Q4
ACTIVE-RESET 4 [63]
LABEL @END-Q4 

JUMP-UNLESS @RESET-Q3 [3]
ACTIVE-SET 3 [63]
JUMP @END-Q3
LABEL @RESET-Q3
ACTIVE-RESET 3 [63]
LABEL @END-Q3 

# ---- Produce pitch for Lead Note #3 and replicate measurement results into qubits ----
MELODIC_GATE 2 1 0

MEASURE 2 [8]
MEASURE 1 [7]
MEASURE 0 [6]

JUMP-UNLESS @RESET-Q8 [8]
ACTIVE-SET 8 [63]
JUMP @END-Q8
LABEL @RESET-Q8
ACTIVE-RESET 8 [63]
LABEL @END-Q8 

JUMP-UNLESS @RESET-Q7 [7]
ACTIVE-SET 7 [63]
JUMP @END-Q7
LABEL @RESET-Q7
ACTIVE-RESET 7 [63]
LABEL @END-Q7 

JUMP-UNLESS @RESET-Q6 [6]
ACTIVE-SET 6 [63]
JUMP @END-Q6
LABEL @RESET-Q6
ACTIVE-RESET 6 [63]
LABEL @END-Q6 

# ---- Produce pitch for Lead Note #4 and replicate measurement results into qubits ----
MELODIC_GATE 2 1 0

MEASURE 2 [11]
MEASURE 1 [10]
MEASURE 0 [9]

JUMP-UNLESS @RESET-Q11 [11]
ACTIVE-SET 11 [63]
JUMP @END-Q11
LABEL @RESET-Q11
ACTIVE-RESET 11 [63]
LABEL @END-Q11 

JUMP-UNLESS @RESET-Q10 [10]
ACTIVE-SET 10 [63]
JUMP @END-Q10
LABEL @RESET-Q10
ACTIVE-RESET 10 [63]
LABEL @END-Q10 

JUMP-UNLESS @RESET-Q9 [9]
ACTIVE-SET 9 [63]
JUMP @END-Q9
LABEL @RESET-Q9
ACTIVE-RESET 9 [63]
LABEL @END-Q9 

# ---- Produce pitch for Lead Note #5 and replicate measurement results into qubits ----
MELODIC_GATE 2 1 0

MEASURE 2 [14]
MEASURE 1 [13]
MEASURE 0 [12]

JUMP-UNLESS @RESET-Q14 [14]
ACTIVE-SET 14 [63]
JUMP @END-Q14
LABEL @RESET-Q14
ACTIVE-RESET 14 [63]
LABEL @END-Q14 

JUMP-UNLESS @RESET-Q13 [13]
ACTIVE-SET 13 [63]
JUMP @END-Q13
LABEL @RESET-Q13
ACTIVE-RESET 13 [63]
LABEL @END-Q13 

JUMP-UNLESS @RESET-Q12 [12]
ACTIVE-SET 12 [63]
JUMP @END-Q12
LABEL @RESET-Q12
ACTIVE-RESET 12 [63]
LABEL @END-Q12 

# ---- Produce pitch for Lead Note #6 and replicate measurement results into qubits ----
MELODIC_GATE 2 1 0

MEASURE 2 [17]
MEASURE 1 [16]
MEASURE 0 [15]

"""))

print(p)



num_runs = 1
res = qvm.run(p, [2, 1, 0, 5, 4, 3, 8, 7, 6, 11, 10, 9, 14, 13, 12, 17, 16, 15], num_runs)
print(res)


