from .supremacy import Qgrid
from .supremacy import Qbit


def generate(height, width, depth, order=None, singlegates=True, mirror=True):
    """
    Calling this function will create and return a quantum supremacy
    circuit as found in https://www.nature.com/articles/s41567-018-0124-x
    """

    grid = Qgrid.Qgrid(height, width, depth, order=order, singlegates=singlegates, mirror=mirror)

    circ = grid.gen_circuit()

    return circ


