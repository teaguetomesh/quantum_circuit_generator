from qiskit import QuantumCircuit, QuantumRegister
import sys
import math
import numpy as np


class QWALK:
    """
    Class to implement the Quantum Walk algorithm as described
    in Childs et al. (https://arxiv.org/abs/quant-ph/0209131)

    A circuit implementing the quantum walk can be generated for a given
    instance of a problem parameterized by N (i.e. # of vertices in a graph)
    by calling the gen_circuit() method.

    Attributes
    ----------
    N : int
        number of vertices in the graph we want to perform the quantum walk on
    barriers : bool
        should barriers be included in the generated circuit
    regname : str
        optional string to name the quantum and classical registers. This
        allows for the easy concatenation of multiple QuantumCircuits.
    qr : QuantumRegister
        Qiskit QuantumRegister holding all of the quantum bits
    circ : QuantumCircuit
        Qiskit QuantumCircuit that represents the uccsd circuit
    """

    def __init__(self, N, barriers=False, regname=None):

        # number of vertices
        self.N = N

        # set flags for circuit generation
        self.barriers = barriers
        self.k = self.gen_coloring()

        # create a QuantumCircuit object
        if regname is None:
            self.qr = QuantumRegister(self.nq)
        else:
            self.qr = QuantumRegister(self.nq, name=regname)
        self.circ = QuantumCircuit(self.qr)

    def gen_coloring(self):
        """
        Generate a coloring for the graph

        k = poly(log(N))
        """

        self.k = 4


    def Vc(self, c):
        """
        Apply the Vc gate to the circuit
        """


    def evolve_T(self, t):
        """
        Simulate the evolution of exp(-iTt)
        """


    def gen_circuit(self):
        """
        Create a circuit implementing the quantum walk algorithm

        Returns
        -------
        QuantumCircuit
            QuantumCircuit object of size nq with no ClassicalRegister and
            no measurements
        """

        t = 1

        for c in range(k):
            self.Vc(c)
            self.evolve_T(t)
            self.Vc(c)

        return self.circ



