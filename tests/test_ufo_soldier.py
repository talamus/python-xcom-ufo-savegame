from .__fixtures import *
from relatable import RelaTable
from ufo.records.soldier import Soldier


def test_read(game_1_path):
    soldiers = Soldier.read(game_1_path)
    assert len(soldiers) == 250
    assert soldiers[8].name == "Helen Jonlan"
    assert soldiers[8].active


def test_write(game_1_path, game_2_path):
    soldiers = Soldier.read(game_1_path)
    Soldier.write(game_2_path, soldiers)
    new_soldiers = Soldier.read(game_2_path)
    for i in range(Soldier.NUMBER_OF_RECORDS):
        assert soldiers[i].original_bytes == new_soldiers[i].pack()
        assert soldiers[i].__dict__ == new_soldiers[i].__dict__
