from .Supremacy import Qgrid_original, Qgrid_Sycamore
from .QAOA import hw_efficient_ansatz
from .VQE import uccsd_ansatz
from .QFT import qft_circ
from .QWalk import quantum_walk
from .Dynamics import quantum_dynamics

def gen_supremacy(height, width, depth, order=None, singlegates=True,
                  mirror=False, barriers=False, measure=False, regname=None):
    """
    Calling this function will create and return a quantum supremacy
    circuit based on the implementations in
    https://www.nature.com/articles/s41567-018-0124-x and
    https://github.com/sboixo/GRCS.
    """

    grid = Qgrid_original.Qgrid(height, width, depth, order=order,
                                mirror=mirror, singlegates=singlegates,
                                barriers=barriers, measure=measure,
                                regname=regname)

    circ = grid.gen_circuit()

    return circ


def gen_sycamore(height, width, depth, order=None, singlegates=True,
                  barriers=False, measure=False, regname=None):
    """
    Calling this function will create and return a quantum supremacy
    circuit as found in https://www.nature.com/articles/s41586-019-1666-5
    """

    grid = Qgrid_Sycamore.Qgrid(height, width, depth, order=order,
                                singlegates=singlegates, barriers=barriers,
                                measure=measure, regname=regname)

    circ = grid.gen_circuit()

    return circ


def gen_hwea(width, depth, parameters='optimal', seed=None, barriers=False,
             measure=False, regname=None):
    """
    Create a quantum circuit implementing a hardware efficient
    ansatz with the given width (number of qubits) and
    depth (number of repetitions of the basic ansatz).
    """

    hwea = hw_efficient_ansatz.HWEA(width, depth, parameters=parameters,
                                    seed=seed, barriers=barriers,
                                    measure=measure, regname=regname)

    circ = hwea.gen_circuit()

    return circ


def gen_uccsd(width, parameters='seeded', seed=None, barriers=True,
              regname=None):
    """
    Generate a UCCSD ansatz with the given width (number of qubits).
    """

    uccsd = uccsd_ansatz.UCCSD(width, parameters=parameters, seed=seed,
                               barriers=barriers, regname=regname)

    circ = uccsd.gen_circuit()

    return circ


def gen_qft(width, inverse=False, kvals=False, barriers=True, measure=False,
            regname=None):
    """
    Generate a QFT (or iQFT) circuit with the given number of qubits
    """

    qft = qft_circ.QFT(width, inverse=inverse, kvals=kvals, barriers=barriers,
                       measure=measure, regname=regname)

    circ = qft.gen_circuit()

    return circ


def gen_qwalk(n, barriers=True, regname=None):
    """
    Generate a quantum walk circuit with specified value of n
    """

    qwalk = quantum_walk.QWALK(n, barriers=barriers, regname=regname)

    circ = qwalk.gen_circuit()

    return circ


def gen_dynamics(H, barriers=True, measure=False, regname=None):
    """
    Generate a circuit to simulate the dynamics of a given Hamiltonian
    """

    dynamics = quantum_dynamics.Dynamics(H, barriers=barriers, measure=measure,
                                         regname=regname)

    circ = dynamics.gen_circuit()

    return circ





