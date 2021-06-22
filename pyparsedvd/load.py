"""Convenience functions"""

__all__ = ['load_vts_pgci']

from io import BufferedReader

from .vts_ifo.vts_pgci import VTSPGCI


def load_vts_pgci(ifo: BufferedReader) -> VTSPGCI:
    """Loads and returns a VTSPGCI object"""
    return VTSPGCI(ifo).load()
