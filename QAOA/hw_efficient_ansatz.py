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

    """

    def __init__(self, width, depth):
        
        # number of qubits 
        self.nq = width
        # number of layers
        self.d  = depth

	# Create a Quantum and Classical Register.
        self.qr = QuantumRegister(self.nq)
        # It is easier for the circuit cutter to handle circuits
        # without measurement or classical registers
        #c = ClassicalRegister(nb_qubits)
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

        return(theta)


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
        
        theta = self.get_noiseless_theta()

        try:
            # print('Using initial_circuit of the RyRz QAOA')

            # INITIAL PARAMETERIZER
            # layer 1
            for i in range(self.nq):
                self.circ.u3(theta[i], 0, 0, self.qr[i])
            
            # layer 2
            for i in range(self.nq):
                self.circ.u3(0, 0, theta[i+self.nq], self.qr[i])

            self.circ.barrier()

            # For each layer, d, execute an entangler followed by a parameterizer block
            for dd in range(self.d):
                # ENTANGLER
                for i in range(self.nq-1):
                    #qc.h(q[i+1])
                    self.circ.cx(self.qr[i], self.qr[i+1])
                    #qc.h(q[i+1])

                self.circ.barrier()

                # PARAMETERIZER
                # layer 1
                for i in range(self.nq):
                    self.circ.u3(theta[i+2*self.nq], 0, 0, self.qr[i])
            
                # layer 2
                for i in range(self.nq):
                    self.circ.u3(0, 0, theta[i+3*self.nq], self.qr[i])
            
                # self.circ.measure(q,c)
            
            return(self.circ)
        
        except QiskitError as ex:
            print('There was an error in the circuit!. Error = {}'.format(ex))
            sys.exit(2)


if __name__ == "__main__":
    nb_qubits = 8
    hwea = HWEA(8,1)
    qc = gen_circuit
    print(qc)


