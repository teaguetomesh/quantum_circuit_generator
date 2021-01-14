# quantum-circuit-generator
Python package for automated generation of various quantum circuits.

Link to repo:

https://github.com/teaguetomesh/quantum_circuit_generator

## Supported Circuits
 - Google quantum supremacy
 - QAOA ansatzes
 - VQE ansatzes
 - QFT and inverse QFT
 - Quantum Adder
 - Quantum teleportation
 - Superdense coding
 - Quantum Walk (in development)

More information on each of these circuits can be found within each of their respective files, including links to the relevant papers which describe their specification.

## Getting Started

### Prerequisites

Install the qiskit python package via pip.

```
pip install qiskit
```

### Generation Example
To generate circuits using the scripts in this package, first place the entire quantum_circuit_generator directory in your project like so

```
your_project_folder/
    your.py
    scripts.py
    here.py
    quantum_circuit_generator/
```

You can then generate circuits in your scripts.
As an example, inside scripts.py you can generate a 4x4x8 supremacy circuit with the following lines

```
# within script.py
from quantum_circuit_generator.generators import gen_supremacy

circ = gen_supremacy(4,4,8)
print(circ)
```
