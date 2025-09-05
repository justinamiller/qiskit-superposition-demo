Quantum Superposition with Qiskit
This project contains a simple Python script (quantum_superposition.py) that demonstrates the quantum mechanical principle of superposition using IBM's Qiskit framework. It creates a quantum circuit with two qubits, places them both into a state of superposition, and then simulates the measurement outcomes to show their probabilistic nature.

What is Quantum Computing?
Classical computers, like the one you're using now, store and process information using bits, which can be in one of two states: 0 or 1. Quantum computers, on the other hand, use qubits. A qubit is a fundamental unit of quantum information that can exist in a state of 0, 1, or a combination of both at the same time. This ability to be in multiple states simultaneously is a key concept that gives quantum computers their immense potential.

Key Concept: Superposition
Superposition is one of the most fundamental principles of quantum mechanics. It states that, much like waves in physics can be added together, a quantum system can be in multiple states at once until it is measured.

Think of a spinning coin. While it's in the air, it's neither heads nor tails—it's in a dynamic state that encompasses both possibilities. Only when it lands (the "measurement") does it collapse into a definite state of either heads or tails. A qubit in superposition is similar; it exists in a combination of the |0⟩ and |1⟩ states. When we measure it, its superposition collapses, and it will be observed as either a 0 or a 1, with a certain probability for each outcome.

In this script, we use a Hadamard Gate (H), which is a quantum logic gate that puts a qubit into an equal superposition. This means that after applying the H-gate, the qubit has a 50% chance of being measured as a 0 and a 50% chance of being measured as a 1.

What the Code Does
The Python script quantum_superposition.py performs the following steps:

Initialization: It creates a quantum circuit with two qubits and two classical bits. The qubits are automatically initialized to the state |0⟩.

Apply Superposition: A Hadamard (H) gate is applied to each of the two qubits. This puts both of them into an equal superposition of |0⟩ and |1⟩.

Measurement: The state of each qubit is measured. This act of measurement collapses the superposition, forcing each qubit into a definite state of either 0 or 1. The result of each measurement is stored in the corresponding classical bit.

Simulation: The quantum circuit is run on a local simulator 1024 times (called "shots"). Because the outcome of a quantum measurement is probabilistic, we run it many times to see the statistical distribution of the results.

Visualization: The script prints a text-based diagram of the circuit, the final counts for each state, and then uses matplotlib to plot a histogram showing the frequency of each possible outcome.

Prerequisites
Python 3.x

pip (Python package installer)

Installation
Clone this repository or download the quantum_superposition.py file.

Open your terminal or command prompt.

Install the required Python libraries:

pip install qiskit qiskit-aer matplotlib

How to Run the Script
Navigate to the directory containing the file and run the following command in your terminal:

python quantum_superposition.py

Expected Output
When you run the script, you will see:

A text-based diagram of the quantum circuit.

The results of the simulation, showing the counts for each of the four possible states ('00', '01', '10', '11').

A pop-up window displaying a histogram.

Because both qubits are in an equal superposition, all four outcomes are equally likely. Therefore, the histogram should show four bars of roughly equal height, with each outcome appearing approximately 25% of the time (around 256 out of 1024 shots).

This result demonstrates that until measured, the two-qubit system existed in a superposition of all four possible classical states.
