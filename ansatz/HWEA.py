import math
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister


class HWEA:
    """

    Attributes
    ----------
    """

    def __init__(self, width, depth):

        self.nq = width
        self.d  = depth

        self.qreg = QuantumRegister(width, 'qreg')
        self.creg = ClassicalRegister(width, 'creg')
        # It is easier to interface with the circuit cutter
        # if there is no Classical Register added to the circuit
        # self.circ = QuantumCircuit(self.qreg, self.creg)
        self.circ = QuantumCircuit(self.qreg)

    
    def gen_circuit(self):
        print('Generating {} qubit HW efficient ansatz with {} layers'.format(self.nq, self.d))

        # apply initial rotations
        pi = math.pi
        ry_angles = [n*pi/8 for n in range(self.nq)]
        for i in range(self.nq):
            self.circ.ry(ry_angles[i],self.qreg[i])

        # apply Entangler block + Rotation block = D - times
        for dd in range(self.d):
            self.circ.h(self.qreg[0])
            for i in range(0, self.nq-1):
                self.circ.cx(self.qreg[i],self.qreg[i+1])
            
            self.circ.barrier()

            for i in range(0, self.nq):
                self.circ.ry(ry_angles[i],self.qreg[i])

        return self.circ

