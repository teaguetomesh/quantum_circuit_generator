from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

class QT:
    """
    Generate an instance of the Quantum Teleportation Protocol.
    
    Attributes
    ----------
    msg : List of Statevectors
        The strand of 1-qubit state vectors that is intended to be sent
    barriers : bool
        Choice to include barriers in circuit or not
    measure : bool
        Choice to measure the teleported qubit at the end or not
    qrname : string
        Name of quantum registers
    crname : string
        Name of classical register holding all teleported bits
    circ : QuantumCircuit
        Qiskit QuantumCircuit that represents the circuit
    """
    
    def __init__(self, msg=None, barriers=True, measure=True, qrname=None, crname=None):
        if msg is None:
            raise Exception('Provide list of Statevectors for the Teleportation circuit')
        self.msg = msg
        
        # Set flags for circuit generation
        self.nq = len(msg)
        self.barriers = barriers
        self.measure = measure
        
        # Set up the registers and the circuit
        num_qr = 3*self.nq
        num_cr = 2*self.nq
        if qrname is None:
            self.qr = QuantumRegister(num_qr, name="q")
        else:
            self.qr = QuantumRegister(num_qr, name=qrname)
        self.circ = QuantumCircuit(self.qr)
        self.cr = []
        for i in range(num_cr):
            self.cr.append(ClassicalRegister(1))
            self.circ.add_register(self.cr[i])
        if crname is None:
            self.circ.add_register(ClassicalRegister(self.nq, name="output"))
        else:
            self.circ.add_register(ClassicalRegister(self.nq, name=crname))
    
    def _create_bell_pair(self, a, b):
        """
        Creates a bell pair
        
        Inputs
        ------
        a : int
            Left most qubit position
        b : int
            Right most qubit position
        """
        self.circ.h(a)
        self.circ.cx(a, b)
    
    def _bell_state_measurement(self, psi, a):
        """
        Performs a bell state measurement using psi and a qubit indices
        
        Inputs
        ------
        psi : int
            The index of the qubit that the messenger would like to send
        a : int
            The index of the qubit that is entangled with the receiver's
        """
        self.circ.cx(psi, a)
        self.circ.h(psi)
        
    def _prepare_cbits(self, q1, q2, c1, c2):
        """
        Measures qubits q1 & q2 on classical registers c1 & c2
        
        Inputs
        ------
        q1 : int
            The index of one qubit to measure
        q2 : int
            The index of a second qubit to measure
        c1 : int
            The index of the classical register for q1
        c2 : int
            The index of the classical register for q2
        """
        self.circ.measure(q1, c1)
        self.circ.measure(q2, c2)
        
    def _decode(self, qubit, c1, c2):
        """
        Receiver applies gates depending on the classical bits received
        
        Inputs
        ------
        qubit : int
            The index of the qubit that will receive the teleported qubit
        c1 : ClassicalRegister
            The first classical register to be read from
        c2 : ClassicalRegister
            The second classical register to be read from
        """
        self.circ.x(qubit).c_if(c2, 1)
        self.circ.z(qubit).c_if(c1, 1)
        
    def gen_circuit(self):
        """
        Create a circuit implementing the Quantum Teleportation protocol
        
        Returns
        -------
        QuantumCircuit
            QuatumCircuit object of size nq
        """
        # Initialize the qubit to be teleported
        # Create bell pairs
        for i in range(self.nq):
            self.circ.initialize(self.msg[i].data, 3*i)
            self._create_bell_pair(3*i+1, 3*i+2)
            if (self.barriers):
                self.circ.barrier([3*i, 3*i+1, 3*i+2])
        
        # q1 is sent to messenger and q2 goes to receiver
        
        # Messenger perform bell state measurements
        for i in range(self.nq):
            self._bell_state_measurement(3*i, 3*i+1)
            if (self.barriers):
                self.circ.barrier([3*i, 3*i+1, 3*i+2])
        
        # Messenger prepares their classical bits to send
        for i in range(self.nq):
            self._prepare_cbits(3*i, 3*i+1, self.cr[2*i], self.cr[2*i+1])
            if (self.barriers):
                self.circ.barrier([3*i, 3*i+1, 3*i+2])
                
        # Messenger sends resulting 2 classical bits to receiver
        
        # Receiver applies certain gate(s) given classical bits' information
        for i in range(self.nq):
            self._decode(3*i+2, self.cr[2*i], self.cr[2*i+1])
        
        # Receiver then measures (if the goal is for a product state)
        if (self.measure):
            for i in range(self.nq):
                self.circ.measure(3*i+2, 3*self.nq-i-1)
        
        return self.circ