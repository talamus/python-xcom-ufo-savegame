from typing import Any
from struct import pack, unpack
from ufo.baserecord import BaseRecord


class Base(BaseRecord):
    """ Represents a single base from BASE.DAT """

    FILE_NAME = "BASE.DAT"
    NUMBER_OF_RECORDS = 8
    RECORD_LENGTH = 292  # bytes

    def unpack(self, data: bytes) -> None:
        (
            name,
            self.short_range_detection_capability,
            self.long_range_detection_capability,
            self.hyperwave_detection_capability,
            facilities,
            days_to_complete_facility,
            self.engineers,
            self.scientists,
            storage_items,
            base_inactive
        ) = unpack("<16shhh36s36sBB192si", data)

        self.active = not base_inactive
        if not self.active:
            return

        name = name.decode(self.ENCODING)
        self.name = name.split("\0")[0]

        self.facilities = unpack("<6s6s6s6s6s6s", facilities)
        self.days_to_complete_facility = unpack("<6s6s6s6s6s6s", days_to_complete_facility)
        self.storage_items = unpack("<96h", storage_items)

    def pack(self) -> bytes:
        if not self.active:
            return pack("<288si", b"", 1)

        return pack("<16shhh36s36sBB192si",
            self.name.encode(self.ENCODING),
            self.short_range_detection_capability,
            self.long_range_detection_capability,
            self.hyperwave_detection_capability,
            pack("<6s6s6s6s6s6s", *self.facilities),
            pack("<6s6s6s6s6s6s", *self.days_to_complete_facility),
            self.engineers,
            self.scientists,
            pack("<96h", *self.storage_items),
            0
        )
