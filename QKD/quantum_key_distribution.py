from qiskit import QuantumCircuit, execute, Aer
from numpy.random import randint
import numpy as np

class QKD:
    """
    Generate an instance of the Quantum Key Distribution Protocol.
    
    Attributes
    ----------
    eave : boolean
        Whether or not there is an eavesdropper (default is false)
    init_length : int
        Length of the initial message established by Alice (default is 100)
    sample_size : int
        Length of the sample size (default is 15)
    seed : int
        Opportunity to alter the seed of the random int generator (default is 0)
    barriers : boolean
        Choice to include barriers in circuits (default is true)
    circs : List of QuantumCircuit
        List of Qiskit QuantumCircuits that represents the circuit
    """
    
    def __init__(self, eave=False, init_length=100, sample_size=15, seed=0, barriers=True):
        # Check the parameters for errors
        if (init_length < 2*sample_size+3):
            raise Exception('Ensure that init_length is considerably larger than sample_size')
        
        # Apply the parameters
        np.random.seed(seed=seed)
        self.__n = init_length
        self.__sample_size = sample_size
        self.__barriers = barriers
        
        # Alice generates her random set of bits
        self.alice_bits = randint(2, size=self.__n)
        
        # Alice chooses bases at random (0=z, 1=x)
        self.alice_bases = randint(2, size=self.__n)
        self.__msg = self._encode()
        
        # Interception (IF applicable)
        if (eave):
            eave_bases = randint(2, size=self.__n)
            intercepted_msg = self._measure_message(eave_bases, True)
        
        # Bob chooses his bases at random and measures
        self.bob_bases = randint(2, size=self.__n)
        self.bob_results = self._measure_message(self.bob_bases, False)
        
        # Alice and Bob discard useless bits
        self.alice_key = self._remove_garbage(self.alice_bits)
        self.bob_key = self._remove_garbage(self.bob_results)
        
        # Prepare bit selection for sample
        bit_selection = randint(self.__n, size=self.__sample_size)
        self.bob_sample = self._sample_bits(self.bob_key, bit_selection)
        self.alice_sample = self._sample_bits(self.alice_key, bit_selection)
    
    def _encode(self):
        """
        Alice measures her random bits on her random bases
        """
        msg = []
        for i in range(self.__n):
            qc = QuantumCircuit(1, 1)
            if self.alice_bases[i] == 0:
                if self.alice_bits[i] == 0:
                    pass
                else:
                    qc.x(0)
            else:
                if self.alice_bits[i] == 0:
                    qc.h(0)
                else:
                    qc.x(0)
                    qc.h(0)
            if (self.__barriers): qc.barrier()
            msg.append(qc)
        return msg
    
    def _measure_message(self, bases, eave):
        """
        Using the shared message, measure with random bases
        
        Inputs
        ------
        bases : array
            Bases to measure in
        eave : boolean
            Is eave the one measuring right now?
        """
        backend = Aer.get_backend('qasm_simulator')
        measurements = []
        for i in range(self.__n):
            if bases[i] == 0:
                self.__msg[i].measure(0, 0)
            else:
                self.__msg[i].h(0)
                self.__msg[i].measure(0, 0)
            result = execute(self.__msg[i], backend, shots=1, memory=True).result()
            measured_bit = int(result.get_memory()[0])
            measurements.append(measured_bit)
            if(self.__barriers and eave): self.__msg[i].barrier()
        measurements = np.array(measurements)
        return measurements
    
    def _remove_garbage(self, bits):
        """
        Traverse Alice and Bob's bases and if they are the same then save bit at that index
        
        Inputs
        ------
        bits : array
            Bits to clean out
        """
        good_bits = []
        for i in range(self.__n):
            if self.alice_bases[i] == self.bob_bases[i]:
                good_bits.append(bits[i])
        return good_bits
        
    def _sample_bits(self, bits, selection):
        """
        Takes a selected sample out of the bits as a test
        
        Inputs
        ------
        bits : array
            The full set of bits to sample
        selection : array
            Array of indices to sample out of the bits
        """
        sample = []
        for i in selection:
            i = np.mod(i, len(bits))
            sample.append(bits.pop(i))
        sample = np.array(sample)
        return sample
        
    def prob_eave_win(self):
        """
        Returns the probability of an eavesdropper not being detected.
        """
        return 0.75**self.__sample_size
        
    def circuits(self):
        """
        Returns the list of circuits that describes the communication at each bit.
        """
        return self.__msg