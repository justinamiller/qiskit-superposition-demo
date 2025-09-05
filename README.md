# quantum-similarity

**Quantum superposition for evaluating two elements** — this project demonstrates how **quantum superposition** can be applied to compare two classical objects (numeric vectors or raw text). It uses the **SWAP test** to measure similarity between the quantum states that represent each element.

---

## What is Superposition?

In classical computing, a bit is either **0** or **1**. In quantum computing, a **qubit** can be in a state that is a *superposition* of both 0 and 1 at the same time:

```
|ψ⟩ = α|0⟩ + β|1⟩
```

where `α` and `β` are complex numbers representing probabilities.  
Superposition allows quantum computers to evaluate multiple possibilities *in parallel* within a single computation.

---

## How this code uses Superposition

1. **Ancilla qubit**: We create an extra "control" qubit and put it into superposition using a Hadamard gate.
2. **Two registers**: We encode two classical elements (vectors or text features) into separate quantum registers.
3. **SWAP test**: The ancilla qubit, in superposition, controls whether we swap these two registers or not.
4. **Interference**: Measuring the ancilla after interference reveals the similarity between the two states.

The outcome probability directly encodes **how similar the two elements are**:
- If the elements are identical, the ancilla almost always measures `0`.
- If they are completely different, the ancilla measures `0` only about half the time.

---

## Real-World Examples of Superposition

- **Document Deduplication**  
  Detect whether two documents are nearly the same (e.g., detecting duplicate support tickets).

- **Genomics**  
  Compare DNA sequences represented as vectors. Superposition lets the circuit test similarity in one coherent operation.

- **Recommender Systems**  
  Compare user preference vectors with product feature vectors to quickly evaluate closeness.

- **Anomaly Detection**  
  Compare an incoming data vector against a baseline "normal" vector to see if it deviates significantly.

These use cases illustrate how **evaluating multiple possibilities simultaneously** (enabled by superposition) can accelerate or simplify certain tasks.

---

## Installation

```bash
pip install -e .
```

---

## CLI Usage

### Compare vectors

```bash
qsim vectors "[1,2,3,4]" "[1,2,3,5]"
```

### Compare text

```bash
qsim text --text1 "Kubernetes scaling with autoscaling" \
          --text2 "Autoscaling strategies for Kubernetes workloads"
```

---

## Output Example

```json
{
  "mode": "vectors",
  "n_qubits_per_register": 2,
  "shots": 8192,
  "p0": 0.92,
  "fidelity": 0.84,
  "overlap": 0.9165
}
```

- **p0**: Probability of ancilla = 0  
- **fidelity**: Squared similarity between states  
- **overlap**: Similarity metric comparable to cosine similarity
