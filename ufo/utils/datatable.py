from __future__ import annotations  # TODO: Remove when forward declaring
# of type hints are the standard
from typing import Any, Iterator
from collections.abc import MutableSequence, MutableMapping


class DataRow(MutableMapping):
    """ A single database-like data row.
        Supports "foreign key"-like references to another tables. """

    def __init__(self, table: DataTable, index: int, data: object) -> None:
        self.__table = table
        self.__index = index
        self.__data = data

    def __getattr__(self, field: str) -> Any:
        """ If data has the field, return it. Otherwise return a DataRow attribute. """
        if hasattr(self.__data, field):
            return self.__getitem__(field)
        else:
            return self.__getattribute__(field)

    def __setattr__(self, field: str, value: Any) -> None:
        if "_DataRow__data" in self.__dict__ and hasattr(self.__data, field):
            setattr(self.__data, field, value)
        else:
            super().__setattr__(field, value)

    def __getitem__(self, field: str) -> Any:
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
        return self.__index

    def data(self) -> Any:
        return self.__data


class DataTable(MutableSequence):
    """ A table of multiple database-like records. """

    def __init__(self, data_type: type, references: dict[str, DataTable] = {}) -> None:
        """ `references` allow smart links from a field value to an another DataTable row. """
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
        del self.rows[index]

    def __len__(self) -> int:
        return len(self.rows)

    def insert(self, index: int, row_data: object) -> None:
        if not isinstance(row_data, self.data_type):
            raise TypeError(
                f"Row data {row_data.__class__} is not {self.data_type}")
        self.rows.insert(index, DataRow(self, index, row_data))
