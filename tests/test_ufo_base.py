import os
import pytest
from pathlib import Path
from ufo.base import Base
from ufo.soldier import Soldier
from ufo.utils.datatable import DataTable


@pytest.fixture
def game_1_path():
    return Path(__file__).parent.joinpath("GAME_1")


@pytest.fixture
def game_2_path():
    path = Path(__file__).parent.joinpath("GAME_2")
    try:
        os.makedirs(path)
    except OSError:
        pass
    return path


def test_read(game_1_path):
    bases = DataTable(Base).read(game_1_path)
    soldiers = DataTable(Soldier, {"base": bases}).read(game_1_path)
    assert len(bases) == 8
    assert soldiers[0].base.name == "Area 52"
    assert bases[0].facilities[2][2] == 0
    assert bases[0].days_to_complete_facility[3][0] == 13


def test_write(game_1_path, game_2_path):
    bases = DataTable(Base).read(game_1_path)
    bases.write(game_2_path)
    new_bases = DataTable(Base).read(game_2_path)
    for i in range(Base.NUMBER_OF_RECORDS):
        assert bases[i].data().__dict__ == new_bases[i].data().__dict__
