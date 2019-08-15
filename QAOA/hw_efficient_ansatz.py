import sys
import numpy as np
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, QiskitError


class HWEA:
    """
    Class to implement a hardware efficient ansatz for the QAOA algorithm.
    Based on the community detection circuit implemented by Francois-Marie Le Régent.
    This ansatz uses the entangler+rotation block structure like that described
    in the paper by Nikolaj Moll et al. (http://iopscience.iop.org/article/10.1088/2058-9565/aab822)

    A HW efficient ansatz circuit can be generated with an instance of this class
    by calling its gen_circuit() method.

    Attributes
    ----------
    nq : int
        number of qubits
    d : int
        number of layers to apply. Where a layer = rotation block + entangler block
        This is also the same as the "P" value often referenced for QAOA.
    parameters : str
        optional string which changes the rotation angles in the rotation block
        [optimal, random, seeded]
    seed : int
        a number to seed the number generator with
    barriers : bool
        should barriers be included in the generated circuit
    measure : bool
        should a classical register & measurement be added to the circuit
    regname : str
        optional string to name the quantum and classical registers. This
        allows for the easy concatenation of multiple QuantumCircuits.
    qr : QuantumRegister
        Qiskit QuantumRegister holding all of the quantum bits
    cr : ClassicalRegister
        Qiskit ClassicalRegister holding all of the classical bits
    circ : QuantumCircuit
        Qiskit QuantumCircuit that represents the hardware-efficient ansatz
    """

    def __init__(self, width, depth, parameters='optimal', seed=None,
                 barriers=False, measure=False, regname=None):

        # number of qubits
        self.nq = width
        # number of layers
        self.d  = depth

        # set flags for circuit generation
        self.parameters = parameters
        self.seed = seed
        self.barriers = barriers
        self.measure = measure

	# Create a Quantum and Classical Register.
        if regname is None:
            self.qr = QuantumRegister(self.nq)
            self.cr = ClassicalRegister(self.nq)
        else:
            self.qr = QuantumRegister(self.nq, name=regname)
            self.cr = ClassicalRegister(self.nq, name='c'+regname)
        # It is easier for the circuit cutter to handle circuits
        # without measurement or classical registers
        if self.measure:
            self.circ = QuantumCircuit(self.qr, self.cr)
        else:
            self.circ = QuantumCircuit(self.qr)


    def get_noiseless_theta(self):
        """
        Get the value of the optimal parameter for the noiseless case

        This method returns a vector of length 4*n if n is the number of 
        qubits in the circuit. It consists of a first Rotation of pi/2 
        on the first qubit then linear entangler and finally rotations 
        of pi on the first half of the qubits

        Parameters
        ----------
        nb_qubits : int
            Number of qubits in the circuit

        Returns
        -------
        list
            vector of length 4*nb_qubits
        """

        theta = [np.pi/2] + [0]*(2*self.nq-1) + [np.pi]*int(self.nq/2) + [0]*int(1.5*self.nq)

        return theta


    def get_random_theta(self):

        if self.parameters == 'seeded':
            if self.seed is None:
                raise Exception('A valid seed must be provided')
            else:
                np.random.seed(self.seed)

        theta = np.random.uniform(-np.pi, np.pi, 4*self.nq)

        return theta


    def gen_circuit(self):
        """
        Create a circuit for the QAOA RyRz ansatz

        This methods generates a circuit which consists of 2 parameterized 
        rotation columns, linear entanglement of all the qubits and finally 
        2 parameterized rotation columns.

        Returns
        -------
        QuantumCircuit
            QuantumCircuit of size nb_qubits with no ClassicalRegister and no measurements

        QiskitError
            Prints the error in the circuit
        """

        if self.parameters == 'optimal':
            theta = self.get_noiseless_theta()
        elif   self.parameters in ['random', 'seeded']:
            theta = self.get_random_theta()
        else:
            raise Exception('Unknown parameter option: {}'.format(self.parameters))

        try:
            # print('Using initial_circuit of the RyRz QAOA')

            # INITIAL PARAMETERIZER
            # layer 1
            for i in range(self.nq):
                self.circ.u3(theta[i], 0, 0, self.qr[i])

            # layer 2
            for i in range(self.nq):
                self.circ.u3(0, 0, theta[i+self.nq], self.qr[i])

            if self.barriers:
                self.circ.barrier()

            # For each layer, d, execute an entangler followed by a parameterizer block
            for dd in range(self.d):
                # ENTANGLER
                for i in range(self.nq-1):
                    #qc.h(q[i+1])
                    self.circ.cx(self.qr[i], self.qr[i+1])
                    #qc.h(q[i+1])

                if self.barriers:
                    self.circ.barrier()

                # PARAMETERIZER
                # layer 1
                for i in range(self.nq):
                    self.circ.u3(theta[i+2*self.nq], 0, 0, self.qr[i])

                # layer 2
                for i in range(self.nq):
                    self.circ.u3(0, 0, theta[i+3*self.nq], self.qr[i])

            # place measurements on the end of the circuit
            if self.measure:
                self.circ.barrier()
                self.circ.measure(self.qr,self.cr)

            return self.circ

        except QiskitError as ex:
            raise Exception('There was an error in the circuit!. Error = {}'.format(ex))


if __name__ == "__main__":
    nb_qubits = 8
    hwea = HWEA(8,1)
    qc = gen_circuit
    print(qc)


