import os
from dataclasses import dataclass
from enum import IntEnum
from fractions import Fraction
from io import BufferedReader
from pprint import pformat
from typing import Dict, List

from ..sector import Sector
from .sector_offsets import SectorOffset

__all__ = ['VTSPGCI', 'ProgramChain', 'PlaybackTime', 'PGCOffset']


class PGCOffset(IntEnum):
    """http://dvd.sourceforge.net/dvdinfo/pgc.html"""
    # 0x0000
    NB_PROGRAMS = 0X0002
    NB_CELLS = 0X0003
    PLAYBACK_TIME = 0X0004
    UOPS = 0X0008
    PGC_AST_CTL = 0X000C
    PGC_SPST_CTL = 0X001C
    NEXT_PGCN = 0X009C
    PREVIOUS_PGCN = 0X009E
    GOUP_PGCN = 0X00A0
    PGC_STILL_TIME = 0X00A2
    PG_PLAYBACK_MODE = 0X00A3
    PALETTE = 0X00A4

    COMMANDS_OFFSET = 0X00E4
    PROGRAM_MAP_OFFSET = 0X00E6
    CELL_PLAYBACK_INFO_TABLE_OFFSET = 0X00E8
    CELL_POS_INFO_TABLE_OFFSET = 0X00EA



@dataclass
class PlaybackTime:
    fps: int
    hours: int
    minutes: int
    seconds: int
    frames: int

    def __repr__(self) -> str:
        return pformat(vars(self), sort_dicts=False)


@dataclass
class ProgramChain:
    duration: PlaybackTime
    nb_program: int
    playback_times: List[PlaybackTime]

    def __repr__(self) -> str:
        return pformat(vars(self), sort_dicts=False)


class VTSPGCI(Sector):
    nb_program_chains: int
    program_chains: List[ProgramChain]

    chain_offset: int

    def __init__(self, ifo: BufferedReader) -> None:
        super().__init__(ifo)

    def load(self):
        self.ifo.seek(SectorOffset.SECTOR_POINTER_VTS_PGCI, os.SEEK_SET)
        offset, = self._unpack_byte(4)

        self.ifo.seek(2048 * offset + 0x01, os.SEEK_SET)
        self.nb_program_chains, = self._unpack_byte(1)

        pcgit_pos = offset * 0x800

        self.ifo.seek(SectorOffset.SECTOR_POINTER_VTS_PGCI, os.SEEK_SET)



        self.program_chains = []

        for nbpgc in range(1, self.nb_program_chains + 1):
            self.ifo.seek(pcgit_pos + (8 * nbpgc) + 4, os.SEEK_SET)
            self.chain_offset, = self._unpack_byte(4)

            offset = pcgit_pos + self.chain_offset

            self.ifo.seek(offset + PGCOffset.NB_PROGRAMS, os.SEEK_SET)
            nb_program, = self._unpack_byte(1)

            self.ifo.seek(offset + PGCOffset.PLAYBACK_TIME, os.SEEK_SET)
            duration = self._get_timespan(self.ifo.read(4))

            # ...

            self.ifo.seek(offset + PGCOffset.PROGRAM_MAP_OFFSET, os.SEEK_SET)
            program_map_offset, = self._unpack_byte(2)

            self.ifo.seek(offset + PGCOffset.CELL_PLAYBACK_INFO_TABLE_OFFSET, os.SEEK_SET)
            cell_table_offset, = self._unpack_byte(2)



            playback_times: List[PlaybackTime] = []

            for program in range(nb_program):
                self.ifo.seek(offset + program_map_offset + program, os.SEEK_SET)
                entry_cell, = self._unpack_byte(1)

                exit_cell = entry_cell

                if program < nb_program - 1:
                    self.ifo.seek(offset + program_map_offset + program + 0x01, os.SEEK_SET)
                    exit_cell, = self._unpack_byte(1)
                    exit_cell -= 1


                for cell in range(entry_cell, exit_cell + 1):
                    cell_start = cell_table_offset + (cell - 1) * 0x18

                    self.ifo.seek(offset + cell_start, os.SEEK_SET)
                    cell_type = self.ifo.read(4)[0] >> 6

                    if cell_type in {0x00, 0x01}:
                        self.ifo.seek(offset + cell_start + 0x0004, os.SEEK_SET)
                        playback_time = self._get_timespan(self.ifo.read(4))
                    else:
                        raise ValueError

                    playback_times.append(playback_time)

            self.program_chains.append(
                ProgramChain(duration, nb_program, playback_times)
            )

        return self

    def _get_timespan(self, data: bytes) -> PlaybackTime:
        frames = self._get_frames(data[3])
        fps = data[3] >> 6

        if fps not in FRAMERATE:
            raise ValueError

        hours, minutes, seconds = [self._bcd_to_int(data[i]) for i in range(3)]

        return PlaybackTime(fps, hours, minutes, seconds, frames)


    def _get_frames(self, byte: int) -> int:
        if ((byte >> 6) & 0x01) == 1:
            frames = self._bcd_to_int(byte & 0x3F)
        else:
            raise ValueError
        return frames

    @staticmethod
    def _bcd_to_int(bcd: int) -> int:
        return ((0xFF & (bcd >> 4)) * 10) + (bcd & 0x0F)


FRAMERATE: Dict[int, Fraction] = {
    0x01: Fraction(25),
    0x03: Fraction(30000, 1001)
}
