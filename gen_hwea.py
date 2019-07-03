from .ansatz import HWEA


def generate(width, depth):
    """
    Create a quantum circuit implementing a hardware efficient
    ansatz with the given width (number of qubits) and 
    depth (number of repetitions of the basic ansatz).
    """

    hwea = HWEA.HWEA(width, depth)

    circ = hwea.gen_circuit()

    return circ
