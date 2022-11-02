import pytest
from ufo.utils.datatable import *

# --- Test Data --------------------------------------------------------------


class Thing:
    def __init__(self, data: dict[str, Any]) -> None:
        for key, value in data.items():
            setattr(self, key, value)


class TotallyDifferentClass:
    pass


OWNERS = [
    Thing({"name": "Jaakko", "age": 36}),
    Thing({"name": "Eino",   "age": 4}),
]
POSSESSIONS = [
    Thing({"owner": 0, "item": "mortgage"}),
    Thing({"owner": 1, "item": "teddy bear"}),
    Thing({"owner": 2, "item": "ufo"}),
]

owners = DataTable(Thing)
for owner in OWNERS:
    owners.append(owner)

possessions = DataTable(Thing, {"owner": owners})
for possession in POSSESSIONS:
    possessions.append(possession)


# --- Actual Tests -----------------------------------------------------------


def test_that_fundamentals_have_not_changed():
    assert "_DataRow__data" in owners[0].__dict__


def test_basics():
    assert possessions[1]["item"] == "teddy bear"
    assert owners[0]["name"] == "Jaakko"
    assert possessions[1].item == "teddy bear"
    assert owners[0].name == "Jaakko"


def test_referencing():
    assert possessions[0].owner.age == 36
    assert possessions[1].owner.name == "Eino"
    assert possessions[1].owner.index() == 1


def test_index_and_data():
    assert owners[1].index() == 1
    assert owners[0].data() == OWNERS[0]
    assert possessions[0].index() == 0
    assert possessions[1].data() == POSSESSIONS[1]
    assert possessions[0].owner.data() == OWNERS[possessions[0].owner.index()]


def test_broken_reference():
    with pytest.raises(IndexError):
        possessions[2].owner


def test_removing_and_inserting_rows():
    with pytest.raises(NotImplementedError):
        del possessions[0]
    with pytest.raises(NotImplementedError):
        possessions.insert(0, Thing({"nope": "wont work"}))


def test_wrong_row_data_type():
    with pytest.raises(TypeError):
        owners.append(TotallyDifferentClass())
    with pytest.raises(TypeError):
        owners[1] = TotallyDifferentClass()


def test_index_and_data():
    assert owners[0].index() == 0
    assert possessions[1].index() == 1
    assert owners[0].data() == OWNERS[0]
    assert possessions[1].data() == POSSESSIONS[1]


def test_manipulating_existing_data():
    possessions[2]["owner"] = owners[0].index()
    assert POSSESSIONS[2].owner == 0
    assert possessions[2].owner.name == "Jaakko"

    possessions[2].owner["name"] = "Teppo"
    assert possessions[2].owner.name == "Teppo"

    possessions[2].owner = owners[1].index()
    assert POSSESSIONS[2].owner == owners[1].index()
    assert possessions[2].owner.name == "Eino"

    possessions[2].owner.name = "Leino"
    assert possessions[2].owner.name == "Leino"


def test_data_iteration():
    new_owners = []
    for owner in owners:
        new_owners.append(owner.data())
    for i in range(len(new_owners)):
        assert new_owners[i] == OWNERS[i]
    assert len(OWNERS) == len(owners)
    assert len(new_owners) == len(owners)


def test_clearing_the_table():
    owners.clear()
    possessions.clear()
    assert len(owners) == 0
    assert len(possessions) == 0
