from distutils.core import setup
from Cython.Build import cythonize
import py2exe

setup(
    ext_modules=cythonize(["mcts.pyx", "bitboard.pyx"]),
    windows = [{"script": "loa.py"}],
    data_files = [(".", ["mcts.pyd", "bitboard.pyd", "constants.py"])]
)