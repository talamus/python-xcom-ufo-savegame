from pathlib import Path
import pytest
import os


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
