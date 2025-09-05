import math
from typing import List, Tuple
import numpy as np

def next_power_of_two(n: int) -> int:
    if n <= 1:
        return 1
    return 1 << (n - 1).bit_length()

def normalize_vector(vec: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(vec)
    if norm == 0:
        raise ValueError("Cannot normalize a zero vector.")
    return vec / norm

def vector_to_statevector(vec: List[float]) -> Tuple[np.ndarray, int]:
    """
    Convert an arbitrary real-valued vector into a valid quantum statevector:
      - zero-pad to length 2^n
      - L2-normalize
      - return (statevector, n_qubits)
    """
    arr = np.array(vec, dtype=float).flatten()
    target_len = next_power_of_two(len(arr))
    if target_len != len(arr):
        arr = np.pad(arr, (0, target_len - len(arr)))
    arr = normalize_vector(arr)
    n_qubits = int(math.log2(len(arr)))
    return arr.astype(complex), n_qubits
