# TODO: Remove this when postponed annotations are the standard
from __future__ import annotations

from typing import Any, Iterator, Sequence
from collections.abc import MutableSequence, MutableMapping


class DataRow(MutableMapping):
    """ A thin "database table row"-like wrapper for data objects.
        Supports "foreign key" style references to another DataTables. """

    def __init__(self, table: DataTable, index: int, data: object) -> None:
        self.__table = table
        self.__index = index
        self.__data = data

    def __getattr__(self, field: str) -> Any:
        """ If the data object has the field, return it. Otherwise return a DataRow attribute. """
        if hasattr(self.__data, field):
            return self.__getitem__(field)
        else:
            return self.__getattribute__(field)

    def __setattr__(self, field: str, value: Any) -> None:
        """ If field already exists on data object, set it. Otherwise set a DataRow attribute instead. """
        if "_DataRow__data" in self.__dict__ and hasattr(self.__data, field):
            setattr(self.__data, field, value)
        else:
            super().__setattr__(field, value)

    def __getitem__(self, field: str) -> Any:
        """ If field is a reference to an another table, return the object from there instead. """
        value = getattr(self.__data, field)
        if field in self.__table.references:
            return self.__table.references[field][value]
        else:
            return value

    def __setitem__(self, field: str, value: Any) -> None:
        setattr(self.__data, field, value)

    def __delitem__(self, field: str) -> None:
        delattr(self.__data, field)

    def __len__(self) -> int:
        return len(self.__data)

    def __iter__(self) -> Iterator:
        return iter(self.__data)

    def index(self) -> int:
        """ Return the index number of this DataRow. """
        return self.__index

    def data(self) -> Any:
        """ Return the actual data object of this DataRow. """
        return self.__data


class DataTable(MutableSequence):
    """ A database-like table of database-like rows.
        Supports "foreign key" style (int to index) references to another DataTable. """

    def __init__(self, data_type: type, references: dict[str, Sequence] = {}) -> None:
        """ `references` map a field value (int) to an element in another table/list. """
        self.data_type = data_type
        self.references = dict(references)
        self.rows = list()

    def __getitem__(self, index: int) -> DataRow:
        return self.rows[index]

    def __setitem__(self, index: int, row_data: object) -> None:
        if not isinstance(row_data, self.data_type):
            raise TypeError(
                f"Row data {row_data.__class__} is not {self.data_type}")
        self.rows[index] = DataRow(self, index, row_data)

    def __delitem__(self, index: int) -> None:
        raise NotImplementedError("Removing rows is not supported.")

    def __len__(self) -> int:
        return len(self.rows)

    def insert(self, index: int, row_data: object) -> None:
        if not isinstance(row_data, self.data_type):
            raise TypeError(
                f"Row data {row_data.__class__} is not {self.data_type}")
        if index != len(self.rows):
            raise NotImplementedError(
                "Inserting rows to the middle is not supported.")
        self.rows.insert(index, DataRow(self, index, row_data))

    def clear(self) -> None:
        """ Empty the DataTable. """
        self.rows = list()

    def read(self, save_game_dir: str) -> DataTable:
        """ Read DataTable from a save game file. """
        return self.data_type.read(save_game_dir, self)

    def write(self, save_game_dir: str) -> None:
        """ Write DataTable to a save game file. """
        self.data_type.write(save_game_dir, self)
