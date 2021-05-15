from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import plot_histogram

class SDC:
    """
    Generate an instance of the Superdense Coding Protocol.

    Attributes
    ----------
    msg : str
        The classical message that is intended to be sent
    barriers : bool
        Choice to include barriers in circuit or not
    circ : QuantumCircuit
        Qiskit QuantumCircuit that represents the circuit
    """

    def __init__(self, msg=None, barriers=True, measure=True):
        if msg is None:
            raise Exception('Provide a message for the Superdense Coding circuit, example: 10')
        else:
            if type(msg) is int:
                self.msg = str(msg)
            else:
                self.msg = msg
        
        # Set flags for circuit generation
        self.nq = len(msg)
        if ((self.nq % 2) != 0):
            self.msg = "0" + msg
            self.nq += 1
        self.barriers = barriers
        self.measure = measure

        # Create a QuantumCircuit object with correct number of qubits
        self.circ = QuantumCircuit(self.nq, self.nq)

    def _create_bell_pair(self, a, b):
        """
        Performs a bell measurement on two qubits

        Inputs
        ------
        a : int
            Left most qubit position
        b : int
            Right most qubit position
        """
        self.circ.h(a)
        self.circ.cx(a, b)
    
    def _encode(self, qubit, msg):
        """
        Encodes message onto a given qubit

        Inputs
        ------
        qubit : int
            Index of the qubit that the message will be encoded on
        """
        if msg == "00":
            pass               # To send 00, we apply Identity gate (do nothing)
        elif msg == "10":
            self.circ.x(qubit) # To send 10, we apply X-gate
        elif msg == "01":
            self.circ.z(qubit) # To send 01, we apply Z-gate
        elif msg == "11":
            self.circ.z(qubit) # To send 11, first we apply Z-gate
            self.circ.x(qubit) # Then we apply X-gate
        else:
            print("Invalid Message: Sending '00'")
    
    def _bell_state_measurement(self, a, b):
        """
        Decodes message by performing bell state measurement

        Inputs
        ------
        a : int
            Left most qubit position
        b : int
            Right most qubit position
        """
        self.circ.cx(a, b)
        self.circ.h(a)

    def gen_circuit(self):
        """
        Create a circuit implementing the Superdense Coding protocol

        Returns
        -------
        QuantumCircuit
            QuantumCircuit object of size nq
        """
        # Create bell pairs for all n/2 pairs
        for i in range(0, self.nq, 2):
            self._create_bell_pair(i, i+1)
            if (self.barriers): 
                self.circ.barrier([i, i+1])

        # At this point, all even number qubits are sent to messenger and odd to receiver

        # Messenger encodes their message onto their qubit(s)
        for i in range(0, self.nq, 2):
            curr_msg = self.msg[self.nq-i-2] + self.msg[self.nq-i-1]
            self._encode(i, curr_msg)
            if (self.barriers): 
                self.circ.barrier([i, i+1])

        # Messenger then sends their encoded qubit(s) to receiver

        # Receiver decodes the qubit(s) sent from the messenger
        for i in range(0, self.nq, 2):
            self._bell_state_measurement(i, i+1)
        
        # Receiver measures their qubits to read the messenger's message
        for i in range(0, self.nq, 2):
            self.circ.barrier([i, i+1])
            
            if (self.measure):
                self.circ.measure(i, i)
                self.circ.measure(i+1, i+1)

        return self.circ