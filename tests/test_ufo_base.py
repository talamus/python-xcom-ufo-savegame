from .__fixtures import *
from relatable import RelaTable
from ufo.records.base import Base
from ufo.records.soldier import Soldier


def test_read(game_1_path):
    bases = RelaTable(rows=Base.read(game_1_path))
    soldiers = RelaTable(foreign_keys={"base": bases}, rows=Soldier.read(game_1_path))
    assert len(bases) == 8
    assert soldiers[0].base.name == "Area 52"
    assert bases[0].facilities[2][2] == 0
    assert bases[0].days_to_complete_facility[3][0] == 13


def test_write(game_1_path, game_2_path):
    bases = RelaTable(rows=Base.read(game_1_path))
    Base.write(game_2_path, bases.export())
    new_bases = RelaTable(rows=Base.read(game_2_path))
    for i in range(Base.NUMBER_OF_RECORDS):
        assert bases[i].original_bytes == new_bases[i].pack()
        assert bases[i].data().__dict__ == new_bases[i].data().__dict__


def test_editing(game_1_path):
    bases = RelaTable(rows=Base.read(game_1_path))
    soldiers = RelaTable(foreign_keys={"base": bases}, rows=Soldier.read(game_1_path))
    soldiers[0].base = 2
    assert soldiers[0].base.name == "Eastasia"
    soldiers[0].base = bases[1].primary_key()
    assert soldiers[0].base.name == "Eurasia"
