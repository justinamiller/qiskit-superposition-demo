import math
from typing import Dict, Tuple
import numpy as np

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def build_swap_test_circuit(
    state_a: np.ndarray, state_b: np.ndarray
) -> QuantumCircuit:
    """
    Build a SWAP-test circuit on |ψ> and |φ> with a single ancilla qubit.
    P(measure ancilla = 0) = (1 + |<ψ|φ>|^2) / 2
    """
    if len(state_a) != len(state_b):
        raise ValueError("Statevectors must have equal length.")
    n = int(math.log2(len(state_a)))
    if 2**n != len(state_a):
        raise ValueError("Statevectors must be power-of-two length.")

    # Layout: [ancilla] [register A (n qubits)] [register B (n qubits)]
    qc = QuantumCircuit(1 + 2*n, 1)

    # Initialize registers A and B
    # A qubits = 1..n, B qubits = n+1..2n
    a_qubits = list(range(1, n + 1))
    b_qubits = list(range(n + 1, 2 * n + 1))

    qc.initialize(state_a, a_qubits)
    qc.initialize(state_b, b_qubits)

    # Put ancilla in superposition
    qc.h(0)

    # Controlled SWAP between each pair of corresponding qubits
    for i in range(n):
        qc.cswap(0, a_qubits[i], b_qubits[i])

    # Interfere ancilla
    qc.h(0)

    # Measure ancilla only
    qc.measure(0, 0)

    return qc

def swap_test_similarity(
    state_a: np.ndarray,
    state_b: np.ndarray,
    shots: int = 8192
) -> Dict[str, float]:
    """
    Run the SWAP test and estimate:
      - p0: probability of ancilla=0
      - fidelity: |<ψ|φ>|^2  (ranges [0,1])
      - overlap: |<ψ|φ>|     (cosine similarity analogue)
    """
    qc = build_swap_test_circuit(state_a, state_b)
    sim = AerSimulator()
    tqc = transpile(qc, sim)
    result = sim.run(tqc, shots=shots).result()
    counts = result.get_counts()
    p0 = counts.get("0", 0) / shots
    fidelity = max(0.0, min(1.0, 2.0 * p0 - 1.0))   # clamp numeric noise
    overlap = math.sqrt(max(0.0, fidelity))
    return {"p0": p0, "fidelity": fidelity, "overlap": overlap}
