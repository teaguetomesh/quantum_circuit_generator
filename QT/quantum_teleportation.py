from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

class QT:
    """
    Generate an instance of the Quantum Teleportation Protocol.

    Attributes
    ----------
    msg : str
        The strand of qubits that is intended to be sent
    barriers : bool
        Choice to include barriers in circuit or not
    circ : QuantumCircuit
        Qiskit QuantumCircuit that represents the circuit
    """

    def __init__(self, msg=None, barriers=True, qrname=None, crname=None):
        if msg is None:
            raise Exception('Provide a message for the Teleportation circuit, example: 10')
        else:
            if type(msg) is int:
                self.msg = str(msg)
            else:
                self.msg = msg
        
        # Set flags for circuit generation
        self.nq = len(msg)
        self.barriers = barriers

        # Setup the registers and the circuit
        if qrname is None:
            self.qr = QuantumRegister(3, name="q")
        else:
            self.qr = QuantumRegister(3, name=qrname)
        self.reg0 = ClassicalRegister(1, name="r0")
        self.reg1 = ClassicalRegister(1, name="r1")
        if crname is None:
            self.cr = ClassicalRegister(self.nq, name="output")
        else:
            self.cr = ClassicalRegister(self.nq, name=crname)
        self.circ = QuantumCircuit(self.qr, self.reg0, self.reg1, self.cr)

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
    
    def _encode(self, psi, a):
        """
        Performs encoding necessary to prepare message to be sent

        Inputs
        ------
        psi : int
            The index of the qubit that the messenger would like to send
        a : int
            The index of the qubit that is entangled with the receiver's
        """
        self.circ.cx(psi, a)
        self.circ.h(psi)

    def _measure(self, a, b):
        """
        Measures qubits a & b on classical registers 0 & 1

        Inputs
        ------
        a : int
            The index of one qubit to measure
        b : int
            The index of a second qubit to measure
        """
        self.circ.measure(a, 0)
        self.circ.measure(b, 1)

    def _decode(self, qubit, reg0, reg1):
        """
        Receiver applies gates depending on the classical bits received

        Inputs
        ------
        qubit : int
            The index of the qubit that will receive the teleported qubit
        reg0 : ClassicalRegister
            The first classical register to be read from
        reg1 : ClassicalRegister
            The second classical register to be read from
        """
        self.circ.z(qubit).c_if(reg0, 1)
        self.circ.x(qubit).c_if(reg1, 1)

    def gen_circuit(self):
        """
        Create a circuit implementing the Quantum Teleportation protocol

        Returns
        -------
        QuantumCircuit
            QuantumCircuit object of size nq
        """

        # Loop over the protocol for every qubit to be teleported from right to left
        for i in reversed(range(self.nq)):

            # Convert q0 to be the qubit to be teleported
            if (self.msg[i] == "1"):
                self.circ.x(0)

            # Create a bell pair between qubits q1 and q2
            self._create_bell_pair(1, 2)
            self.circ.barrier([1, 2])

            # q1 is sent to messenger and q2 goes to receiver

            # Messenger performs their encoding on their qubits
            self._encode(0, 1)
            self.circ.barrier([0, 1])

            # Messenger performs measurements and stores results in classical registers
            self._measure(0, 1)
            self.circ.barrier([1, 2])

            # Messenger sends resulting 2 classical bits to receiver

            # Receiver applies certain gate(s) given classical bits information
            self._decode(2, self.reg0, self.reg1)

            # Receiver then measures q2 to find the qubit teleported to them
            self.circ.measure(2, self.cr[self.nq-i-1])

            # Reset the qubits to 0 for the next iteration if necessary
            if (i > 0):
                self.circ.barrier()
                self.circ.reset(0)
                self.circ.reset(1)
                self.circ.reset(2)
        
        return self.circ