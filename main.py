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

# == Produce melody ==
# ---- Produce pitch for Lead Note #2 and replicate measurement results into qubits ----
MELODIC_GATE 2 1 0

MEASURE 2 [5]
MEASURE 1 [4]
MEASURE 0 [3]

JUMP-UNLESS @RESET-Q5 [5]
ACTIVE-SET 2 [63]
JUMP @END-Q5
LABEL @RESET-Q5
ACTIVE-RESET 5 [63]
LABEL @END-Q5 

JUMP-UNLESS @RESET-Q4 [4]
ACTIVE-SET 1 [63]
JUMP @END-Q4
LABEL @RESET-Q4
ACTIVE-RESET 4 [63]
LABEL @END-Q4 

JUMP-UNLESS @RESET-Q3 [3]
ACTIVE-SET 0 [63]
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
ACTIVE-SET 2 [63]
JUMP @END-Q8
LABEL @RESET-Q8
ACTIVE-RESET 2 [63]
LABEL @END-Q8 

JUMP-UNLESS @RESET-Q7 [7]
ACTIVE-SET 1 [63]
JUMP @END-Q7
LABEL @RESET-Q7
ACTIVE-RESET 1 [63]
LABEL @END-Q7 

JUMP-UNLESS @RESET-Q6 [6]
ACTIVE-SET 0 [63]
JUMP @END-Q6
LABEL @RESET-Q6
ACTIVE-RESET 0 [63]
LABEL @END-Q6 

# ---- Produce pitch for Lead Note #4 and replicate measurement results into qubits ----
MELODIC_GATE 2 1 0

MEASURE 2 [11]
MEASURE 1 [10]
MEASURE 0 [9]

JUMP-UNLESS @RESET-Q11 [11]
ACTIVE-SET 2 [63]
JUMP @END-Q11
LABEL @RESET-Q11
ACTIVE-RESET 2 [63]
LABEL @END-Q11 

JUMP-UNLESS @RESET-Q10 [10]
ACTIVE-SET 1 [63]
JUMP @END-Q10
LABEL @RESET-Q10
ACTIVE-RESET 1 [63]
LABEL @END-Q10 

JUMP-UNLESS @RESET-Q9 [9]
ACTIVE-SET 0 [63]
JUMP @END-Q9
LABEL @RESET-Q9
ACTIVE-RESET 0 [63]
LABEL @END-Q9 

# ---- Produce pitch for Lead Note #5 and replicate measurement results into qubits ----
MELODIC_GATE 2 1 0

MEASURE 2 [14]
MEASURE 1 [13]
MEASURE 0 [12]

JUMP-UNLESS @RESET-Q14 [14]
ACTIVE-SET 2 [63]
JUMP @END-Q14
LABEL @RESET-Q14
ACTIVE-RESET 2 [63]
LABEL @END-Q14 

JUMP-UNLESS @RESET-Q13 [13]
ACTIVE-SET 1 [63]
JUMP @END-Q13
LABEL @RESET-Q13
ACTIVE-RESET 1 [63]
LABEL @END-Q13 

JUMP-UNLESS @RESET-Q12 [12]
ACTIVE-SET 0 [63]
JUMP @END-Q12
LABEL @RESET-Q12
ACTIVE-RESET 0 [63]
LABEL @END-Q12 

# ---- Produce pitch for Lead Note #6 and replicate measurement results into qubits ----
MELODIC_GATE 2 1 0

MEASURE 2 [17]
MEASURE 1 [16]
MEASURE 0 [15]

JUMP-UNLESS @RESET-Q17 [17]
ACTIVE-SET 2 [63]
JUMP @END-Q17
LABEL @RESET-Q17
ACTIVE-RESET 2 [63]
LABEL @END-Q17 

JUMP-UNLESS @RESET-Q16 [16]
ACTIVE-SET 1 [63]
JUMP @END-Q16
LABEL @RESET-Q16
ACTIVE-RESET 1 [63]
LABEL @END-Q16 

JUMP-UNLESS @RESET-Q15 [15]
ACTIVE-SET 0 [63]
JUMP @END-Q15
LABEL @RESET-Q15
ACTIVE-RESET 0 [63]
LABEL @END-Q15 

# ---- Produce pitch for Lead Note #7 and replicate measurement results into qubits ----
MELODIC_GATE 2 1 0

MEASURE 2 [20]
MEASURE 1 [19]
MEASURE 0 [18]

# == Produce harmony ==
# ---- Retrieve pitch for Lead Note #1, replicate it into qubits, and produce pitch for Harmony Note #1a ----
JUMP-UNLESS @RESET-Q2a [2]
ACTIVE-SET 2 [63]
JUMP @END-Q2a
LABEL @RESET-Q2a
ACTIVE-RESET 2 [63]
LABEL @END-Q2a 

JUMP-UNLESS @RESET-Q1a [1]
ACTIVE-SET 1 [63]
JUMP @END-Q1a
LABEL @RESET-Q1a
ACTIVE-RESET 1 [63]
LABEL @END-Q1a 

JUMP-UNLESS @RESET-Q0a [0]
ACTIVE-SET 0 [63]
JUMP @END-Q0a
LABEL @RESET-Q0a
ACTIVE-RESET 0 [63]
LABEL @END-Q0a 

HARMONIC_GATE 2 1 0

MEASURE 2 [23]
MEASURE 1 [22]
MEASURE 0 [21]

