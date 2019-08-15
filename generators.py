from .supremacy import Qgrid
from .supremacy import Qbit
#from .ansatz import HWEA
from .QAOA import hw_efficient_ansatz
from .VQE import uccsd_ansatz
from .QFT import qft_circ

def gen_supremacy(height, width, depth, order=None, singlegates=True,
                  mirror=True, barriers=False, measure=False, regname=None):
    """
    Calling this function will create and return a quantum supremacy
    circuit as found in https://www.nature.com/articles/s41567-018-0124-x
    """

    grid = Qgrid.Qgrid(height, width, depth, order=order,
                       singlegates=singlegates, mirror=mirror,
                       barriers=barriers, measure=measure, regname=regname)

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

