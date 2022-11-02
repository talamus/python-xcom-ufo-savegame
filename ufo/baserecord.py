# TODO: Remove this when postponed annotations are the standard
from __future__ import annotations

from pathlib import Path
from typing import Sequence
from abc import abstractmethod


class BaseRecord:
    """ A base class for all save game records. """

    ENCODING = "cp437"      # A wild guess
    FILE_NAME = ""
    NUMBER_OF_RECORDS = 0
    RECORD_LENGTH = 0       # In bytes

    @classmethod
    def read(cls, save_game_dir: str, container: Sequence[BaseRecord] = list()):
        """ Read a single save game file into a container. """

        file_name = Path(save_game_dir).joinpath(cls.FILE_NAME)
        index = 0

        with open(file_name, "rb") as file:
            container.clear()
            while True:
                data = file.read(cls.RECORD_LENGTH)
                if len(data) == 0:
                    break
                if (l := len(data)) != cls.RECORD_LENGTH:
                    raise IOError(file_name, "r", "RECORD_LENGTH",
                                  f"Was expecting {cls.RECORD_LENGTH} bytes "
                                  f"of data but got only {l}.")
                container.append(cls(data))
                index += 1

        if index != cls.NUMBER_OF_RECORDS:
            raise IOError(file_name, "r", "NUMBER_OF_RECORDS",
                          f"Was expecting {cls.NUMBER_OF_RECORDS} records "
                          f"but got {index} instead.")

        return container

    @classmethod
    def write(cls, save_game_dir: str, container: Sequence[BaseRecord]) -> None:
        """ Write the content of a container into a single save game file. """

        file_name = Path(save_game_dir).joinpath(cls.FILE_NAME)

        if (index := len(container)) != cls.NUMBER_OF_RECORDS:
            raise IOError(file_name, "w", "NUMBER_OF_RECORDS",
                          f"Was expecting {cls.NUMBER_OF_RECORDS} records "
                          f"but got {index} instead.")

        with open(file_name, "wb") as file:
            for item in container:
                file.write(item.pack())

    @abstractmethod
    def unpack(self, data: bytes) -> None: pass

    @abstractmethod
    def pack(self) -> bytes: pass
