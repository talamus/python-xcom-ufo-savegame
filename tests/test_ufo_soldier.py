import os
import pytest
from pathlib import Path
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


def test_simple_read(game_1_path):
    soldiers = Soldier.read(game_1_path)
    assert len(soldiers) == 250
    assert soldiers[8].name == "Helen Jonlan"
    assert soldiers[8].alive


def test_simple_write(game_1_path, game_2_path):
    soldiers = Soldier.read(game_1_path)
    Soldier.write(game_2_path, soldiers)
    new_soldiers = Soldier.read(game_2_path)
    for i in range(Soldier.NUMBER_OF_RECORDS):
        assert soldiers[i].__dict__ == new_soldiers[i].__dict__


def test_datatable_read(game_1_path):
    soldiers = DataTable(Soldier).read(game_1_path)
    assert len(soldiers) == 250
    assert soldiers[8].name == "Helen Jonlan"
    assert soldiers[8].alive


def test_datatable_write(game_1_path, game_2_path):
    soldiers = DataTable(Soldier).read(game_1_path)
    soldiers.write(game_2_path)
    new_soldiers = DataTable(Soldier).read(game_2_path)
    for i in range(Soldier.NUMBER_OF_RECORDS):
        assert soldiers[i].data().__dict__ == new_soldiers[i].data().__dict__
