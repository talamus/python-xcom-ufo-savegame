# TODO: Remove this when postponed annotations are the standard
from __future__ import annotations

from pathlib import Path
from typing import Sequence
from abc import abstractmethod


class BaseRecord:
    """
    ### A base class for all save game records
    """

    ENCODING: str = "cp437"  # A wild guess
    FILE_NAME: str = ""
    NUMBER_OF_RECORDS: int = 0
    RECORD_LENGTH: int = 0  # in bytes
    original_bytes: bytes  # Original binary bytes from the savefile
    active: bool  # Is the entity active or not? (I.e. does it exist.)

    def __init__(self, data: bytes | None = None) -> None:
        self.original_bytes = data
        self.active = False
        if data:
            self.unpack(data)

    @classmethod
    def read(
        cls, save_game_dir: str, container: Sequence[BaseRecord] | None = None
    ) -> Sequence[BaseRecord]:
        """
        Read a single save game file into a container.
        :param save_game_dir:
            Directory name where the `.DAT` files are located.
        :param container:
            Container where the records are going to be stored.
        :returns:
            A list of records.
        """
        if container is None:
            container = list()

        file_name = Path(save_game_dir).joinpath(cls.FILE_NAME)
        index = 0

        with open(file_name, "rb") as file:
            container.clear()
            while True:
                data = file.read(cls.RECORD_LENGTH)
                if len(data) == 0:
                    break
                if (l := len(data)) != cls.RECORD_LENGTH:
                    raise IOError(
                        f"While reading from {file_name}: "
                        f"Was expecting {cls.RECORD_LENGTH} bytes "
                        f"of data but got only {l}."
                    )
                container.append(cls(data))
                index += 1

        if index != cls.NUMBER_OF_RECORDS:
            raise IOError(
                f"While reading from {file_name}: "
                f"Was expecting {cls.NUMBER_OF_RECORDS} records "
                f"but got {index} instead."
            )

        return container

    @classmethod
    def write(cls, save_game_dir: str, container: Sequence[BaseRecord]) -> None:
        """
        Write the content of a container into a single save game file.
        :param save_game_dir:
            Directory name where the `.DAT` files are located.
        :param container:
            Container where the records are stored.
        """

        file_name = Path(save_game_dir).joinpath(cls.FILE_NAME)

        if (index := len(container)) != cls.NUMBER_OF_RECORDS:
            raise IOError(
                f"While writing to {file_name}: "
                f"Was expecting {cls.NUMBER_OF_RECORDS} records "
                f"but got {index} instead."
            )

        with open(file_name, "wb") as file:
            for item in container:
                file.write(item.pack())

    @abstractmethod
    def unpack(self, data: bytes) -> None:
        """Unpack binary string into a record."""
        pass

    @abstractmethod
    def pack(self) -> bytes:
        """Pack the record into a binary string."""
        pass
