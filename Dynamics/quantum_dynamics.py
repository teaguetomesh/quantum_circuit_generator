from qiskit import QuantumCircuit, QuantumRegister
import sys
import math
import numpy as np


class Dynamics:
    """
    Class to implement the simulation of quantum dynamics as described
    in Section 4.7 of Nielsen & Chuang (Quantum computation and quantum
    information (10th anniv. version), 2010.)

    A circuit implementing the quantum simulation can be generated for a given
    problem Hamiltonian parameterized by calling the gen_circuit() method.

    Attributes
    ----------
    H : ??
        The given Hamiltonian whose dynamics we want to simulate
    barriers : bool
        should barriers be included in the generated circuit
    measure : bool
        should a ClassicalRegister and measurements be added to the circuit
    regname : str
        optional string to name the quantum and classical registers. This
        allows for the easy concatenation of multiple QuantumCircuits.
    qr : QuantumRegister
        Qiskit QuantumRegister holding all of the quantum bits
    circ : QuantumCircuit
        Qiskit QuantumCircuit that represents the uccsd circuit
    """

    def __init__(self, H, barriers=False, measure=False, regname=None):

        # number of vertices
        self.H = H

        # set flags for circuit generation
        self.barriers = barriers
        self.nq = self.get_num_qubits()

        # create a QuantumCircuit object
        if regname is None:
            self.qr = QuantumRegister(self.nq)
        else:
            self.qr = QuantumRegister(self.nq, name=regname)
        self.circ = QuantumCircuit(self.qr)

        # Create and add an ancilla register to the circuit
        self.ancQ = QuantumRegister(1, 'ancQ')
        self.circ.add_register(self.ancQ)


    def get_num_qubits(self):
        """
        Given the problem Hamiltonian, return the appropriate number of qubits
        needed to simulate its dynamics.

        This number does not include the single ancilla qubit that is added
        to the circuit.
        """
        return 3


    def apply_phase_shift(self, delta_t):
        """
        Simulate the evolution of exp(-i(dt)Z)
        """
        # apply CNOT ladder -> compute parity
        for i in range(self.nq):
            self.circ.cx(self.qr[i], self.ancQ[0])

        # apply phase shift to the ancilla
        self.circ.rz(delta_t, self.ancQ[0])

        # apply CNOT ladder -> uncompute parity
        for i in range(self.nq-1, -1, -1):
            self.circ.cx(self.qr[i], self.ancQ[0])



    def gen_circuit(self):
        """
        Create a circuit implementing the quantum dynamics simulation

        Returns
        -------
        QuantumCircuit
            QuantumCircuit object of size nq with no ClassicalRegister and
            no measurements
        """

        self.apply_phase_shift(0.1)

        return self.circ



