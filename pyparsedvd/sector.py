from abc import ABC, abstractmethod
from io import BufferedReader
from pprint import pformat
from struct import unpack
from typing import Any, Dict, Tuple

__all__ = ['Sector']


class Sector(ABC):
    """Abstract IFO sector object interface"""
    ifo: BufferedReader

    def __init__(self, ifo: BufferedReader) -> None:
        self.ifo = ifo
        super().__init__()

    def __repr__(self) -> str:
        return pformat(vars(self), sort_dicts=False)

    @abstractmethod
    def load(self):
        """Method loading the IFO object"""

    def _unpack_byte(self, n: int) -> Tuple[Any, ...]:
        """
            Size 1 -> big-endian unsigned char
            Size 2 -> big-endian unsigned short
            Size 4 -> big-endian unsigned int
            Size 8 -> big-endian unsigned long long
        """
        formats: Dict[int, str] = {1: '>B', 2: '>H', 4: '>I', 8: '>Q'}
        return unpack(formats[n], self.ifo.read(n))