# ---- Replicate Harmony Note #1a into qubits, and produce pitch for Harmony Note #1b ----
JUMP-UNLESS @RESET-Q23 [23]
ACTIVE-SET 2 [63]
JUMP @END-Q23
LABEL @RESET-Q23
ACTIVE-RESET 2 [63]
LABEL @END-Q23 

JUMP-UNLESS @RESET-Q22 [22]
ACTIVE-SET 1 [63]
JUMP @END-Q22
LABEL @RESET-Q22
ACTIVE-RESET 1 [63]
LABEL @END-Q22 

JUMP-UNLESS @RESET-Q21 [21]
ACTIVE-SET 0 [63]
JUMP @END-Q21
LABEL @RESET-Q21
ACTIVE-RESET 0 [63]
LABEL @END-Q21 

MELODIC_GATE 2 1 0

MEASURE 2 [44]
MEASURE 1 [43]
MEASURE 0 [42]

# ---- Retrieve pitch for Lead Note #2, replicate it into qubits, and produce pitch for Harmony Note #2a ----
JUMP-UNLESS @RESET-Q5a [5]
ACTIVE-SET 2 [63]
JUMP @END-Q5a
LABEL @RESET-Q5a
ACTIVE-RESET 2 [63]
LABEL @END-Q5a 

JUMP-UNLESS @RESET-Q4a [4]
ACTIVE-SET 1 [63]
JUMP @END-Q4a
LABEL @RESET-Q4a
ACTIVE-RESET 1 [63]
LABEL @END-Q4a 

JUMP-UNLESS @RESET-Q3a [3]
ACTIVE-SET 0 [63]
JUMP @END-Q3a
LABEL @RESET-Q3a
ACTIVE-RESET 0 [63]
LABEL @END-Q3a 

HARMONIC_GATE 2 1 0

MEASURE 2 [26]
MEASURE 1 [25]
MEASURE 0 [24]

# ---- Replicate Harmony Note #2a into qubits, and produce pitch for Harmony Note #2b ----
JUMP-UNLESS @RESET-Q26 [26]
ACTIVE-SET 2 [63]
JUMP @END-Q26
LABEL @RESET-Q26
ACTIVE-RESET 2 [63]
LABEL @END-Q26 

JUMP-UNLESS @RESET-Q25 [25]
ACTIVE-SET 1 [63]
JUMP @END-Q25
LABEL @RESET-Q25
ACTIVE-RESET 1 [63]
LABEL @END-Q25 

JUMP-UNLESS @RESET-Q24 [24]
ACTIVE-SET 0 [63]
JUMP @END-Q24
LABEL @RESET-Q24
ACTIVE-RESET 0 [63]
LABEL @END-Q24 

MELODIC_GATE 2 1 0

MEASURE 2 [47]
MEASURE 1 [46]
MEASURE 0 [45]

# ---- Retrieve pitch for Lead Note #3, replicate it into qubits, and produce pitch for Harmony Note #3a ----
JUMP-UNLESS @RESET-Q8a [8]
ACTIVE-SET 2 [63]
JUMP @END-Q8a
LABEL @RESET-Q8a
ACTIVE-RESET 2 [63]
LABEL @END-Q8a 

JUMP-UNLESS @RESET-Q7a [7]
ACTIVE-SET 1 [63]
JUMP @END-Q7a
LABEL @RESET-Q7a
ACTIVE-RESET 1 [63]
LABEL @END-Q7a 

JUMP-UNLESS @RESET-Q6a [6]
ACTIVE-SET 0 [63]
JUMP @END-Q6a
LABEL @RESET-Q6a
ACTIVE-RESET 0 [63]
LABEL @END-Q6a 

HARMONIC_GATE 2 1 0

MEASURE 2 [29]
MEASURE 1 [28]
MEASURE 0 [27]

# ---- Replicate Harmony Note #3a into qubits, and produce pitch for Harmony Note #3b ----
JUMP-UNLESS @RESET-Q29 [29]
ACTIVE-SET 2 [63]
JUMP @END-Q29
LABEL @RESET-Q29
ACTIVE-RESET 2 [63]
LABEL @END-Q29 

JUMP-UNLESS @RESET-Q28 [28]
ACTIVE-SET 1 [63]
JUMP @END-Q28
LABEL @RESET-Q28
ACTIVE-RESET 1 [63]
LABEL @END-Q28 

JUMP-UNLESS @RESET-Q27 [27]
ACTIVE-SET 0 [63]
JUMP @END-Q27
LABEL @RESET-Q27
ACTIVE-RESET 0 [63]
LABEL @END-Q27 

MELODIC_GATE 2 1 0

MEASURE 2 [50]
MEASURE 1 [49]
MEASURE 0 [48]

"""))

print(p)



num_runs = 1
res = qvm.run(p, [2, 1, 0,     23, 22, 21,   44, 43, 42,
                  5, 4, 3,     26, 25, 24,   47, 46, 45,
                  8, 7, 6,     29, 28, 27,   50, 49, 48,
                  11, 10, 9,   32, 31, 30,   53, 52, 51,
                  14, 13, 12,  35, 34, 33,   56, 55, 54,
                  17, 16, 15,  38, 37, 36,   59, 58, 57,
                  20, 19, 18,  41, 40, 39,   62, 61, 60], num_runs)
print(res)


